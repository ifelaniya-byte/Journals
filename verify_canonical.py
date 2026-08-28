#!/usr/bin/env python3
"""Verify generated product facts against PORTFOLIO.md's canonical table.

This guard deliberately treats PORTFOLIO.md—not generator constants or a
previously generated CATALOG.csv—as the source for decision-bound product
fields. It verifies all 18 concepts for title, configured collection, pages,
trim, price posture, wave, and publication status. It also verifies generated
book metadata and builder/release configuration where those facts exist.

A value of `TBD` or `N/A` is meaningful policy, not a loose placeholder: it
must match exactly and prevents a held/Vault item from inheriting a sellable
price merely because a build tuple contains a legacy numeric default.
"""
from __future__ import annotations

import ast
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TABLE_MARKER = '## Machine-readable canonical product table'
TABLE_END = '## Signed decision controls'
FIELDS = ('amazon_title', 'collection', 'pages', 'trim', 'price', 'release_wave', 'publication_status')
CANON_HEADERS = {
    'Canonical title': 'amazon_title',
    'Configured collection': 'collection',
    'Pages': 'pages',
    'Trim': 'trim',
    'Price posture': 'price',
    'Release wave': 'release_wave',
    'Publication status': 'publication_status',
}


def markdown_cells(line: str) -> list[str]:
    """Split the simple controlled table while honoring escaped pipes."""
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        return []
    content = line[1:-1]
    cells, current, escaped = [], [], False
    for char in content:
        if escaped:
            current.append(char)
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == '|':
            cells.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append('\\')
    cells.append(''.join(current).strip())
    return cells


def canonical_rows() -> dict[str, dict[str, str]]:
    text = (ROOT / 'PORTFOLIO.md').read_text(encoding='utf8')
    if TABLE_MARKER not in text or TABLE_END not in text:
        raise ValueError('PORTFOLIO.md canonical table markers are missing')
    section = text.split(TABLE_MARKER, 1)[1].split(TABLE_END, 1)[0]
    table_lines = [line for line in section.splitlines() if line.startswith('|')]
    if len(table_lines) < 3:
        raise ValueError('PORTFOLIO.md canonical table has no data rows')
    headers = markdown_cells(table_lines[0])
    expected_headers = ['ID', *CANON_HEADERS]
    if headers != expected_headers:
        raise ValueError(f'canonical table headers differ: {headers!r}')
    result: dict[str, dict[str, str]] = {}
    for line in table_lines[2:]:
        values = markdown_cells(line)
        if len(values) != len(headers):
            raise ValueError(f'malformed canonical table row: {line!r}')
        row = dict(zip(headers, values))
        sku = row.pop('ID')
        if not re.fullmatch(r'[AB]\d\d', sku):
            raise ValueError(f'invalid SKU {sku!r} in canonical table')
        if sku in result:
            raise ValueError(f'duplicate canonical SKU {sku}')
        result[sku] = {CANON_HEADERS[name]: row[name] for name in CANON_HEADERS}
    if len(result) != 18:
        raise ValueError(f'canonical table must contain exactly 18 SKUs, found {len(result)}')
    return result


def literal_assignment(name: str):
    tree = ast.parse((ROOT / 'build_catalog.py').read_text(encoding='utf8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f'build_catalog.py does not have literal {name}')


def metadata_fields(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding='utf8').splitlines():
        if ': ' in line:
            key, value = line.split(': ', 1)
            values[key] = value
    return values


def main() -> int:
    try:
        canonical = canonical_rows()
        manifest = {row['id']: row for row in csv.DictReader((ROOT / 'CATALOG.csv').open(encoding='utf8'))}
        products = {row[0]: row for row in literal_assignment('PRODUCTS')}
        release_state = literal_assignment('RELEASE_STATE')
        non_kdp = literal_assignment('NON_KDP_PRODUCTS')
    except (OSError, ValueError, SyntaxError, csv.Error) as error:
        print(f'FAIL  canonical baseline cannot be read: {error}')
        return 1

    errors: list[str] = []
    for sku, expected in canonical.items():
        observed = manifest.get(sku)
        if observed is None:
            errors.append(f'{sku}: missing from CATALOG.csv')
            continue
        for field in FIELDS:
            if observed.get(field) != expected[field]:
                errors.append(f'{sku}: CATALOG.csv {field}={observed.get(field)!r}; canonical={expected[field]!r}')
        state = release_state.get(sku)
        if state is None:
            errors.append(f'{sku}: missing from RELEASE_STATE')
        elif (state[0], state[1]) != (expected['release_wave'], expected['publication_status']):
            errors.append(f'{sku}: RELEASE_STATE={(state[0], state[1])!r}; canonical wave/status={(expected["release_wave"], expected["publication_status"])!r}')

        if sku == 'A03':
            spec = non_kdp.get('A03', {})
            if (str(spec.get('pages')), spec.get('trim'), spec.get('price')) != (expected['pages'], expected['trim'], expected['price']):
                errors.append('A03: NON_KDP_PRODUCTS page/trim/price does not match canonical table')
            brief = ROOT / observed['folder'] / 'PRODUCT_BRIEF.md'
            if not brief.is_file():
                errors.append('A03: non-KDP product brief missing')
            continue

        product = products.get(sku)
        if product is None:
            errors.append(f'{sku}: missing from PRODUCTS')
            continue
        title, collection, trim, target_pages = product[4], product[2], product[6], product[7]
        if title != expected['amazon_title']:
            errors.append(f'{sku}: generator title does not match canonical table')
        if collection != expected['collection']:
            errors.append(f'{sku}: generator collection does not match canonical table')
        if f'{trim[0]:g}x{trim[1]:g}' != expected['trim']:
            errors.append(f'{sku}: generator trim does not match canonical table')
        if str(target_pages) != expected['pages']:
            errors.append(f'{sku}: generator target pages does not match canonical table')

        metadata_path = ROOT / observed['folder'] / 'metadata.txt'
        if not metadata_path.is_file():
            errors.append(f'{sku}: generated metadata missing')
            continue
        md = metadata_fields(metadata_path)
        checks = {
            'AMAZON TITLE': expected['amazon_title'],
            'SERIES': expected['collection'],
            'PAGES': expected['pages'],
            'PRICE': expected['price'],
        }
        trim_md = md.get('TRIM', '').replace(' × ', 'x').replace(' in.', '')
        if trim_md != expected['trim']:
            errors.append(f'{sku}: metadata TRIM={md.get("TRIM")!r}; canonical={expected["trim"]!r}')
        for label, wanted in checks.items():
            if md.get(label) != wanted:
                errors.append(f'{sku}: metadata {label}={md.get(label)!r}; canonical={wanted!r}')

    extra = set(manifest) - set(canonical)
    if extra:
        errors.append('CATALOG.csv contains non-canonical SKUs: ' + ', '.join(sorted(extra)))
    if errors:
        for error in errors:
            print('FAIL ', error)
        print(f'\nCanonical verification blocked: {len(errors)} mismatch(es).')
        return 1
    print('PASS  canonical portfolio table matches all 18 catalog rows, build configuration, release states, and applicable metadata.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
