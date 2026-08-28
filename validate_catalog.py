#!/usr/bin/env python3
"""Structural QC for all 18 Ritual Library KDP scout packages.

Validates file inventory, metadata completeness, 7-keyword requirement, interior pages/trim,
cover dimensions/spine math, listing image dimensions, upload-checklist headings, and lookbook.
It is structural QC only; it does not replace KDP Previewer, physical proofs, or legal review.
"""
from pathlib import Path
import csv, re, sys, json
from PIL import Image
import fitz
R=Path(__file__).resolve().parent
CAT=R/'CATALOG.csv'; REL=R/'release'
BRAND=json.loads((R/'brand_config.json').read_text(encoding='utf-8')); IMPRINT=BRAND.get('imprint','').strip(); DOMAIN=BRAND.get('domain','').strip()
BLEED=.125; PPI=.002252
fails=[]; passed=0

def check(ok,label):
    global passed
    if ok: passed+=1
    else: fails.append(label)

def num(s):return float(s)

rows=list(csv.DictReader(CAT.open(encoding='utf-8')))
check(len(rows)==18,'catalog must have 18 products')
required_policy_fields={'release_wave','publication_status','primary_validation','release_trigger'}
check(required_policy_fields.issubset(rows[0].keys()),'catalog release-policy columns present')
check(sum(r.get('release_wave')=='Wave 1' for r in rows)==6,'exactly six Wave 1 candidates')
check(sum(r.get('release_wave')=='Vault' for r in rows)==2,'exactly two KDP vault products')
check(bool(IMPRINT) and IMPRINT not in {'[Author / Imprint]','Author / Imprint'},'working imprint is configured')
print(f"{'ID':<4} {'PRODUCT':<32} {'PG':>4} {'TRIM':>10} {'INT':>3} {'WRAP':>4} {'META':>4} {'IMG':>3}")
for r in rows:
    folder=R/r['folder']; trim=tuple(map(float,r['trim'].split('x')));pages=int(r['pages'])
    required=['interior.pdf','cover_wrap.pdf','cover.jpg','listing_02_interior.jpg','listing_03_interior.jpg','listing_04_interior.jpg','listing_05_interior.jpg','listing_06_callout.jpg','listing_07_series.jpg','metadata.txt']
    inv=all((folder/x).exists() for x in required)
    interior=fitz.open(folder/'interior.pdf'); rect=interior[0].rect
    intok=len(interior)==pages and abs(rect.width/72-trim[0])<.02 and abs(rect.height/72-trim[1])<.02 and bool(interior[0].get_text().strip())
    wrap=fitz.open(folder/'cover_wrap.pdf');wr=wrap[0].rect;spine=pages*PPI;ew=2*BLEED+2*trim[0]+spine;eh=2*BLEED+trim[1]
    wrapok=len(wrap)==1 and abs(wr.width/72-ew)<.02 and abs(wr.height/72-eh)<.02 and 'BARCODE KEEP-CLEAR AREA' in wrap[0].get_text()
    md=(folder/'metadata.txt').read_text(encoding='utf-8') if (folder/'metadata.txt').exists() else ''
    fields=['AMAZON TITLE:','COVER TITLE:','SUBTITLE:','AUTHOR:','SERIES:','FORMAT:','TRIM:','PAGES:','PRICE:','CATEGORIES:','KEYWORDS:','DESCRIPTION:','CLAIMS / RELEASE BOUNDARY:']
    kw=[]
    m=re.search(r'^KEYWORDS:\s*(.*)$',md,re.M)
    if m:kw=[x.strip() for x in m.group(1).split(',') if x.strip()]
    metaok=all(x in md for x in fields) and len(kw)==7
    first_pages='\n'.join(interior[i].get_text() for i in range(min(2,len(interior))))
    wraptext=wrap[0].get_text()
    identityok=(f'AUTHOR: {IMPRINT}' in md and IMPRINT in first_pages and IMPRINT.lower() in wraptext.lower() and not any(token in (first_pages+'\n'+md+'\n'+wraptext) for token in ('[Author / Imprint]','[yourdomain.example]','yourdomain.example','[URL]')))
    imgok=True
    for x in required[2:9]:
        try:
            im=Image.open(folder/x); w,h=im.size
            if w<900 or h<900:imgok=False
        except Exception:imgok=False
    check(inv and intok and wrapok and metaok and imgok and identityok,r['id'])
    print(f"{r['id']:<4} {r['cover_title'][:32]:<32} {len(interior):>4} {trim[0]:>4g}x{trim[1]:<4g} {'OK' if intok else 'NO':>3} {'OK' if wrapok else 'NO':>4} {'OK' if metaok else 'NO':>4} {'OK' if imgok else 'NO':>3}")

up=(R/'UPLOAD_CHECKLIST.md').read_text(encoding='utf-8')
check(len(re.findall(r'^## [AB]\d+',up,re.M))==18,'upload checklist must have 18 sections')
look=fitz.open(R/'LOOKBOOK.pdf')
check(len(look)==19,'lookbook must have title + 18 product pages')
check(all((R/x).exists() for x in ['MARKETING.md','LEGAL_AND_CLAIMS.md','00_START_HERE.md','RELEASE_POLICY.md','PORTFOLIO.md','WAVE1_HUMAN_QA.md','KDP_ACCOUNT_OPERATIONS.md','POLISH_NOTES.md','PREPUBLICATION_SEQUENCE.md','QR_AND_AUDIO.md','QR_AUDIO_REVIEW.md','TRADEMARK_SCREENING.md','DECISIONS.md']),'operating and release-control docs present')
check((R/'configure_wave1_qr.py').is_file() and (R/'qr-routing'/'worker.js').is_file(),'QR routing/stamp tooling present')
if DOMAIN:
    route_file=R/'qr-routing'/'routes.json'
    route_data=json.loads(route_file.read_text(encoding='utf-8')) if route_file.exists() else {}
    check(route_data.get('domain')==DOMAIN and len(route_data.get('routes',[]))==6,'configured QR route map has six candidate routes')
    check(all((R/'qr-routing'/'site'/'audio'/x).is_file() for x in ['A01-arrive.mp3','A04-soften.mp3','A05-harbor.mp3','B10-settle.mp3','B12-enough.mp3','B18-clarity.mp3']),'six Wave 1 draft audio files present')
    check(all((R/'qr-routing'/'site'/'listen'/x/'index.html').is_file() for x in ['arrive','soften','harbor','settle','enough','clarity']),'six Wave 1 candidate landing pages present')
print(f'\nChecks passed: {passed}/30')
if fails:
    print('FAILURES:', '; '.join(fails));sys.exit(1)
print('ALL 18 PRODUCTS: STRUCTURALLY COMPLETE — BRANDED INTERIORS, WRAPS, LISTING ASSETS, METADATA, CHECKLIST, LOOKBOOK')
