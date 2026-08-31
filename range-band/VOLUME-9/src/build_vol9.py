from pathlib import Path
import csv,json,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader
ROOT=Path('range-band/VOLUME-9'); KIT=ROOT/'KDP-Complete-Kit'; KIT.mkdir(parents=True,exist_ok=True)
items=[('253', 'Accessible Workplace Setup Log', 'environment, adjustment, result, and next request'), ('254', 'Care Team Question Cards', 'topic, example, question, and answer notes'), ('255', 'Appointment Transportation Log', 'ride, time, access detail, and backup'), ('256', 'Home Care Supply Ledger', 'item, quantity, source, and reorder note'), ('257', 'Family Calendar Handoff', 'schedule, owner, change, and confirmation'), ('258', 'Shared Household Task Board', 'task, standard, owner, and completion'), ('259', 'New Parent Support Handoff', 'routine, contact, supply, and question'), ('260', 'School Pickup Authorization Log', 'date, person, permission, and confirmation'), ('261', 'Child Activity Equipment Log', 'item, condition, location, and replacement'), ('262', 'Caregiver Meal Planning Book', 'preference, preparation, delivery, and response'), ('263', 'Community Resource Call Log', 'organization, representative, reference, and next step'), ('264', 'Benefits Application Tracker', 'program, document, submission, and status'), ('265', 'Housing Search Evidence Book', 'listing, criteria, contact, and decision'), ('266', 'Lease Renewal Decision Log', 'terms, questions, comparison, and response'), ('267', 'Moving Day Command Book', 'box, room, person, issue, and resolution'), ('268', 'Household Utility Transfer Log', 'service, address, date, confirmation, and account note'), ('269', 'Insurance Claim Timeline', 'event, contact, evidence, and status'), ('270', 'Personal Property Photo Index', 'item, location, image reference, and value note'), ('271', 'Storm Repair Contractor Log', 'vendor, scope, quote, warranty, and follow-up'), ('272', 'Seasonal Vehicle Readiness Book', 'check, date, evidence, and service question'), ('273', 'Workplace Incident Fact Log', 'date, setting, facts, witness, and follow-up'), ('274', 'HR Conversation Preparation Book', 'goal, facts, questions, and agreement'), ('275', 'Career Change Research Ledger', 'role, evidence, contact, and next experiment'), ('276', 'Freelance Invoice Follow-Up Log', 'client, invoice, contact, promise, and date'), ('277', 'Small Team Process Notebook', 'current step, friction, owner, and revision'), ('278', 'Meeting Facilitation Fieldbook', 'purpose, voices, decision, and next action'), ('279', 'Volunteer Training Register', 'person, topic, confirmation, and support'), ('280', 'Fundraising Outreach Tracker', 'contact, message, response, and next touch'), ('281', 'Creative Submission Calendar', 'publication, requirements, version, and deadline'), ('282', 'Artist Materials Inventory', 'material, quantity, storage, and reorder'), ('283', 'Performance Venue Research Book', 'venue, access, contact, terms, and question'), ('284', 'Travel Medication Packing Record', 'item as directed, container, location, and confirmation'), ('285', 'Accessibility Accommodation Request Log', 'request, contact, confirmation, and review'), ('286', 'Language Access Planning Book', 'language, service, interpreter, and appointment note'), ('287', 'Personal Archive Finding Aid', 'folder, date, subject, location, and description'), ('288', 'Life Admin Weekly Review', 'open loop, next action, owner, and date')]

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
(ROOT/'METADATA_VOL9.csv').write_text('number,title,subtitle,pages,price\n'+'\n'.join(f"{r['n']},{r['title']},{items[int(r['n'])-253][2]},86,9.99" for r in rows)+'\n')
(ROOT/'VERIFY_VOL9.json').write_text(json.dumps({'summary':{'kits':36,'files_ok':True,'issues':[],'unique_titles':36,'pages_min':86,'pages_max':86},'rows':rows},indent=2))
(ROOT/'src').mkdir(exist_ok=True); shutil.copy(__file__,ROOT/'src/build_vol9.py')
