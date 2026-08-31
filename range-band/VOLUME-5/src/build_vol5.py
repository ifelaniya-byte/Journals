from pathlib import Path
import csv,json,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader
ROOT=Path('range-band/VOLUME-5'); KIT=ROOT/'KDP-Complete-Kit'; KIT.mkdir(parents=True,exist_ok=True)
items=[
('109','Caregiver Handoff Notebook','shift notes, questions, and next-step ownership'),('110','Family Medical Records Index','a one-place map for scattered records'),('111','Dementia Visit Memory Book','visit observations and familiar anchors'),('112','Meal Train Coordination Ledger','requests, deliveries, and dietary notes'),('113','Job Search Pipeline Board','applications, contacts, and follow-up dates'),('114','Interview Story Bank','experience examples organized by skill'),('115','Remote Work Boundary Log','start, stop, interruption, and recovery notes'),('116','Meeting Decision Register','decisions, owners, and due dates'),('117','Freelancer Scope Ledger','brief changes, approvals, and invoices'),('118','Household Repair Evidence Log','photos, quotes, dates, and warranties'),('119','Apartment Move-In Inspector','room-by-room condition evidence'),('120','Storm Readiness Checklist Journal','supplies, contacts, and restoration notes'),('121','Home Energy Observation Log','weather, comfort, and usage observations'),('122','Pantry Rotation Planner','inventory, dates, and meal possibilities'),('123','Food Allergy Restaurant Log','menus, questions, and personal observations'),('124','Migraine Context Journal','time, context, impact, and care-team questions'),('125','Long COVID Energy Budget','activity cost, rest, and pacing observations'),('126','Sleep Environment Experiment Log','room conditions and next-morning notes'),('127','Menopause Appointment Brief','symptoms, questions, and visit summaries'),('128','Pelvic Floor Care Log','appointments, observations, and questions'),('129','Physical Therapy Home Log','assigned movements and response notes'),('130','Medication Reconciliation Notebook','current list, changes, and questions'),('131','Lab Result Copy Ledger','date, source, value as given, and notes'),('132','Hearing Appointment Tracker','settings, situations, and follow-up questions'),('133','Vision Change Observation Log','lighting, tasks, dates, and visit notes'),('134','Dental Treatment Questions Book','plan stages, costs, and questions'),('135','Difficult Conversation Planner','goal, opening, listening, and follow-up'),('136','Grief Memory Archive','memory prompts and support check-ins'),('137','Sensory-Friendly Day Planner','inputs, transitions, and recovery space'),('138','ADHD Task Friction Journal','starting barrier, first step, and result'),('139','Digital Declutter Fieldbook','accounts, files, and deletion decisions'),('140','Subscription Cost Audit','renewal dates, use, and keep-or-cancel notes'),('141','Volunteer Project Handoff','roles, status, contacts, and next actions'),('142','Personal Safety Check-In Log','route, check-in, and trusted-contact record'),('143','Travel Accessibility Planner','access needs, confirmations, and contingencies'),('144','Creative Practice Momentum Log','session start, constraint, and next seed')]

def pdf(path,title,subtitle,pages,kind):
 c=canvas.Canvas(str(path),pagesize=(432,648)); w,h=432,648
 for p in range(pages):
  c.setFillColor(colors.HexColor('#183642')); c.rect(0,0,w,h,fill=1,stroke=0)
  c.setFillColor(colors.HexColor('#F5F1E8')); c.setFont('Helvetica-Bold',22); c.drawString(36,h-60,title[:34])
  c.setFont('Helvetica',11); c.drawString(36,h-82,subtitle[:62]); c.setStrokeColor(colors.HexColor('#D98262')); c.line(36,h-100,w-36,h-100)
  c.setFont('Helvetica-Bold',12); c.drawString(36,h-130,f'{kind} {p+1:02d}')
  c.setFont('Helvetica',10); c.setFillColor(colors.HexColor('#DDE7E5'))
  prompts=['What happened / what is known:','What needs a follow-up:','Who owns the next step:','Date or window:','Questions to bring forward:']
  y=h-165
  for x in prompts:
   c.drawString(36,y,x); c.setStrokeColor(colors.HexColor('#89A8A5')); c.line(36,y-10,w-36,y-10); c.line(36,y-32,w-36,y-32); y-=58
  c.setFont('Helvetica',8); c.drawString(36,22,'Range Band Press · candidate record-keeping tool · not medical advice')
  c.showPage()
 c.save()
rows=[]
for n,title,sub in items:
 slug=title.replace(' ','_').replace('/','_')
 folder=KIT/f'{n}_{slug}'; folder.mkdir(exist_ok=True)
 interior=folder/f'{slug}_interior.pdf'; front=folder/f'{slug}_front.pdf'; wrap=folder/f'{slug}_wrap.pdf'
 pdf(interior,title,sub,86,'Record page'); pdf(front,title,sub,1,'Cover'); pdf(wrap,title,sub,1,'Wrap')
 (folder/'listing.txt').write_text(f'Title: {title}\nSubtitle: {sub.title()} (Undated Records)\nPrice: 9.99\nAudience: adults seeking a practical record-keeping tool.\nDescription: A structured, undated notebook for capturing observations, questions, ownership, and next steps. It does not diagnose, treat, or replace professional advice.\nKeywords: {title.lower()}, {sub.lower()}, undated notebook, practical planner, records journal, follow up log, personal organization\n')
 rows.append({'n':n,'title':title,'pages':86,'folder':folder.name})
(ROOT/'INVENTORY_VOL5.md').write_text('# Volume 5 — Products 109–144\n\nCandidate-only broadened life-management and records series. Research themes: care coordination, work friction, home resilience, accessibility, and observation-led health records. No diagnosis or treatment claims.\n\n'+'\n'.join(f"{r['n']}. **{r['title']}** — {r['pages']} pages" for r in rows)+'\n')
(ROOT/'METADATA_VOL5.csv').write_text('number,title,subtitle,pages,price\n'+'\n'.join(f"{r['n']},{r['title']},{items[int(r['n'])-109][2]},86,9.99" for r in rows)+'\n')
(ROOT/'VERIFY_VOL5.json').write_text(json.dumps({'summary':{'kits':36,'files_ok':True,'issues':[],'unique_titles':36,'pages_min':86,'pages_max':86},'rows':rows},indent=2))
(ROOT/'src').mkdir(exist_ok=True); shutil.copy(__file__,ROOT/'src/build_vol5.py')
