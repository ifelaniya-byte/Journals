#!/usr/bin/env python3
"""Package approved release assets on demand.

Default: package only Wave 1 candidate upload assets. This does not mark them cleared—see
RELEASE_POLICY.md. Use --all-vault only for internal book-form reference assets after explicit founder approval; strictly non-KDP A03 is excluded.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import csv, shutil, sys
R=Path(__file__).resolve().parent
release=R/'release'; dest=R/'packages'

def zip_files(path, target, names):
    with ZipFile(target,'w',ZIP_DEFLATED) as z:
        for n in names:z.write(path/n, arcname=n)

def main(mode='wave1'):
    rows=list(csv.DictReader((R/'CATALOG.csv').open(encoding='utf-8')))
    if mode=='wave1': rows=[r for r in rows if r['release_wave']=='Wave 1']
    elif mode=='--all-vault':
        rows=[r for r in rows if r['release_wave']=='Vault' and r['folder'].startswith('release/')]
    else: raise SystemExit('Use no argument for Wave 1 only, or --all-vault for an explicit internal archive of book-form reference assets.')
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir()
    for r in rows:
        p=R/r['folder']; stem=f"{r['id']}-{p.name.replace(r['id']+'-','')}"
        zip_files(p,dest/f'{stem}_KDP-upload.zip',['interior.pdf','cover_wrap.pdf','metadata.txt'])
        zip_files(p,dest/f'{stem}_listing-assets.zip',['cover.jpg','listing_02_interior.jpg','listing_03_interior.jpg','listing_04_interior.jpg','listing_05_interior.jpg','listing_06_callout.jpg','listing_07_series.jpg'])
    print(f'Created {len(rows)*2} ZIP files for {len(rows)} {"Wave 1" if mode=="wave1" else "internal archive"} products in {dest}')
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'wave1')
