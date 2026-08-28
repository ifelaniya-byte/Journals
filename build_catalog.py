"""Repository build harness for the 18-product Ritual Library KDP scout catalog.

Generates the 11 additional KDP scout packages, assembles the seven existing full scouts,
creates all listing assets, documentation, lookbook, metadata, and validates output through
validate_catalog.py. Requires: reportlab, Pillow, PyMuPDF.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image, ImageDraw, ImageFont
import fitz, shutil, csv, math, calendar, textwrap, json

ROOT=Path(__file__).resolve().parent
BRAND=json.loads((ROOT/'brand_config.json').read_text(encoding='utf-8'))
IMPRINT=BRAND['imprint']
RELEASE=ROOT/'release'
DELUXE=ROOT/'deluxe-heroes'
for d in (ROOT,RELEASE,DELUXE):d.mkdir(parents=True,exist_ok=True)

# Shared KDP formulas and visual system
BLEED=.125
PPI=0.002252 # white-paper B&W KDP paperback spine formula — validate against current KDP template before upload
INK=colors.Color(.14,.14,.14); MID=colors.Color(.38,.38,.38); LIGHT=colors.Color(.72,.72,.72); FAINT=colors.Color(.90,.90,.90)
COLORS={
'A01':'20313D','A02':'556B5E','A03':'9C6F48','A04':'49354A','A05':'172338','A06':'756359','A07':'4B6070','A08':'334A4D','A09':'314944',
'B10':'294A52','B11':'6C6860','B12':'35443A','B13':'51546A','B14':'385E50','B15':'744B54','B16':'68555B','B17':'4C6770','B18':'443C2B'}
ACCENTS={
'A01':'A4C3B2','A02':'E4C59A','A03':'EAD0AB','A04':'E3B4A5','A05':'C8CEE8','A06':'E4D1B8','A07':'BCD9D8','A08':'D1C389','A09':'D7AE86',
'B10':'A7D2D0','B11':'E1D7C8','B12':'D8B887','B13':'CED5E8','B14':'C9D9B3','B15':'E7C4BF','B16':'EACFB9','B17':'C3D8DC','B18':'E6C778'}

PRODUCTS=[
# id, slug, collection, cover, amazon title, subtitle, trim, pages, paper, price, kind, description, kws, categories, boundary
('A01','dose-and-breathe','Pace & Progress','Dose & Breathe','Dose & Breathe: A Mindful Weekly GLP-1 Companion','A mindful weekly companion for your GLP-1 journey',(6,8),128,'white',14.99,'existing','A discreet weekly reflection book for adults using prescribed GLP-1 medication. Optional routine notes, a simple breath visual, and gentle space for comfort, support, and care-team questions.','GLP-1 journal|mindful wellness journal|weekly reflection journal|self compassion tracker|medication routine companion|calming journal|health journey notebook','Self-Help / Journaling|Health & Fitness / Healthy Living','No dosing, injection, weight-loss, symptom-relief, or treatment promises. Legal/healthcare marketing review required.'),
('A02','color-your-way-forward','Pace & Progress','Color Your Way Forward','Color Your Way Forward: A Mindful GLP-1 Coloring Workbook','Healthy rituals, calm scenes, and room to reflect',(8.5,11),100,'white',14.99,'coloring','A single-sided coloring workbook with calming everyday scenes, gentle reflection cues, and room for a low-pressure weekly check-in.','GLP-1 coloring book|adult wellness coloring|mindful coloring journal|healthy habits coloring|stress relief coloring|weight journey journal|calm creative workbook','Crafts & Hobbies / Coloring Books|Self-Help / Journaling','No weight-loss or therapeutic art claims. Use only cleared GLP-1 customer-facing language.'),
('A03','scent-of-a-steady-year','Pace & Progress','The Scent of a Steady Year','The Scent of a Steady Year: An Undated GLP-1 Ritual Calendar','Twelve months of gentle planning and sensory cues',(8.5,11),120,'white',14.99,'calendar','An undated twelve-month planning journal with roomy calendar grids, sensory-inspired prompts, and optional personal-routine reflection.','GLP-1 planner|wellness calendar undated|self care calendar|mindful year planner|health journey organizer|ritual planner|wellness journal','Self-Help / Journaling|Health & Fitness / Healthy Living','Paperback edition contains visual sensory cues only—no fragrance, medical, or weight-loss claims.'),
('A04','softer-words','Pace & Progress','Softer Words','Softer Words: A Gratitude & Self-Talk Diary','A gentle daily reflection practice for ordinary hard days',(6,8),128,'white',14.99,'existing','An undated gratitude and self-talk diary for the ordinary hard days, with brief prompts that make room for what felt difficult, what you did with care, and a kinder sentence to carry forward.','self compassion journal|gratitude diary|positive self talk journal|gentle daily journal|mindful reflection|kindness journal|gift journal','Self-Help / Journaling|Self-Help / Personal Growth','Personal reflection only; not therapy or treatment for anxiety, depression, or other conditions.'),
('A05','night-harbor','Pace & Progress','Night Harbor','Night Harbor: An Evening Wind-Down & Sleep Reflection Companion','A bedside landing place for setting down the day',(6,8),168,'white',14.99,'existing','A quiet evening wind-down and morning reflection companion with brief prompts for setting down the day, choosing comfort, noticing patterns, and approaching tomorrow gently.','sleep journal|bedtime journal|evening reflection|wind down routine|night journal|gentle self care gift|bedside notebook','Self-Help / Journaling|Self-Help / Stress Management','Not a sleep-treatment product and does not diagnose or treat sleep conditions.'),
('A06','stillness-and-stretch','Pace & Progress','Stillness & Stretch','Stillness & Stretch: A Gentle Movement Reflection Companion','Slow shapes, body-scan pages, and permission to pause',(8,10),128,'white',15.99,'movement','A gentle movement reflection companion with simple illustrated shape cues, body-scan pages, and undated practice planning.','gentle movement journal|yin inspired journal|body scan reflection|slow stretch planner|mindful movement|wellness practice journal|restorative routine','Health & Fitness / Exercise|Self-Help / Journaling','Not exercise instruction or medical advice. Do not make post-injection safety claims; have movement copy reviewed.'),
('A07','steady-signal','Pace & Progress','Steady Signal','Steady Signal: A Calm-Check & Optional Pulse Observation Journal','Notice signals without turning them into a verdict',(6,8),120,'white',14.99,'signal','A personal observation journal for noticing sensations, optional resting-pulse notes, grounding attempts, and questions to raise with a care professional.','calm check journal|anxiety reflection journal|body signal tracker|grounding journal|wellness observation|pulse notes journal|self care tracker','Self-Help / Journaling|Self-Help / Stress Management','Not a medical device or diagnostic tool. Do not claim that pulse readings detect anxiety; include urgent-care language in final review.'),
('A08','unhurried-year','Pace & Progress','The Unhurried Year','The Unhurried Year: An Undated Executive Wellness Planner','A capacity-respecting year for work, care, and real life',(7,9),160,'white',15.99,'planner','An undated executive-style planner with month views, weekly priorities, capacity check-ins, and private routine space.','undated wellness planner|executive self care planner|capacity planning journal|professional wellness planner|mindful weekly planner|self care organizer|year planner','Self-Help / Journaling|Business & Money / Time Management','General planning tool only. Avoid medical or weight-loss outcomes; use private routine wording.'),
('A09','pocket-of-calm-companion','Stillwork Editions','Pocket of Calm','Pocket of Calm: A Guided Journaling Companion','Fifty-four small prompts for the moments a blank page is too much',(6,8),120,'white',14.99,'existing','A stand-alone companion with 54 gentle prompts organized into arrive, soften, nourish, reach, continue, and reset.','journaling prompts|mindfulness journal|self reflection book|calming gift|stress relief journal|prompt journal|gentle wellness','Self-Help / Journaling|Self-Help / Personal Growth','Current scout is collection-neutral. Do not label GLP-1-specific unless copy and claims receive a separate review.'),
('B10','rest-and-regulate','Stillwork Editions','Rest & Regulate','Rest & Regulate: A 90-Day Breath-Paced Planner','Small returns to the present, without performance metrics',(6,8),144,'white',14.99,'existing','A ninety-day reflection planner built around optional grounding and paced-breathing practices, with room to notice what supports you.','breathwork journal|grounding practice planner|90 day mindfulness journal|stress relief journal|nervous system journal|daily reflection|calming planner','Self-Help / Journaling|Self-Help / Stress Management','Do not claim vagus stimulation, anxiety treatment, HRV improvement, or physiological outcomes.'),
('B11','under-the-covers','Stillwork Editions','Under the Covers','Under the Covers: A Weighted-Blanket Sleep & Stress Diary','A cozy, specific bedside reflection practice',(7,9),120,'white',14.99,'weighted','A bedside diary for recording personal comfort, room feel, settling rituals, and morning impressions around a weighted-blanket routine.','weighted blanket journal|sleep diary|bedtime comfort journal|stress reflection|cozy sleep planner|sleep environment log|night routine journal','Self-Help / Journaling|Self-Help / Stress Management','Do not recommend blanket weights or claim treatment for anxiety/insomnia. Include a final weighted-blanket safety note.'),
('B12','back-to-enough','Stillwork Editions','Back to Enough','Back to Enough: A Compassionate Productivity Rescue Workbook','Make the plan smaller until it becomes possible',(6,8),160,'white',15.99,'existing','A compassionate productivity rescue workbook for low-capacity days, featuring task triage, capacity checks, mini-break planning, and weekly resets.','burnout workbook|compassionate productivity planner|task triage planner|overwhelm journal|recovery planning|self care workbook|low capacity planner','Self-Help / Journaling|Self-Help / Stress Management','Planning/reflection support only; not a diagnosis or treatment for burnout, anxiety, depression, or workplace harm.'),
('B13','breathwork-integration','Stillwork Editions','Breathwork Integration','The Breathwork Integration Book: A Session Reflection Log','Preparation, integration, and a place to make meaning',(8.27,11.69),128,'white',15.99,'integration','A session reflection log with intention, setting, sensory memory, mandala sketch, and integration-planning pages.','breathwork journal|session integration journal|mandala reflection|breathwork log|integration notebook|wellness workshop journal|mindful session notes','Self-Help / Journaling|Self-Help / Personal Growth','Not a guide to intense breathwork and not a substitute for qualified facilitation or clinical care. Do not use restricted trademarked method names.'),
('B14','among-the-trees','Stillwork Editions','Among the Trees','Among the Trees: A Forest-Bathing Photo Reflection Journal','Slow outdoor attention, season by season',(8,8),128,'white',15.99,'forest','A nature reflection journal with five-senses prompts, room for photographs or found paper, seasonal returns, and restorative-place notes.','forest bathing journal|nature reflection journal|shinrin yoku journal|outdoor mindfulness|photo journal nature|nature walk notebook|gift for hikers','Self-Help / Journaling|Nature & Wildlife / Outdoor Skills','Personal reflection product only; do not promise therapeutic or medical outcomes from time outdoors.'),
('B15','color-and-check-in','Stillwork Editions','Color & Check In','Color & Check In: A Mandala Coloring & Mood Diary','Creative pauses and a place to notice what shifts',(8.5,11),120,'white',15.99,'moodcolor','A coloring and mood-reflection book with original line-art mandalas, color notes, and spacious personal check-ins.','mandala coloring journal|mood diary coloring|stress relief coloring journal|adult coloring workbook|creative self care|mindful coloring|mood reflection','Crafts & Hobbies / Coloring Books|Self-Help / Journaling','Use “creative stress-relief practice,” not art therapy or treatment claims.'),
('B16','us-in-balance','Stillwork Editions','Us, In Balance','Us, In Balance: A Couples’ Pause & Repair Workbook','Side-by-side check-ins for two people under stress',(7,9),160,'white',15.99,'couples','A shared reflection workbook with optional me/you/us check-ins, repair conversations, support requests, and weekly rituals.','couples journal|relationship workbook|communication journal|couples check in|emotional regulation journal|partner reflection|relationship gift','Self-Help / Journaling|Family & Relationships / Love & Romance','Not couples therapy. Include a discreet resource page and do not position for coercive or abusive relationships.'),
('B17','one-minute-at-my-desk','Stillwork Editions','One Minute at My Desk','One Minute at My Desk: A Micro-Meditation & Reflection Book','Sixty small desk resets for full days',(5,7),120,'white',12.99,'desk','A compact collection of sixty 30–90 second desk-reset prompts with micro-journal pages for before, after, and next.','desk meditation book|micro mindfulness journal|one minute reset|office self care|work stress journal|desk wellness gift|short meditation prompts','Self-Help / Journaling|Business & Money / Time Management','General reflection only. Do not make medical, therapeutic, or workplace-performance claims.'),
('B18','enough-money-enough-calm','Stillwork Editions','Enough Money, Enough Calm','Enough Money, Enough Calm: A Financial-Anxiety Mindset Workbook','Facts, feelings, and one manageable next step',(6,8),168,'white',14.99,'existing','An emotion-forward reflection workbook for money moments that separates facts, feelings, and a manageable next step.','money anxiety journal|financial mindset workbook|money reflection journal|financial wellness journal|calm money planner|self reflection|money feelings journal','Self-Help / Journaling|Business & Money / Personal Finance','No financial, legal, tax, investment, or mental-health advice or outcome promises.'),
]
P={x[1]:x for x in PRODUCTS}

# Release state is intentionally separate from build state. An asset can be complete and still be held.
RELEASE_STATE={
 'A01':('Wave 1','HOLD — awaiting release gates','KDP paperback + price-visible waitlist','Required GLP-1/claims/name review, human QA, KDP Previewer, proof'),
 'A02':('Wave 2','HOLD','Future book/creative test','Signed open-slot decision and review'),
 'A03':('Wave 2','HOLD — digital-first','Etsy undated calendar','Digital demand signal; paperback is not primary test'),
 'A04':('Wave 1','HOLD — awaiting release gates','KDP paperback','Human QA, general claims/name review, KDP Previewer, proof'),
 'A05':('Wave 1','HOLD — awaiting release gates','KDP paperback','Human QA, sleep-adjacent review, KDP Previewer, proof'),
 'A06':('Wave 2','HOLD — review-heavy','Future movement-reflection test','Movement/health review and signed open slot'),
 'A07':('Wave 2','HOLD — review-heavy','Future non-device observation test','Clinical/claims review and signed open slot'),
 'A08':('Wave 2','HOLD — waitlist-first','$28–30 waitlist','25%+ conversion AND 400+ email leads'),
 'A09':('Vault','DO NOT PUBLISH TO KDP','Paid digital card sample + waitlist/presale','Neutral boxed-deck test; KDP companion is reference only'),
 'B10':('Wave 1','HOLD — awaiting release gates','KDP paperback','Human QA, breathwork/claims review, KDP Previewer, proof'),
 'B11':('Wave 2','HOLD — review-heavy','Future comfort-diary test','Sleep/blanket review and signed open slot'),
 'B12':('Wave 1','HOLD — awaiting release gates','KDP paperback','Human QA, burnout claims review, KDP Previewer, proof'),
 'B13':('Wave 2','HOLD — review-heavy','Future practitioner/creator test','Facilitation/naming/safety review and signed open slot'),
 'B14':('Wave 2','HOLD','Future visual retail/Etsy test','Paid visual/gift demand signal and open slot'),
 'B15':('Wave 2','HOLD','Future coloring demand test','Distinct creative hypothesis and claims review'),
 'B16':('Wave 2','HOLD — review-heavy','Future relationship-audience test','Safety/resource review and signed open slot'),
 'B17':('Vault','DO NOT PUBLISH TO KDP','Paid digital desk-practice sample','Physical easel/pad test; book form is reference only'),
 'B18':('Wave 1','HOLD — awaiting release gates','KDP paperback','Human QA, financial boundary review, KDP Previewer, proof'),
}

# PDF helpers
class Book:
 def __init__(self,path,trim,title,subtitle):
  self.path=path;self.w,self.h=trim[0]*inch,trim[1]*inch;self.c=canvas.Canvas(str(path),pagesize=(self.w,self.h),pageCompression=1);self.title=title;self.subtitle=subtitle;self.n=0;self.mx=.52*inch
 def frame(self,section='THE RITUAL LIBRARY',num=True):
  c=self.c;c.setFillColor(colors.white);c.rect(0,0,self.w,self.h,fill=1,stroke=0);c.setStrokeColor(FAINT);c.setLineWidth(.35);c.line(self.mx,self.h-.48*inch,self.w-self.mx,self.h-.48*inch);c.setFont('Helvetica',6.8);c.setFillColor(MID);c.drawString(self.mx,self.h-.39*inch,section.upper())
  if num and self.n>0:c.drawRightString(self.w-self.mx,.33*inch,str(self.n+1))
  c.line(self.mx,.45*inch,self.w-self.mx,.45*inch)
 def end(self):self.c.showPage();self.n+=1
 def title_page(self,ident):
  c=self.c;bg=colors.HexColor('#'+COLORS[ident]);ac=colors.HexColor('#'+ACCENTS[ident]);c.setFillColor(bg);c.rect(0,0,self.w,self.h,fill=1,stroke=0);c.setStrokeColor(ac);c.setLineWidth(1.1)
  for rr in [1.05,1.42,1.79]:c.circle(self.w*.75,self.h*.76,rr*inch,stroke=1,fill=0)
  centred(c,self.title,self.w/2,self.h*.57,22,colors.white,'Helvetica-Bold',self.w-1.05*inch,26);centred(c,self.subtitle,self.w/2,self.h*.46,10.4,colors.HexColor('#'+ACCENTS[ident]),'Helvetica',self.w-1.1*inch,13)
  c.setFillColor(colors.white);c.setFont('Helvetica',8.5);c.drawCentredString(self.w/2,self.h*.2,IMPRINT);c.setFillColor(colors.HexColor('#'+ACCENTS[ident]));c.setFont('Helvetica',6.5);c.drawCentredString(self.w/2,.38*inch,'THE RITUAL LIBRARY');self.end()
 def copyright(self,boundary):
  self.frame('Before you begin',False);c=self.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(self.mx,self.h-.86*inch,'A note before you begin');y=self.h-1.15*inch;y=para(c,boundary,self.mx,y,self.w-2*self.mx,9.5,12.5,INK);y-=.25*inch;y=para(c,'This is a personal reflection product. Use only the pages that help. Finalize the named imprint, exact QR/audio route, and all release gates before publication.',self.mx,y,self.w-2*self.mx,8.5,11,MID);self.end()
 def notes(self,title='Open notes',prompt='This page is yours.',section='Notes',lines=17):
  self.frame(section);c=self.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(self.mx,self.h-.82*inch,title);c.setFont('Helvetica-Oblique',8.3);c.setFillColor(MID);c.drawString(self.mx,self.h-1.03*inch,prompt);y=self.h-1.35*inch;c.setStrokeColor(FAINT)
  for _ in range(lines):c.line(self.mx,y,self.w-self.mx,y);y-=.28*inch
  self.end()

def lines(text,font,size,width):
 out=[];cur=''
 for word in text.replace('\n',' \n ').split():
  if word=='\\n':out.append(cur);cur='';continue
  t=(cur+' '+word).strip()
  if not cur or stringWidth(t,font,size)<=width:cur=t
  else:out.append(cur);cur=word
 if cur:out.append(cur)
 return out
def para(c,text,x,y,width,size=9.5,leading=12,color=INK,font='Helvetica'):
 c.setFont(font,size);c.setFillColor(color)
 for z in lines(text,font,size,width):c.drawString(x,y,z);y-=leading
 return y
def centred(c,text,x,y,size,color,font,width,leading):
 c.setFont(font,size);c.setFillColor(color);z=lines(text,font,size,width);off=(len(z)-1)*leading/2
 for i,a in enumerate(z):c.drawCentredString(x,y+off-i*leading,a)
def field(c,label,x,y,w,n=2):
 c.setFillColor(INK);c.setFont('Helvetica-Bold',8.2);c.drawString(x,y,label);c.setStrokeColor(FAINT);y-=.17*inch
 for _ in range(n):c.line(x,y,x+w,y);y-=.25*inch
 return y-.05*inch
def intro(b,ident,heading,copy,boundary):
 b.title_page(ident);b.copyright(boundary);b.frame('Welcome',False);c=b.c;c.setFont('Helvetica-Bold',18);c.setFillColor(INK);y=b.h-1.0*inch
 for ln in lines(heading,'Helvetica-Bold',18,b.w-2*b.mx):c.drawString(b.mx,y,ln);y-=.27*inch
 para(c,copy,b.mx,y-.12*inch,b.w-2*b.mx,10,13,INK);b.end()
def generic_entry(b,section,heading,quote,fields):
 b.frame(section);c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(b.mx,b.h-.82*inch,heading);c.setFillColor(MID);c.setFont('Helvetica-Oblique',8.8);y=para(c,'“'+quote+'”',b.mx,b.h-1.06*inch,b.w-2*b.mx,8.8,11,MID);y-=.22*inch
 for lab,n in fields:y=field(c,lab,b.mx,y,b.w-2*b.mx,n)
 b.end()
def pad(b,target):
 while b.n<target:b.notes()
 if b.n%2:b.notes()
 b.c.save();return b.n

PROMPTS=['What would make the next hour five percent gentler?','What is one thing I can notice without judgment?','What is already helping, even a little?','What can I make smaller before I make it better?','What would support look like in a practical form?','What can wait until I have more energy or information?','What does enough look like today?','What is one sentence I need to hear?','What belongs on the page instead of in my head?','What is one quiet win I can count?','What could I ask for instead of trying to guess?','What can be true without being fixed right now?']

def make_coloring(path,prod,mood=False):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'Color one small corner of the day.','These pages are not a test of artistic skill. Choose a color, make a mark, notice what changes—or simply enjoy the pattern.',boundary)
 art=48 if not mood else 42
 for i in range(art):
  # art page
  b.frame('Creative pause');c=b.c;c.setStrokeColor(INK);c.setLineWidth(1)
  cx,cy=b.w/2,b.h/2;R=min(b.w,b.h)*.32
  if i%4==0:
   for k in range(24):
    a=2*math.pi*k/24;x=cx+math.cos(a)*R;y=cy+math.sin(a)*R;c.circle(x,y,R*.11+(k%3)*3,stroke=1,fill=0)
   for r in [.18,.36,.54,.72,.9]:c.circle(cx,cy,R*r,stroke=1,fill=0)
  elif i%4==1:
   for k in range(28):
    a=2*math.pi*k/28;r=R*(.25+.65*((k%5)/5));x=cx+math.cos(a)*r;y=cy+math.sin(a)*r;c.circle(x,y,R*.15,stroke=1,fill=0)
   c.circle(cx,cy,R*.16,stroke=1,fill=0)
  elif i%4==2:
   for k in range(16):
    a=2*math.pi*k/16;pts=[]
    for j in range(7):
     aa=a+j*2*math.pi/6;rr=R*(.28+.1*(j%2));pts.append((cx+math.cos(aa)*rr,cy+math.sin(aa)*rr))
    p=c.beginPath();p.moveTo(*pts[0]);[p.lineTo(*pt) for pt in pts[1:]];p.close();c.drawPath(p,stroke=1,fill=0)
  else:
   for r in range(7):
    pts=[]
    for k in range(80):
     a=2*math.pi*k/79;rad=R*(.2+r*.105)+10*math.sin(5*a+r);pts.append((cx+math.cos(a)*rad,cy+math.sin(a)*rad))
    p=c.beginPath();p.moveTo(*pts[0]);[p.lineTo(*pt) for pt in pts[1:]];c.drawPath(p,stroke=1,fill=0)
  c.setFillColor(MID);c.setFont('Helvetica-Oblique',7.5);c.drawCentredString(cx,.7*inch,'Color what feels good. There is no finished version required.');b.end()
  if mood:
   generic_entry(b,'Color reflection',f'After page {i+1}',PROMPTS[i%len(PROMPTS)],[('THE COLORS I REACHED FOR',1),('WHAT I NOTICED WHILE COLORING',3),('A WORD FOR THIS MOMENT',1)])
  else:
   # blank back preserves marker-friendly coloring format
   b.frame('');b.end()
 return pad(b,target)

def make_calendar(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'Begin in any month.','This is an undated calendar. Its seasonal cues are invitations—not scent, diet, or medical protocols. Make the year start when you do.',boundary)
 for m in range(1,13):
  b.frame('Undated month');c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',18);c.drawString(b.mx,b.h-.82*inch,calendar.month_name[m]);c.setFont('Helvetica',8);c.setFillColor(MID);c.drawString(b.mx,b.h-1.04*inch,'Month ________   ·   A sensory cue: '+['open the window','sip something warm','step outside','clear one small surface'][m%4])
  x=b.mx;y=b.h-1.4*inch;cw=(b.w-2*b.mx)/7;ch=.56*inch
  for q,day in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):c.setFont('Helvetica-Bold',6.5);c.setFillColor(MID);c.drawCentredString(x+cw*(q+.5),y,day)
  y-=.12*inch
  c.setStrokeColor(LIGHT)
  for row in range(6):
   for col in range(7):c.rect(x+col*cw,y-(row+1)*ch,cw,ch,stroke=1,fill=0)
  b.end()
  generic_entry(b,'Monthly reflection',f'{calendar.month_name[m]} · small rituals',PROMPTS[m%len(PROMPTS)],[('WHAT I WANT TO MAKE EASIER',3),('A SENSORY CUE I WANT TO TRY',2),('A ROUTINE / APPOINTMENT NOTE',2),('ONE KIND NEXT STEP',1)])
  for w in range(6):generic_entry(b,'Weekly note',f'{calendar.month_name[m]} · week {w+1}',PROMPTS[(m+w)%len(PROMPTS)],[('WHAT MATTERS THIS WEEK',2),('WHAT CAN STAY SMALL',2),('ONE THING THAT SUPPORTED ME',1)])
 return pad(b,target)

def make_movement(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'Slow is a valid pace.','These pages invite you to notice comfort, environment, and choice. They are not instructions to push through pain or override your own professional guidance.',boundary)
 shapes=['Seated pause','Supported fold','Wall rest','Side-lying pause','Feet-up rest','Chair twist','Wide stance','Open arms','Knee hug','Quiet walk','Floor rest','Shoulder circle']
 for i in range(24):
  b.frame('Practice menu');c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',16);c.drawString(b.mx,b.h-.82*inch,shapes[i%len(shapes)])
  c.setStrokeColor(MID);c.setLineWidth(1.5);cx=b.w/2;cy=b.h*.54
  # abstract, non-instructional body-shape glyph
  c.circle(cx,cy+.52*inch,.18*inch,stroke=1,fill=0);c.line(cx,cy+.34*inch,cx+(i%3-1)*.2*inch,cy-.35*inch);c.line(cx,cy+.15*inch,cx-.4*inch,cy-.05*inch);c.line(cx,cy+.15*inch,cx+.4*inch,cy-.05*inch);c.line(cx+(i%3-1)*.2*inch,cy-.35*inch,cx-.35*inch,cy-.7*inch);c.line(cx+(i%3-1)*.2*inch,cy-.35*inch,cx+.35*inch,cy-.7*inch)
  c.setFillColor(MID);para(c,'A shape cue, not a prescription. Choose props, range, or rest according to your own comfort and professional guidance.',b.mx,.95*inch,b.w-2*b.mx,8.5,11,MID);b.end()
  generic_entry(b,'Body-scan reflection',f'Practice {i+1}',PROMPTS[i%len(PROMPTS)],[('BEFORE · WHAT I NOTICE',2),('WHAT FELT SUPPORTIVE OR NOT FOR ME',3),('AFTER · WHAT I WANT TO REMEMBER',2)])
 return pad(b,target)

def make_signal(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'Notice without chasing certainty.','You may skip every number. The purpose is to make observations less lonely and to keep any questions you want to raise with an appropriate professional.',boundary)
 for i in range(90):
  generic_entry(b,'Calm-check',f'Check-in {i+1}',PROMPTS[i%len(PROMPTS)],[('WHAT I AM NOTICING',2),('OPTIONAL RESTING-PULSE NOTE / TIME',1),('A GROUNDING STEP I TRIED',1),('AFTER · WHAT, IF ANYTHING, SHIFTED?',2)])
 return pad(b,target)

def make_planner(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'A year that respects capacity.','This undated planner holds work, care, appointments, and rest in the same honest frame. Use the private routine fields however you wish—or leave them blank.',boundary)
 for m in range(1,13):
  generic_entry(b,'Month at a glance',f'Month {m}',PROMPTS[m%len(PROMPTS)],[('TOP PRIORITIES',2),('APPOINTMENTS / IMPORTANT DATES',3),('CAPACITY I WANT TO PROTECT',2),('PRIVATE ROUTINE NOTE (OPTIONAL)',1)])
  for w in range(4):
   b.frame('Weekly plan');c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(b.mx,b.h-.82*inch,f'Month {m} · week {w+1}')
   y=b.h-1.15*inch
   for day in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
    c.setFont('Helvetica-Bold',7.5);c.setFillColor(INK);c.drawString(b.mx,y,day);c.setStrokeColor(FAINT);c.line(b.mx+.42*inch,y-.03*inch,b.w-b.mx,y-.03*inch);y-=.42*inch
   c.setFont('Helvetica-Bold',8);c.drawString(b.mx,y-.06*inch,'STRESS WEATHER / CAPACITY NOTE');c.setStrokeColor(FAINT);c.line(b.mx,y-.28*inch,b.w-b.mx,y-.28*inch);b.end()
 for i in range(12):generic_entry(b,'Quarterly return',f'Capacity review {i+1}',PROMPTS[i%len(PROMPTS)],[('WHAT IS WORKING',2),('WHAT NEEDS LESS PRESSURE',2),('ONE CHANGE I CAN MAKE',2)])
 return pad(b,target)

def make_weighted(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'Make the bed a landing place.','This diary records your own comfort observations. It does not recommend blanket weight, use, or treatment; follow product and professional guidance.',boundary)
 for i in range(90):generic_entry(b,'Bedside diary',f'Night {i+1}',PROMPTS[i%len(PROMPTS)],[('EVENING · ROOM FEEL / COMFORT NOTE',2),('BLANKET / BEDDING NOTE (OPTIONAL)',1),('SETTLING RITUAL I CHOSE',1),('MORNING · HOW REST FELT',2)])
 return pad(b,target)

def make_integration(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'An experience may need a slower landing.','This book is not a guide to conducting intense breathwork. It is a private place to prepare, make notes, and integrate alongside qualified support where appropriate.',boundary)
 for i in range(12):
  generic_entry(b,'Before session',f'Session {i+1} · intention',PROMPTS[i%len(PROMPTS)],[('SETTING / FACILITATOR NOTES',2),('MY INTENTION',3),('WHAT SUPPORT DO I WANT AFTERWARD?',2)])
  b.frame('Creative integration');c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(b.mx,b.h-.82*inch,'Mandala / memory map');c.setStrokeColor(LIGHT);c.circle(b.w/2,b.h*.5,min(b.w,b.h)*.27,stroke=1,fill=0)
  for r in [.2,.4,.6,.8]:c.circle(b.w/2,b.h*.5,min(b.w,b.h)*.27*r,stroke=1,fill=0)
  b.end()
  generic_entry(b,'After session',f'Session {i+1} · integration',PROMPTS[(i+3)%len(PROMPTS)],[('WHAT I NOTICE NOW',3),('WHAT I WANT TO TEND GENTLY',2),('A 24–72 HOUR INTEGRATION STEP',2)])
 for i in range(30):b.notes('Integration notes','Let the experience take the time it takes.','Integration')
 return pad(b,target)

def make_forest(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'Return to one place slowly.','Use these pages outside, at home, or after a walk. Bring only what helps: a note, a photograph, a leaf sketch, a memory.',boundary)
 for i in range(40):
  b.frame('Field note');c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(b.mx,b.h-.82*inch,f'Outing {i+1} · five senses')
  y=b.h-1.15*inch
  for lab in ['PLACE / WEATHER','WHAT I SAW','WHAT I HEARD','WHAT I FELT / TOUCHED','WHAT I WANT TO REMEMBER'] :y=field(c,lab,b.mx,y,b.w-2*b.mx,1)
  b.end()
  b.frame('Keepsake');c=b.c;c.setStrokeColor(LIGHT);c.setLineWidth(1);c.rect(b.mx,b.h-4.7*inch,b.w-2*b.mx,3.55*inch,stroke=1,fill=0);c.setFillColor(MID);c.setFont('Helvetica-Oblique',8);c.drawCentredString(b.w/2,b.h-4.95*inch,'Photo, found paper, sketch, or a memory of the light.');b.end()
  generic_entry(b,'Return',f'Outing {i+1} · reflection',PROMPTS[i%len(PROMPTS)],[('WHAT CHANGED WHEN I SLOWED DOWN?',3),('A PLACE I WANT TO RETURN TO',2)])
 return pad(b,target)

def make_couples(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'A pause before the solution.','This workbook offers optional shared language for two people. It is not couples therapy and is not designed for coercive, abusive, or unsafe situations. Seek appropriate support when needed.',boundary)
 for i in range(52):
  b.frame('Me / you / us');c=b.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(b.mx,b.h-.82*inch,f'Check-in {i+1} · pause together');x=b.mx;mid=b.w/2;top=b.h-1.18*inch;c.setStrokeColor(LIGHT);c.line(mid,1*inch,mid,top)
  for xx,head in [(x,'ME'),(mid+.22*inch,'YOU')]:
   c.setFillColor(INK);c.setFont('Helvetica-Bold',8.5);c.drawString(xx,top,head);y=top-.28*inch
   for lab in ['WHAT I AM FEELING','WHAT I NEED','ONE KIND REQUEST']:
    c.setFont('Helvetica-Bold',6.8);c.drawString(xx,y,lab);c.setStrokeColor(FAINT);c.line(xx,y-.12*inch,(mid-.18*inch if xx==x else b.w-b.mx),y-.12*inch);c.line(xx,y-.33*inch,(mid-.18*inch if xx==x else b.w-b.mx),y-.33*inch);y-=.63*inch
  c.setFillColor(MID);c.setFont('Helvetica-Oblique',7);c.drawCentredString(b.w/2,.72*inch,'Skip, adapt, or take a break. A shared page never overrides anyone’s boundaries.');b.end()
  generic_entry(b,'Us',f'Check-in {i+1} · one small repair',PROMPTS[i%len(PROMPTS)],[('WHAT WE WANT TO UNDERSTAND',2),('ONE THING THAT HELPED US PAUSE',2),('A NEXT STEP WE BOTH CONSENT TO',2)])
 return pad(b,target)

def make_desk(path,prod):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;b=Book(path,trim,cover,sub);intro(b,ident,'A minute can be enough.','These practices are designed to be read at a desk in 30–90 seconds. They are invitations, not performance tools. Skip any that do not fit your day.',boundary)
 practices=['Look at a point across the room for one slow breath.','Put both feet on the floor. Notice the surface supporting them.','Unclench your hands. Let the next task begin after that.','Name one thing that can wait ten minutes.','Let your eyes find three ordinary colors near you.','Roll your shoulders once, then choose a smaller next step.','Take a sip of water, if one is available.','Write the first physical action, not the whole project.','Place one object where it belongs.','Let your exhale be natural and a little longer.']
 for i in range(60):generic_entry(b,'Desk reset',f'Reset {i+1}',practices[i%len(practices)],[('BEFORE · ONE WORD',1),('AFTER · ONE WORD',1),('WHAT I NEED NEXT',2)])
 return pad(b,target)

BUILDERS={'coloring':make_coloring,'calendar':make_calendar,'movement':make_movement,'signal':make_signal,'planner':make_planner,'weighted':make_weighted,'integration':make_integration,'forest':make_forest,'moodcolor':lambda a,b:make_coloring(a,b,True),'couples':make_couples,'desk':make_desk}

# Existing KDP scouts assembled from prior complete production batch
EXISTING={'dose-and-breathe':'dose-and-breathe','softer-words':'softer-words','night-harbor':'night-harbor','back-to-enough':'back-to-enough','rest-and-regulate':'rest-and-regulate','enough-money-enough-calm':'enough-money-enough-calm','pocket-of-calm-companion':'pocket-of-calm-companion'}
SRC=ROOT/'source'/'baseline-kdp'

def make_cover(prod,pages,out):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod;tw,th=trim;spine=pages*PPI;W=(2*BLEED+2*tw+spine)*inch;H=(2*BLEED+th)*inch;c=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1);bg=colors.HexColor('#'+COLORS[ident]);ac=colors.HexColor('#'+ACCENTS[ident]);c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0);c.setStrokeColor(ac);c.setLineWidth(.8)
 for rr in [1.0,1.35,1.7,2.05]:c.circle(W*.82,H*.80,rr*inch,stroke=1,fill=0)
 sx=(BLEED+tw)*inch;c.setStrokeColor(colors.Color(1,1,1,.2));c.line(sx,0,sx,H);c.line(sx+spine*inch,0,sx+spine*inch,H)
 fx=(BLEED+tw+spine)*inch;centred(c,cover,fx+tw*inch/2,H*.59,23,colors.white,'Helvetica-Bold',tw*inch-.8*inch,27);centred(c,sub,fx+tw*inch/2,H*.47,9.6,ac,'Helvetica',tw*inch-.9*inch,12)
 c.setFillColor(colors.white);c.setFont('Helvetica',8);c.drawCentredString(fx+tw*inch/2,H*.17,IMPRINT);c.setFillColor(ac);c.setFont('Helvetica',6.5);c.drawCentredString(fx+tw*inch/2,.38*inch,'THE RITUAL LIBRARY')
 bx=BLEED*inch+.35*inch;c.setFillColor(ac);c.setFont('Helvetica-Bold',7.5);c.drawString(bx,H*.66,'THE RITUAL LIBRARY');para(c,desc,bx,H*.62,tw*inch-.7*inch,8.3,10.5,colors.white);c.setFillColor(colors.white);c.rect(.32*inch,.35*inch,2*inch,1.2*inch,fill=1,stroke=0);c.setFillColor(bg);c.setFont('Helvetica',5.3);c.drawCentredString(1.32*inch,.28*inch,'BARCODE KEEP-CLEAR AREA')
 if spine>=.18:
  c.saveState();c.translate(sx+spine*inch/2,.36*inch);c.rotate(90);c.setFillColor(colors.white);c.setFont('Helvetica-Bold',max(4,min(7,spine*28)));c.drawCentredString(th*inch/2,0,cover.upper());c.restoreState()
 c.save();return spine,(2*BLEED+2*tw+spine),(2*BLEED+th)

def cover_front_jpg(prod, output):
 ident,slug,coll,cover,title,sub,trim,*_=prod;W,H=1600,2400;im=Image.new('RGB',(W,H),'#'+COLORS[ident]);dr=ImageDraw.Draw(im);ac='#'+ACCENTS[ident];
 fbig=font(90,True);fsub=font(38);fsmall=font(28)
 # circles
 for r in [350,470,590]:dr.ellipse((W-300-r,H*0.15-r,W-300+r,H*0.15+r),outline=ac,width=3)
 centered_image(dr,cover,W/2,int(H*.47),fbig,'#FFFFFF',W-180,108);centered_image(dr,sub,W/2,int(H*.61),fsub,ac,W-220,50);dr.text((W/2,H-310),IMPRINT,font=fsmall,fill='#FFFFFF',anchor='mm');dr.text((W/2,H-120),'THE RITUAL LIBRARY',font=font(20),fill=ac,anchor='mm');im.save(output,quality=94)

def font(size,bold=False):
 paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
 for p in paths:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default()
def wrapped_img(draw,text,f,w):
 words=text.split();out=[];cur=''
 for z in words:
  t=(cur+' '+z).strip()
  if draw.textbbox((0,0),t,font=f)[2]<=w or not cur:cur=t
  else:out.append(cur);cur=z
 if cur:out.append(cur)
 return out
def centered_image(draw,text,x,y,f,fill,w,lead):
 ls=wrapped_img(draw,text,f,w);y-=lead*(len(ls)-1)/2
 for l in ls:draw.text((x,y),l,font=f,fill=fill,anchor='mm');y+=lead

def page_jpg(pdf,page,out):
 d=fitz.open(str(pdf));page=min(page,len(d)-1);pix=d[page].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False);pix.save(str(out))
def callout_jpg(prod,out):
 ident,slug,coll,cover,title,sub,trim,pages,paper,price,*_=prod;W,H=1600,1200;im=Image.new('RGB',(W,H),'#F7F4EF');dr=ImageDraw.Draw(im);bg='#'+COLORS[ident];ac='#'+ACCENTS[ident];dr.rectangle((0,0,W,250),fill=bg);dr.text((80,95),cover,font=font(62,True),fill='#FFFFFF');dr.text((80,185),sub,font=font(28),fill=ac)
 cols=[('TRIM',f'{trim[0]:g} × {trim[1]:g} in.'),('PAGES',str(pages)),('INTERIOR','B&W · white paper'),('SCOUT PRICE',f'${price:.2f}')]
 for i,(a,b) in enumerate(cols):
  x=90+(i%2)*770;y=380+(i//2)*290;dr.rounded_rectangle((x,y,x+660,y+190),20,fill='#FFFFFF',outline=ac,width=4);dr.text((x+35,y+45),a,font=font(24,True),fill=bg);dr.text((x+35,y+105),b,font=font(34),fill='#262626')
 dr.text((80,1060),'A KDP scout edition from The Ritual Library · deluxe materials sold separately where available.',font=font(22),fill='#505050');im.save(out,quality=94)
def series_jpg(collection,out):
 W,H=1600,1200;bg='#20313D' if collection=='Pace & Progress' else '#35443A';ac='#A4C3B2' if collection=='Pace & Progress' else '#D8B887';im=Image.new('RGB',(W,H),bg);dr=ImageDraw.Draw(im)
 for i in range(6):
  x=110+i*220;y=510-((i%2)*60);dr.rounded_rectangle((x,y,x+170,y+350),20,fill='#F8F4ED',outline=ac,width=5);dr.line((x+35,y+90,x+135,y+90),fill=ac,width=5);dr.line((x+35,y+125,x+120,y+125),fill=ac,width=3)
 dr.text((W/2,190),'THE RITUAL LIBRARY',font=font(35,True),fill=ac,anchor='mm');dr.text((W/2,280),collection,font=font(70,True),fill='#FFFFFF',anchor='mm');dr.text((W/2,1010),'Quiet, tactile tools for real life · notice, soothe, continue',font=font(30),fill=ac,anchor='mm');im.save(out,quality=94)

def write_metadata(prod,pages,spine,wrapw,wraph,folder):
 ident,slug,coll,cover,title,sub,trim,target,paper,price,kind,desc,kws,cats,boundary=prod
 (folder/'metadata.txt').write_text(f'''AMAZON TITLE: {title}
COVER TITLE: {cover}
SUBTITLE: {sub}
AUTHOR: {IMPRINT}
SERIES: {coll}
FORMAT: Paperback · black & white interior · white paper · no interior bleed · matte cover
TRIM: {trim[0]:g} × {trim[1]:g} in.
PAGES: {pages}
SPINE: {spine:.4f} in. (white-paper formula; validate in KDP Cover Calculator)
COVER WRAP: {wrapw:.4f} × {wraph:.4f} in.
PRICE: ${price:.2f}
CATEGORIES: {cats}
KEYWORDS: {kws.replace('|',', ')}

DESCRIPTION:
{desc}

CLAIMS / RELEASE BOUNDARY:
{boundary}

UPLOAD NOTE:
Confirm the final imprint, use the current KDP cover template, and inspect a physical proof. Wave 1 QR/audio is a separate live-route and proof-scan gate before publication or advertising.
''',encoding='utf-8')

def rgb(hex_value):
 hex_value=hex_value.lstrip('#');return tuple(int(hex_value[i:i+2],16)/255 for i in (0,2,4))

def brand_existing_interior(pdf_path,ident):
 # Baseline interiors stay immutable. Stamp only regenerated release copies with the working imprint
 # and a clear unpublished QR/audio holding note. configure_wave1_qr.py replaces this note once all route gates pass.
 doc=fitz.open(str(pdf_path));page=doc[0];page.add_redact_annot(fitz.Rect(105,420,328,455),fill=rgb(COLORS[ident]));page.apply_redactions();page.insert_textbox(fitz.Rect(75,430,358,448),IMPRINT,fontsize=8.5,fontname='helv',color=(1,1,1),align=1,overlay=True)
 page=doc[1];page.add_redact_annot(fitz.Rect(34,215,398,285),fill=(1,1,1));page.apply_redactions();page.insert_text((40,233),f'Copyright © 2026 {IMPRINT}. All rights reserved.',fontsize=7.2,fontname='helv',color=(.31,.31,.31),overlay=True);page.insert_textbox(fitz.Rect(40,242,365,280),'Prepublication candidate: do not publish until the brand-owned QR/audio route, claims review, KDP preflight, and physical-proof gates are complete.',fontsize=7.0,fontname='helv',color=(.31,.31,.31),overlay=True)
 tmp=pdf_path.with_suffix('.tmp.pdf');doc.save(tmp,garbage=4,deflate=True);doc.close();tmp.replace(pdf_path)

def assemble_existing(prod):
 ident,slug,*_=prod;out=RELEASE/f'{ident}-{slug}';out.mkdir(parents=True,exist_ok=True);src=SRC/f'{ident}-{slug}'
 shutil.copy2(src/'interior.pdf',out/'interior.pdf');shutil.copy2(src/'cover_wrap.pdf',out/'cover_wrap.pdf');brand_existing_interior(out/'interior.pdf',ident)
 d=fitz.open(str(out/'interior.pdf'));pages=len(d);d.close();tw,th=prod[6];spine=pages*PPI;write_metadata(prod,pages,spine,2*BLEED+2*tw+spine,2*BLEED+th,out)
 return out,pages

def build_extra(prod):
 ident,slug,*_=prod;out=RELEASE/f'{ident}-{slug}';out.mkdir(parents=True,exist_ok=True);pages=BUILDERS[prod[10]](out/'interior.pdf',prod);spine,ww,wh=make_cover(prod,pages,out/'cover_wrap.pdf');write_metadata(prod,pages,spine,ww,wh,out);return out,pages

def assets(prod,folder):
 # listing 1: front cover; listing 2-5: representative interior pages; 6 callout; 7 series
 cover_front_jpg(prod,folder/'cover.jpg')
 d=fitz.open(str(folder/'interior.pdf'));candidates=[0,max(1,len(d)//12),max(2,len(d)//3),max(3,len(d)//2)]
 for i,p in enumerate(candidates,2):page_jpg(folder/'interior.pdf',p,folder/f'listing_{i:02d}_interior.jpg')
 callout_jpg(prod,folder/'listing_06_callout.jpg')
 # one shared visual stored per product so every upload directory is self-contained
 series_jpg(prod[2],folder/'listing_07_series.jpg')

def docs():
 # CSV
 with (ROOT/'CATALOG.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['id','collection','amazon_title','cover_title','subtitle','pages','trim','paper','spine_in','wrap_w','wrap_h','price','folder','keywords','categories','format','claims_boundary','release_wave','publication_status','primary_validation','release_trigger'])
  for prod in PRODUCTS:
   ident,slug,coll,cover,title,sub,trim,target,paper,price,*_=prod;folder=RELEASE/f'{ident}-{slug}';d=fitz.open(str(folder/'interior.pdf'));pages=len(d);spine=pages*PPI;wave,status,test,trigger=RELEASE_STATE[ident];w.writerow([ident,coll,title,cover,sub,pages,f'{trim[0]:g}x{trim[1]:g}',paper,f'{spine:.4f}',f'{2*BLEED+2*trim[0]+spine:.4f}',f'{2*BLEED+trim[1]:.4f}',f'${price:.2f}',f'release/{ident}-{slug}',prod[12],prod[13],'Paperback · B&W · white · no bleed · matte',prod[14],wave,status,test,trigger])
 # Start, readme, upload
 (ROOT/'00_START_HERE.md').write_text('''# The Ritual Library — start here

This is a Git-ready 18-SKU KDP scout catalog with two companion deluxe-hero packages. It is deliberately organized like a production repository: every paperback has interior, wrap, seven listing images, metadata, upload settings, rebuild code, and automated structural QC.

## First actions
1. Read `LEGAL_AND_CLAIMS.md` before changing or publishing health-adjacent metadata.
2. Open `CATALOG.csv` to see every KDP listing title, price, format, and file path.
3. Read `RELEASE_POLICY.md` and `PORTFOLIO.md`. For each **Wave 1** scout only, open its `release/[ID]-[slug]/metadata.txt`; copy the **AMAZON TITLE**, not merely the cover word.
4. Use `UPLOAD_CHECKLIST.md` and KDP Print Previewer. Order a proof before enabling ads.
5. Run `python validate_catalog.py` after any rebuild. A green validation result is structural QC, not legal/clinical clearance.
6. For the two-read Oct 31 / Nov 28 Gate 1 calculations, use `/home/user/ritual-library-launch-kit/gate-1-validation-scorecard.xlsx` and its adjacent `SCORECARD_READ1_READ2_SPEC.md`.

## Two collections
| Collection | IDs | Customer promise |
|---|---|---|
| Pace & Progress | A01–A08 | Gentle, private support for routines, reflection, and care journeys. |
| Stillwork Editions | A09, B10–B18 | Small tactile rituals for hard days, desks, relationships, rest, and outdoors. |

## Files in every KDP product folder
| File | Purpose |
|---|---|
| `interior.pdf` | KDP paperback interior |
| `cover_wrap.pdf` | Full paperback wrap, sized from page count / white-paper spine formula |
| `cover.jpg` | Listing image 1 / front-cover asset |
| `listing_02`–`05_interior.jpg` | Interior-preview images |
| `listing_06_callout.jpg` | Trim / page / paper / scout-price card |
| `listing_07_series.jpg` | Collection card |
| `metadata.txt` | Upload title, listing description, seven keywords, categories, price, claims boundary |

## Rebuild / package / QC
```bash
pip install -r requirements.txt
python build_catalog.py        # regenerates the full release package
python validate_catalog.py     # structural QC; exits non-zero on a failure
python make_zips.py            # creates only the six Wave 1 candidate bundles
python make_zips.py --all-vault # explicit internal archive only; never an upload plan\n# Only after a real domain and deployment: python configure_wave1_qr.py --domain <domain> --apply --verify-live
```

Do not release a product simply because it validates or has a ZIP file. Follow `RELEASE_POLICY.md`; only six Wave 1 SKUs are potential September uploads. Stillwork Studio is the working imprint candidate, subject to clearance. Clear names/claims, complete the QR/audio gate where applicable, validate the final KDP template, and approve proof copies.
''',encoding='utf-8')
 (ROOT/'README.md').write_text('''# The Ritual Library — 18 KDP scouts + deluxe hero formats

A complete, repository-grade production system for an 18-product wellness-stationery catalog. **Built does not mean published:** only six Wave 1 KDP scouts are eligible for the release gates; twelve assets are intentionally held or vaulted. This is not a list of ideas: it includes full low-content interiors, KDP wraps, listing image suites, listing metadata, catalogs, launch documentation, reproducible source, and structural validation.

## Deliverables at a glance
- **18 KDP paperback packages** in `release/`, each with 10 publication/listing files.
- **2 deluxe hero packages** in `deluxe-heroes/`: *Dose & Breathe* and *Pocket of Calm*.
- **Commercial operating docs:** `CATALOG.csv`, `RELEASE_POLICY.md`, `PORTFOLIO.md`, `WAVE1_HUMAN_QA.md`, `KDP_ACCOUNT_OPERATIONS.md`, `LEGAL_AND_CLAIMS.md`, `MARKETING.md`, `UPLOAD_CHECKLIST.md`, `ART_DIRECTION.md`, `DELUXE_HEROES.md`, `POLISH_NOTES.md`, `HISTORY.md`, `LOOKBOOK.pdf`, `00_START_HERE.md`, `PREPUBLICATION_SEQUENCE.md`, `SCORECARD_READ1_READ2_SPEC.md` (in the launch kit), `QR_AND_AUDIO.md`, `QR_AUDIO_REVIEW.md`, `TRADEMARK_SCREENING.md`, `BACKUP_IMPRINT_SHORTLIST.md`, `COUNSEL_ENGAGEMENT_MEMO.md`, and `DECISIONS.md`.
- **Build/QC tools:** `build_catalog.py`, `polish_catalog.py`, `validate_catalog.py`, `configure_wave1_qr.py`, `make_zips.py`, and `requirements.txt`.

## Product truthfulness
The KDP editions are purposeful scout products: complete paperback experiences with honest paperback materials. Deluxe materials—foil, ribbons, velvet, coils, card decks, rigid boxes, pockets, scent treatments, and kitting—are not represented as part of a KDP paperback. The two deluxe hero directories are vendor-ready content/art packages that still require final printer dielines and physical proofs.

## Release blockers
The v1.1 candidate build uses **Stillwork Studio** as its working imprint. Before any release: obtain name/claims clearance, register the buyer-controlled domain, complete and test the Wave 1 QR/audio route, complete the final KDP Cover Calculator check, and approve the physical proof. `Pocket of Calm` is current collection-neutral copy; do not convert it to GLP-1-specific promotion without a separate reviewed content pass.
''',encoding='utf-8')
 # Upload list
 s=['# KDP upload checklist — 18 scout paperbacks','', 'Use the exact title, price, categories, and keywords in each product folder’s `metadata.txt`. Standard configuration unless metadata says otherwise: **Paperback · black-and-white · white paper · no interior bleed · matte cover**. Upload interior + wrap, run Previewer, order a proof, then publish.','']
 for prod in PRODUCTS:
  ident,slug,coll,cover,title,sub,trim,target,paper,price,*_=prod;folder=RELEASE/f'{ident}-{slug}';pages=len(fitz.open(str(folder/'interior.pdf')))
  s+= [f'## {ident} — {cover}',f'1. Title: **{title}**',f'2. Author / imprint: **{IMPRINT}** (working candidate; confirm name clearance before upload).',f'3. Settings: B&W · white paper · {trim[0]:g} × {trim[1]:g} in. · no bleed · matte.',f'4. Upload `release/{ident}-{slug}/interior.pdf` + `cover_wrap.pdf`.',f'5. Price: **${price:.2f}** · pages: {pages} · series: {coll}.',f'6. Preview → check barcode/spine/margins → order proof → publish only after claims review.','']
 (ROOT/'UPLOAD_CHECKLIST.md').write_text('\n'.join(s),encoding='utf-8')
 (ROOT/'MARKETING.md').write_text('''# The Ritual Library — listing and launch system

## Series / collection rule
Keep listing pages, ad groups, and imagery organized into two collections. Follow `RELEASE_POLICY.md`: only Wave 1 can be uploaded/tested; Pocket of Calm is a collection-neutral Stillwork flagship and its KDP companion stays vaulted. **Pace & Progress** (A01–A09) and **Stillwork Editions** (B10–B18). Do not launch 18 ads. Use the validation scorecard to decide which 3–4 initial scouts deserve spend.

## Amazon listing-image order — every SKU
1. `cover.jpg` — listing main image / clean cover representation.
2. `listing_02_interior.jpg` through `listing_05_interior.jpg` — actual interior samples; these are crucial for low-content products.
3. `listing_06_callout.jpg` — trim, pages, paper, and scout price.
4. `listing_07_series.jpg` — collection relationship / cross-sell visual.

## Initial ad candidates, not automatic launches
| Product | Why test it first | Marketing boundary |
|---|---|---|
| A01 Dose & Breathe | Distinctive routine + calm positioning | Generic GLP-1 wording only; no outcomes, dosing, or trademark misuse. |
| A04 Softer Words | Broad gifting and low-friction daily use | Personal-reflection language only. |
| B12 Back to Enough | Clear low-capacity productivity problem | No treatment claims for burnout. |
| B10 Rest & Regulate | Strong ritual/content clarity | No vagus, HRV, or anxiety-treatment claims. |
| B18 Enough Money, Enough Calm | Emotion-led finance niche | No financial advice/outcome claims. |
| A09 Pocket of Calm companion | Vaulted KDP reference only | Do not advertise/upload this KDP companion; validate the collection-neutral deck through its separate paid card/waitlist path. |

## Title / claims discipline
- Paste **AMAZON TITLE** from `metadata.txt`, not only the short cover title.
- Use all seven keywords exactly as a starting hypothesis, then revise only through documented testing.
- Never add outcome promises to listings, images, ads, reviews, packaging, or creator briefs.
- KDP versions must state/depict only what they physically include. Do not show card decks, foil, ribbon, scent, or boxes unless the listing is for that exact product.

## First review language to watch
The desired organic words are **gift**, **beautiful**, **gentle**, and **finally**. Log buyer objections—especially “not enough inside,” “expected deluxe materials,” “too clinical,” and “unclear”—in the validation Scorecard before changing a title, price, or interior.
''',encoding='utf-8')
 (ROOT/'LEGAL_AND_CLAIMS.md').write_text('''# Legal, trademark, advertising, and QR/audio control

**Status:** prepublication control; not legal, medical, clinical, financial, trademark, advertising-platform, or data-privacy clearance.

## Global product rules
- Do not promise treatment, diagnosis, cure, symptom relief, weight loss, physiological change, safer medication use, financial results, relationship outcomes, or a guaranteed emotional effect.
- Keep KDP paperback and deluxe-object descriptions distinct. Never claim an insert, material, QR/audio, scent, card deck, or device in a product that does not include it.
- Clear **The Ritual Library**, **Stillwork Studio**, series names, every product name, and any third-party mark before public launch. The preliminary observation log is `TRADEMARK_SCREENING.md`; it is not clearance.
- Obtain an appropriate reviewer’s sign-off for all GLP-1, sleep, pulse, anxiety, breathwork, movement, blanket, relationship, money, creator, landing-page, and optional-audio language—cover, interior, listing, advertising, creator brief, packaging, and landing page.

## Wave 1 claims/name sweep
Before a Wave 1 title is marked Clear, review its title, subtitle, seven keywords, description, cover/wrap, listing images, A+ copy, QR landing-page transcript, creator brief, and paid-ad variants for: **Ozempic, Wegovy, Mounjaro, dose, injection, medication, treatment, cure, medical, therapy, weight loss, anxiety, sleep**, and outcome/guarantee language. Named prescription-drug marks are not a default keyword or creative option.

## Paid-media policy verification — Collection A
**Open gate:** No paid Meta or TikTok campaign for A01 or another Collection A/GLP-1-adjacent asset is authorized until the relevant platform’s current policy, account eligibility, country, creative, landing page, targeting, age setting, and tracking plan are reviewed and documented.

- Do not target or imply a viewer’s medical condition, prescription use, body status, or other sensitive personal attribute. Do not request health information in a lead form without the platform permissions and privacy review that apply.
- Do not use prescription-drug names, drug imagery, outcome claims, before/after imagery, body shaming, calorie-count pressure, or health-condition profiling as a shortcut to an audience.
- Meta’s current policy materials prohibit health/personal-attribute assertions and set 18+ restrictions for many weight-loss/health product or service ads. Confirm the exact policy/account treatment at launch: <https://transparency.meta.com/policies/ad-standards/objectionable-content/privacy-violations-personal-attributes> and <https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness/>.
- TikTok policy materials restrict prescription-drug content and weight-management/body-image claims. Confirm the current U.S. account treatment before submitting any creative: <https://ads.tiktok.com/help/article/tiktok-ads-policy-dangerous-products-or-services> and <https://ads.tiktok.com/help/article/tiktok-ads-policy-weight-management>.
- Amazon Ads requires truthful, substantiated detail-page-aligned claims; its moderation guidance identifies prescription-medicine keywords/products as unacceptable targeting. Keep Amazon keywords in the product’s truthful reflection/journaling scope and complete the metadata audit: <https://advertising.amazon.com/library/guides/sponsored-brands-display-ads-moderation>.

Interest-adjacent wellness/journaling creative and collection-neutral creator seeding are hypotheses to review, not pre-cleared substitutes for policy compliance. Do not pass health/medical or sensitive financial data to ad platforms. See `PREPUBLICATION_SEQUENCE.md` for the release order.

## QR/audio and privacy gate
Only the six Wave 1 paperbacks may receive the selected optional QR/audio feature. The printed code must use a buyer-controlled HTTPS host, resolve to a reviewed first-party page, play the actual named audio, expose a matching transcript, and pass a physical-proof scan. No raw platform/shortener URL, temporary host, unreviewed audio, health data capture, or undisclosed tracker belongs in the printed experience. Follow `QR_AND_AUDIO.md` and use `configure_wave1_qr.py` only after deployment.

## Product-specific escalations
| ID | Escalation |
|---|---|
| A01–A03, A06–A08 | GLP-1 / medication-adjacent copy: never provide medical guidance or outcomes. |
| A05, B11 | Sleep/blanket: no insomnia treatment or blanket-weight recommendation. |
| A07 | Pulse/sensation logging: not a device, diagnosis, or emergency guide. |
| B10, B13 | Breathwork: no vagus/HRV/treatment claims; B13 is not instruction for intense breathwork. |
| B12, B15, B16, B18 | Do not market as therapy, art therapy, couples therapy, or financial/mental-health treatment. |

## Proofing gate
No product may be published until the relevant metadata boundary has been reviewed, required claims/name/ad-policy scope is clear, the exact QR/audio feature (if selected) passes its gate, and the KDP proof matches the listing’s material/format claims.
''',encoding='utf-8')
 (ROOT/'.gitignore').write_text('''# Generated packages and local environments
packages/
__pycache__/
.venv/
*.pyc
.DS_Store
''',encoding='utf-8')
 (ROOT/'requirements.txt').write_text('reportlab>=4.4,<5\nPillow>=10,<13\nPyMuPDF>=1.24,<2\nqrcode[pil]>=8,<9\n',encoding='utf-8')

def make_lookbook():
 W,H=11*inch,8.5*inch;c=canvas.Canvas(str(ROOT/'LOOKBOOK.pdf'),pagesize=(W,H),pageCompression=1)
 # title
 c.setFillColor(colors.HexColor('#20313D'));c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(colors.white);c.setFont('Helvetica-Bold',28);c.drawCentredString(W/2,H*.64,'THE RITUAL LIBRARY');c.setFillColor(colors.HexColor('#A4C3B2'));c.setFont('Helvetica',14);c.drawCentredString(W/2,H*.56,'18 KDP scout paperbacks · 2 deluxe hero formats');c.setFont('Helvetica-Oblique',11);c.drawCentredString(W/2,H*.46,'notice · soothe · continue');c.showPage()
 for prod in PRODUCTS:
  ident,slug,coll,cover,title,sub,trim,target,paper,price,*_=prod;folder=RELEASE/f'{ident}-{slug}';img=Image.open(folder/'cover.jpg');img.thumbnail((int(2.25*inch),int(3.35*inch)))
  # reportlab can place jpg file
  c.setFillColor(colors.HexColor('#F7F4EF'));c.rect(0,0,W,H,fill=1,stroke=0);c.drawImage(str(folder/'cover.jpg'),.75*inch,2.1*inch,width=2.1*inch,height=3.15*inch,preserveAspectRatio=True,anchor='c')
  c.setFillColor(colors.HexColor('#'+COLORS[ident]));c.setFont('Helvetica-Bold',9);c.drawString(3.3*inch,H-1.05*inch,coll.upper())
  c.setFillColor(INK);c.setFont('Helvetica-Bold',25);y=H-1.52*inch
  for line in lines(cover,'Helvetica-Bold',25,W-4.15*inch):c.drawString(3.3*inch,y,line);y-=.34*inch
  c.setFont('Helvetica',12);c.setFillColor(MID);y-=.08*inch
  for line in lines(sub,'Helvetica',12,W-4.15*inch):c.drawString(3.3*inch,y,line);y-=.19*inch
  c.setFillColor(INK);c.setFont('Helvetica',10);y-=.3*inch;y=para(c,prod[11],3.3*inch,y,W-4.15*inch,10,13,INK)
  y-=.22*inch;c.setFont('Helvetica-Bold',9);c.drawString(3.3*inch,y,f'KDP SCOUT  ·  {trim[0]:g} × {trim[1]:g} in.  ·  {len(fitz.open(str(folder/"interior.pdf")))} pages  ·  ${price:.2f}')
  c.setFillColor(MID);c.setFont('Helvetica',8);para(c,'Deluxe version: '+('available as a separate hero-production package.' if ident in ('A01','A09') else 'future product path; not included with paperback scout.'),3.3*inch,y-.23*inch,W-4.15*inch,8,10,MID)
  c.showPage()
 c.save()

def main():
 # rebuild/assemble 18 interiors and wraps
 for prod in PRODUCTS:
  if prod[1] in EXISTING: folder,pages=assemble_existing(prod)
  else: folder,pages=build_extra(prod)
  assets(prod,folder)
 # copy deluxe hero originals
 srcdel=ROOT/'source'/'baseline-deluxe'
 if srcdel.exists():
  for item in srcdel.iterdir():
   dest=DELUXE/item.name
   if dest.exists():shutil.rmtree(dest)
   shutil.copytree(item,dest)
 docs();
 # Buyer-visible cover/listing system is a deliberate second art-direction pass.
 import subprocess, sys
 subprocess.run([sys.executable, str(ROOT/'polish_catalog.py')], check=True)
 make_lookbook()
 print('Built 18 KDP products at',ROOT)

if __name__=='__main__':main()
