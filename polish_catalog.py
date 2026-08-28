#!/usr/bin/env python3
"""Second-pass art director: regenerate distinct premium cover/wrap/listing assets.

This layer leaves approved interiors untouched and makes the buyer-visible system more editorial:
custom serif typography, product-specific line motifs, meaningful format badges, a visible imprint,
and collection collage cards. Run after build_catalog.py; build_catalog also calls it automatically.
"""
from pathlib import Path
import csv, math, re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent;REL=ROOT/'release';FONTS=ROOT/'fonts';BLEED=.125;PPI=.002252
pdfmetrics.registerFont(TTFont('RitualSerif',str(FONTS/'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('RitualSerifBold',str(FONTS/'DejaVuSerif-Bold.ttf')))
pdfmetrics.registerFont(TTFont('RitualSans',str(FONTS/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('RitualSansBold',str(FONTS/'DejaVuSans-Bold.ttf')))

# A product receives one individual visual metaphor—not the same generic decoration across all covers.
DETAIL={
'A01':('square-breath','A WEEKLY CALM COMPANION'), 'A02':('petals','48 ORIGINAL CREATIVE PAUSES'), 'A03':('sun-calendar','12 UNDATED MONTHS'),
'A04':('soft-wave','90 DAYS OF KINDER SELF-TALK'), 'A05':('moon','84 BEDSIDE LANDING PAGES'), 'A06':('figure','24 SLOW SHAPE CUES'),
'A07':('signal','90 CALM-CHECK PAGES'), 'A08':('horizon','12 MONTHS · 48 WEEKS'), 'A09':('cards','54 SMALL PROMPTS INSIDE'),
'B10':('breath-waves','90 DAYS · NO STREAKS REQUIRED'), 'B11':('quilt','90 COZY BEDSIDE CHECK-INS'), 'B12':('stepping','84 LOW-CAPACITY DAILY PAGES'),
'B13':('radial','12 SESSION INTEGRATION CHAPTERS'), 'B14':('trees','40 OUTDOOR RETURNS'), 'B15':('mandala','42 COLOR-AND-CHECK-IN PAIRS'),
'B16':('overlap','52 SIDE-BY-SIDE CHECK-INS'), 'B17':('desk','60 MICRO-RESET PROMPTS'), 'B18':('rings','60 CALM-MONEY PRACTICES'),
}
BG={
'A01':'20313D','A02':'556B5E','A03':'9C6F48','A04':'49354A','A05':'172338','A06':'756359','A07':'4B6070','A08':'334A4D','A09':'314944',
'B10':'294A52','B11':'6C6860','B12':'35443A','B13':'51546A','B14':'385E50','B15':'744B54','B16':'68555B','B17':'4C6770','B18':'443C2B'}
AC={
'A01':'A4C3B2','A02':'E4C59A','A03':'EAD0AB','A04':'E3B4A5','A05':'C8CEE8','A06':'E4D1B8','A07':'BCD9D8','A08':'D1C389','A09':'D7AE86',
'B10':'A7D2D0','B11':'E1D7C8','B12':'D8B887','B13':'CED5E8','B14':'C9D9B3','B15':'E7C4BF','B16':'EACFB9','B17':'C3D8DC','B18':'E6C778'}

# text helpers
def p_lines(text,font,size,width):
 out=[];cur=''
 for word in text.split():
  t=(cur+' '+word).strip()
  if not cur or stringWidth(t,font,size)<=width:cur=t
  else:out.append(cur);cur=word
 if cur:out.append(cur)
 return out
def p_center(c,text,cx,y,font,size,color,width,lead):
 c.setFont(font,size);c.setFillColor(color);a=p_lines(text,font,size,width);top=y+(len(a)-1)*lead/2
 for i,line in enumerate(a):c.drawCentredString(cx,top-i*lead,line)
def p_left(c,text,x,y,font,size,color,width,lead):
 c.setFont(font,size);c.setFillColor(color)
 for line in p_lines(text,font,size,width):c.drawString(x,y,line);y-=lead
 return y

def pdf_motif(c,motif,cx,cy,s,accent):
 c.setStrokeColor(accent);c.setLineWidth(.9)
 if motif=='square-breath':
  z=s*.20
  for dx,dy in [(0,0),(1,0),(1,1),(0,1)]:c.rect(cx+(dx-.5)*z,cy+(dy-.5)*z,z,z,stroke=1,fill=0)
  c.roundRect(cx-.52*s,cy-.52*s,1.04*s,1.04*s,9,stroke=1,fill=0)
 elif motif=='petals':
  for i in range(12):
   a=2*math.pi*i/12;x=cx+math.cos(a)*s*.31;y=cy+math.sin(a)*s*.31;c.circle(x,y,s*.22,stroke=1,fill=0)
  c.circle(cx,cy,s*.13,stroke=1,fill=0)
 elif motif=='sun-calendar':
  c.circle(cx,cy,s*.23,stroke=1,fill=0)
  for i in range(12):
   a=2*math.pi*i/12;c.line(cx+math.cos(a)*s*.31,cy+math.sin(a)*s*.31,cx+math.cos(a)*s*.48,cy+math.sin(a)*s*.48)
  c.roundRect(cx-s*.52,cy-s*.52,s*1.04,s*1.04,8,stroke=1,fill=0)
 elif motif=='soft-wave':
  for j in range(3):
   p=c.beginPath();
   for i in range(61):
    x=cx-s*.62+i*s*1.24/60;y=cy+(j-1)*s*.17+math.sin(i/60*math.pi*2)*s*.11
    (p.moveTo if i==0 else p.lineTo)(x,y)
   c.drawPath(p,stroke=1,fill=0)
 elif motif=='moon':
  c.circle(cx,cy,s*.43,stroke=1,fill=0);c.setFillColor(colors.HexColor('#'+BG_CUR));c.circle(cx+s*.17,cy+s*.10,s*.43,stroke=0,fill=1)
  for i in range(9):
   a=2*math.pi*i/9;c.circle(cx+math.cos(a)*s*.62,cy+math.sin(a)*s*.62,s*.025,stroke=1,fill=0)
 elif motif=='figure':
  c.circle(cx,cy+s*.32,s*.09,stroke=1,fill=0);c.line(cx,cy+s*.23,cx,cy-.15*s);c.line(cx,cy+.1*s,cx-s*.32,cy);c.line(cx,cy+.1*s,cx+s*.32,cy);c.line(cx,cy-.15*s,cx-s*.25,cy-s*.42);c.line(cx,cy-.15*s,cx+s*.25,cy-s*.42);c.arc(cx-s*.55,cy-s*.55,cx+s*.55,cy+s*.55,210,120)
 elif motif=='signal':
  p=c.beginPath();
  for i in range(9):
   x=cx-s*.55+i*s*1.1/8;y=cy+(0 if i not in (3,4,5) else [-.12,.28,-.08][i-3])*s
   (p.moveTo if i==0 else p.lineTo)(x,y)
  c.drawPath(p,stroke=1,fill=0);c.circle(cx,cy,s*.58,stroke=1,fill=0)
 elif motif=='horizon':
  for i in range(4):c.line(cx-s*.58,cy+(i-1.5)*s*.20,cx+s*.58,cy+(i-1.5)*s*.20)
  c.arc(cx-s*.48,cy-s*.26,cx+s*.48,cy+s*.70,205,130)
 elif motif=='cards':
  for dx,dy,a in [(-.16,.12,-12),(0,0,0),(.16,-.12,12)]:
   c.saveState();c.translate(cx+dx*s,cy+dy*s);c.rotate(a);c.roundRect(-s*.27,-s*.37,s*.54,s*.74,7,stroke=1,fill=0);c.restoreState()
 elif motif=='breath-waves':
  for j in range(5):
   p=c.beginPath()
   for i in range(51):
    x=cx-s*.62+i*s*1.24/50;y=cy+(j-2)*s*.14+math.sin((i/50*2*math.pi)+(j*.7))*s*.08
    (p.moveTo if i==0 else p.lineTo)(x,y)
   c.drawPath(p,stroke=1,fill=0)
 elif motif=='quilt':
  for x in range(4):
   for y in range(4):c.roundRect(cx-s*.46+x*s*.23,cy-s*.46+y*s*.23,s*.19,s*.19,4,stroke=1,fill=0)
 elif motif=='stepping':
  for i in range(5):c.roundRect(cx-s*.48+i*s*.20,cy-s*.38+i*s*.16,s*.17,s*.17,3,stroke=1,fill=0)
  c.line(cx-s*.5,cy-s*.43,cx+s*.48,cy+s*.43)
 elif motif=='radial':
  for r in [.18,.36,.54]:c.circle(cx,cy,s*r,stroke=1,fill=0)
  for i in range(16):
   a=2*math.pi*i/16;c.line(cx+math.cos(a)*s*.18,cy+math.sin(a)*s*.18,cx+math.cos(a)*s*.60,cy+math.sin(a)*s*.60)
 elif motif=='trees':
  c.line(cx,cy-s*.48,cx,cy+s*.43)
  for dx,dy in [(-.4,-.05),(.42,.08),(-.33,.26),(.34,.38),(-.2,.5)]:c.line(cx,cy+dy*s,cx+dx*s,cy+(dy+.24)*s)
  for x in [-.4,-.2,0,.2,.4]:c.circle(cx+x*s,cy+s*.53-abs(x)*s*.12,s*.12,stroke=1,fill=0)
 elif motif=='mandala':
  for r in [.2,.38,.56]:c.circle(cx,cy,s*r,stroke=1,fill=0)
  for i in range(16):
   a=2*math.pi*i/16;c.circle(cx+math.cos(a)*s*.46,cy+math.sin(a)*s*.46,s*.11,stroke=1,fill=0)
 elif motif=='overlap':
  c.circle(cx-s*.18,cy,s*.38,stroke=1,fill=0);c.circle(cx+s*.18,cy,s*.38,stroke=1,fill=0);c.circle(cx,cy+s*.03,s*.15,stroke=1,fill=0)
 elif motif=='desk':
  c.roundRect(cx-s*.5,cy-s*.31,s,s*.62,6,stroke=1,fill=0)
  for i in range(4):c.line(cx-s*.38,cy+s*.16-i*s*.13,cx+s*.38,cy+s*.16-i*s*.13)
  c.line(cx-s*.38,cy-s*.47,cx+s*.38,cy-s*.47)
 elif motif=='rings':
  for r in [.17,.34,.51]:c.circle(cx,cy,s*r,stroke=1,fill=0)
  c.arc(cx-s*.67,cy-s*.67,cx+s*.67,cy+s*.67,35,105)

def img_motif(draw,motif,cx,cy,s,accent,bg):
 # use high-level PIL analogs—slightly bolder to read in thumbnail.
 w=4
 if motif=='square-breath':
  z=int(s*.20)
  for dx,dy in [(0,0),(1,0),(1,1),(0,1)]:draw.rectangle((cx+(dx-.5)*z,cy+(dy-.5)*z,cx+(dx+.5)*z,cy+(dy+.5)*z),outline=accent,width=w)
  draw.rounded_rectangle((cx-s*.52,cy-s*.52,cx+s*.52,cy+s*.52),15,outline=accent,width=w)
 elif motif in ('petals','mandala'):
  n=12 if motif=='petals' else 16
  for i in range(n):
   a=2*math.pi*i/n;r=s*(.31 if motif=='petals' else .46);rr=s*(.22 if motif=='petals' else .11);x=cx+math.cos(a)*r;y=cy+math.sin(a)*r;draw.ellipse((x-rr,y-rr,x+rr,y+rr),outline=accent,width=w)
  for r in ([.13] if motif=='petals' else [.2,.38,.56]):draw.ellipse((cx-s*r,cy-s*r,cx+s*r,cy+s*r),outline=accent,width=w)
 elif motif=='sun-calendar':
  draw.ellipse((cx-s*.23,cy-s*.23,cx+s*.23,cy+s*.23),outline=accent,width=w);draw.rounded_rectangle((cx-s*.52,cy-s*.52,cx+s*.52,cy+s*.52),15,outline=accent,width=w)
  for i in range(12):
   a=2*math.pi*i/12;draw.line((cx+math.cos(a)*s*.31,cy+math.sin(a)*s*.31,cx+math.cos(a)*s*.48,cy+math.sin(a)*s*.48),fill=accent,width=w)
 elif motif in ('soft-wave','breath-waves'):
  count=3 if motif=='soft-wave' else 5
  for j in range(count):
   pts=[]
   for i in range(60):pts.append((cx-s*.62+i*s*1.24/59,cy+(j-(count-1)/2)*s*.14+math.sin(i/59*math.pi*2+j*.7)*s*.08))
   draw.line(pts,fill=accent,width=w)
 elif motif=='moon':
  draw.ellipse((cx-s*.43,cy-s*.43,cx+s*.43,cy+s*.43),outline=accent,width=w);draw.ellipse((cx-s*.26,cy-s*.33,cx+s*.60,cy+s*.53),fill=bg)
 elif motif=='figure':
  draw.ellipse((cx-s*.09,cy+s*.23,cx+s*.09,cy+s*.41),outline=accent,width=w);draw.line((cx,cy+s*.23,cx,cy-s*.15),fill=accent,width=w);draw.line((cx,cy+s*.1,cx-s*.32,cy),fill=accent,width=w);draw.line((cx,cy+s*.1,cx+s*.32,cy),fill=accent,width=w);draw.line((cx,cy-s*.15,cx-s*.25,cy-s*.42),fill=accent,width=w);draw.line((cx,cy-s*.15,cx+s*.25,cy-s*.42),fill=accent,width=w)
 elif motif=='signal':
  pts=[(cx-s*.55,cy),(cx-s*.3,cy),(cx-s*.12,cy),(cx,cy-s*.12),(cx+s*.1,cy+s*.28),(cx+s*.18,cy-s*.08),(cx+s*.55,cy)];draw.line(pts,fill=accent,width=w);draw.ellipse((cx-s*.58,cy-s*.58,cx+s*.58,cy+s*.58),outline=accent,width=w)
 elif motif=='horizon':
  for i in range(4):draw.line((cx-s*.58,cy+(i-1.5)*s*.20,cx+s*.58,cy+(i-1.5)*s*.20),fill=accent,width=w)
  draw.arc((cx-s*.48,cy-s*.26,cx+s*.48,cy+s*.70),205,335,fill=accent,width=w)
 elif motif=='cards':
  for dx,dy in [(-.16,.12),(0,0),(.16,-.12)]:draw.rounded_rectangle((cx+(dx-.27)*s,cy+(dy-.37)*s,cx+(dx+.27)*s,cy+(dy+.37)*s),9,outline=accent,width=w)
 elif motif=='quilt':
  for x in range(4):
   for y in range(4):draw.rounded_rectangle((cx-s*.46+x*s*.23,cy-s*.46+y*s*.23,cx-s*.27+x*s*.23,cy-s*.27+y*s*.23),5,outline=accent,width=w)
 elif motif=='stepping':
  for i in range(5):draw.rounded_rectangle((cx-s*.48+i*s*.20,cy-s*.38+i*s*.16,cx-s*.31+i*s*.20,cy-s*.21+i*s*.16),4,outline=accent,width=w)
 elif motif=='radial':
  for r in [.18,.36,.54]:draw.ellipse((cx-s*r,cy-s*r,cx+s*r,cy+s*r),outline=accent,width=w)
  for i in range(16):
   a=2*math.pi*i/16;draw.line((cx+math.cos(a)*s*.18,cy+math.sin(a)*s*.18,cx+math.cos(a)*s*.60,cy+math.sin(a)*s*.60),fill=accent,width=w)
 elif motif=='trees':
  draw.line((cx,cy-s*.48,cx,cy+s*.43),fill=accent,width=w)
  for x in [-.4,-.2,0,.2,.4]:draw.ellipse((cx+x*s-s*.12,cy+s*.53-abs(x)*s*.12-s*.12,cx+x*s+s*.12,cy+s*.53-abs(x)*s*.12+s*.12),outline=accent,width=w)
 elif motif=='overlap':
  draw.ellipse((cx-s*.56,cy-s*.38,cx+s*.20,cy+s*.38),outline=accent,width=w);draw.ellipse((cx-s*.20,cy-s*.38,cx+s*.56,cy+s*.38),outline=accent,width=w)
 elif motif=='desk':
  draw.rounded_rectangle((cx-s*.5,cy-s*.31,cx+s*.5,cy+s*.31),8,outline=accent,width=w)
  for i in range(4):draw.line((cx-s*.38,cy+s*.16-i*s*.13,cx+s*.38,cy+s*.16-i*s*.13),fill=accent,width=w)
 elif motif=='rings':
  for r in [.17,.34,.51]:draw.ellipse((cx-s*r,cy-s*r,cx+s*r,cy+s*r),outline=accent,width=w)

def ipath(size,bold=False):
 return FONTS/('DejaVuSerif-Bold.ttf' if bold else 'DejaVuSerif.ttf')
def img_font(size,bold=False):return ImageFont.truetype(str(ipath(size,bold)),size)
def sans(size,bold=False):return ImageFont.truetype(str(FONTS/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
def wrap_img(draw,text,f,w):
 words=text.split();out=[];cur=''
 for word in words:
  t=(cur+' '+word).strip()
  if not cur or draw.textbbox((0,0),t,font=f)[2]<=w:cur=t
  else:out.append(cur);cur=word
 if cur:out.append(cur)
 return out
def center_img(draw,text,x,y,f,fill,w,lead):
 ls=wrap_img(draw,text,f,w);top=y-(len(ls)-1)*lead/2
 for i,l in enumerate(ls):draw.text((x,top+i*lead),l,font=f,fill=fill,anchor='mm')

def make_wrap(row):
 global BG_CUR
 ident=row['id'];tw,th=map(float,row['trim'].split('x'));pages=int(row['pages']);spine=pages*PPI;ww=2*BLEED+2*tw+spine;hh=2*BLEED+th;W,H=ww*inch,hh*inch;folder=ROOT/row['folder'];motif,badge=DETAIL[ident];bg=colors.HexColor('#'+BG[ident]);accent=colors.HexColor('#'+AC[ident]);BG_CUR=BG[ident]
 md=(folder/'metadata.txt').read_text(encoding='utf-8'); match=re.search(r'DESCRIPTION:\n(.*?)\n\nCLAIMS',md,re.S); description=match.group(1).strip() if match else row['subtitle']
 c=canvas.Canvas(str(folder/'cover_wrap.pdf'),pagesize=(W,H),pageCompression=1);c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0)
 # grid and product motif occur only in the front; back stays readable.
 fx=(BLEED+tw+spine)*inch;cx=fx+tw*inch/2
 c.setStrokeColor(colors.Color(1,1,1,.11));c.setLineWidth(.35)
 for r in range(5):c.line(fx+.35*inch,(1.0+r*1.25)*inch,fx+tw*inch-.35*inch,(1.0+r*1.25)*inch)
 pdf_motif(c,motif,cx,H*.74,1.08*inch,accent)
 c.setStrokeColor(accent);c.setLineWidth(.75);c.line(fx+.72*inch,H*.54,fx+tw*inch-.72*inch,H*.54)
 p_center(c,row['cover_title'].upper(),cx,H*.43,'RitualSerif',22,colors.white,tw*inch-1.0*inch,27)
 p_center(c,row['subtitle'],cx,H*.32,'RitualSans',8.9,accent,tw*inch-1.05*inch,12)
 # signature badge
 bw=tw*inch-1.10*inch;bh=.25*inch;bx=fx+.55*inch;by=.58*inch;c.setFillColor(colors.white);c.roundRect(bx,by,bw,bh,8,fill=1,stroke=0);c.setFillColor(bg);c.setFont('RitualSansBold',5.6);c.drawCentredString(bx+bw/2,by+.085*inch,badge)
 c.setFillColor(accent);c.setFont('RitualSans',5.8);c.drawCentredString(cx,.30*inch,'THE RITUAL LIBRARY')
 # back
 bx=BLEED*inch+.38*inch;c.setFillColor(accent);c.setFont('RitualSansBold',6.8);c.drawString(bx,H*.68,row['collection'].upper());c.setFillColor(colors.white);c.setFont('RitualSerif',14);c.drawString(bx,H*.61,'A small ritual for real life.')
 p_left(c,description,bx,H*.52,'RitualSans',7.5,colors.white,tw*inch-.75*inch,9.5)
 c.setStrokeColor(accent);c.setLineWidth(.55);c.line(bx,H*.26,bx+tw*inch-.75*inch,H*.26);c.setFont('RitualSans',5.6);c.setFillColor(accent);c.drawString(bx,H*.20,'UNDATED · DESIGNED FOR PERSONAL REFLECTION')
 # no-print barcode reserve
 c.setFillColor(colors.white);c.rect(.34*inch,.33*inch,2*inch,1.2*inch,fill=1,stroke=0);c.setFillColor(bg);c.setFont('RitualSans',4.9);c.drawCentredString(1.34*inch,.25*inch,'BARCODE KEEP-CLEAR AREA')
 # spine
 sx=(BLEED+tw)*inch
 if spine>=.18:
  c.saveState();c.translate(sx+spine*inch/2,.35*inch);c.rotate(90);c.setFillColor(colors.white);c.setFont('RitualSansBold',max(4,min(6.5,spine*26)));c.drawCentredString(th*inch/2,0,row['cover_title'].upper());c.restoreState()
 c.save()

def make_front(row):
 ident=row['id'];motif,badge=DETAIL[ident];W,H=1800,2700;bg='#'+BG[ident];accent='#'+AC[ident];im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
 # editorial hairlines
 for i in range(5):d.line((150,430+i*125,W-150,430+i*125),fill=tuple(int(bg[j:j+2],16)+18 if int(bg[j:j+2],16)<230 else 240 for j in (1,3,5)),width=2)
 img_motif(d,motif,W//2,720,430,accent,bg)
 d.line((200,1240,W-200,1240),fill=accent,width=3)
 center_img(d,row['cover_title'].upper(),W//2,1460,img_font(92), '#FFFFFF',W-220,118)
 center_img(d,row['subtitle'],W//2,1780,sans(33),accent,W-300,48)
 # badge
 bbox=(230,2240,W-230,2315);d.rounded_rectangle(bbox,37,fill='#FFFFFF');d.text((W//2,2278),badge,font=sans(21,True),fill=bg,anchor='mm')
 d.text((W//2,2520),'THE RITUAL LIBRARY',font=sans(20),fill=accent,anchor='mm')
 im.save(ROOT/row['folder']/'cover.jpg',quality=95)

def callout(row):
 ident=row['id'];motif,badge=DETAIL[ident];W,H=1800,1350;bg='#'+BG[ident];accent='#'+AC[ident];im=Image.new('RGB',(W,H),'#F7F3EC');d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,315),fill=bg);img_motif(d,motif,1450,155,165,accent,bg);d.text((95,105),row['cover_title'].upper(),font=img_font(55),fill='#FFFFFF');d.text((95,205),badge,font=sans(24,True),fill=accent)
 trims=row['trim'].replace('x',' × ')+' in.'; stats=[('FORMAT',trims),('PAGES',row['pages']),('INTERIOR','B&W · WHITE'),('SCOUT PRICE',row['price'])]
 for i,(a,b) in enumerate(stats):
  x=100+(i%2)*850;y=450+(i//2)*285;d.rounded_rectangle((x,y,x+740,y+195),24,fill='#FFFFFF',outline=accent,width=4);d.text((x+38,y+43),a,font=sans(22,True),fill=bg);d.text((x+38,y+110),b,font=sans(35),fill='#222222')
 d.text((95,1215),'A complete paperback scout edition. Deluxe materials are never implied where they are not included.',font=sans(19),fill='#555555')
 im.save(ROOT/row['folder']/'listing_06_callout.jpg',quality=95)

def series_cards(rows):
 for collection in sorted({r['collection'] for r in rows}):
  picks=[r for r in rows if r['collection']==collection];W,H=1800,1350;bg='#20313D' if collection=='Pace & Progress' else '#35443A';accent='#A4C3B2' if collection=='Pace & Progress' else '#D8B887';im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
  d.text((W//2,105),'THE RITUAL LIBRARY',font=sans(24,True),fill=accent,anchor='mm');d.text((W//2,195),collection,font=img_font(65),fill='#FFFFFF',anchor='mm')
  # nine visible cover thumbnails, deliberately varied colors
  for i,row in enumerate(picks):
   thumb=Image.open(ROOT/row['folder']/'cover.jpg');thumb.thumbnail((220,330));x=100+i*185;y=395+(i%2)*50;im.paste(thumb,(x,y))
  d.text((W//2,1170),'A collection of quiet, tactile tools for real life',font=sans(28),fill=accent,anchor='mm');d.text((W//2,1220),'notice · soothe · continue',font=sans(20),fill='#FFFFFF',anchor='mm')
  for row in picks:im.save(ROOT/row['folder']/'listing_07_series.jpg',quality=95)

def main():
 rows=list(csv.DictReader((ROOT/'CATALOG.csv').open(encoding='utf-8')))
 for row in rows:make_wrap(row);make_front(row);callout(row)
 series_cards(rows)
 print('Polished 18 covers, wraps, callouts, and collection cards.')
if __name__=='__main__':main()
