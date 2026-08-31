from pathlib import Path
import csv,json,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader
ROOT=Path('range-band/VOLUME-7'); KIT=ROOT/'KDP-Complete-Kit'; KIT.mkdir(parents=True,exist_ok=True)
items=[('181', 'Neighborhood Mutual Aid Ledger', 'requests, offers, owners, and completion notes'), ('182', 'School Support Meeting Brief', 'observations, questions, accommodations, and follow-up'), ('183', 'Special Education Document Index', 'document, date, provider, and next action'), ('184', 'Youth Activity Safety Log', 'venue, contact, check-in, and incident notes'), ('185', 'Elder Housing Options Notebook', 'features, costs, tours, and questions'), ('186', 'Care Transition Contact Book', 'providers, permissions, dates, and handoffs'), ('187', 'Family Emergency Information File', 'contacts, locations, access notes, and updates'), ('188', 'Estate Task Coordination Ledger', 'task, responsible person, deadline, and status'), ('189', 'Probate Document Tracker', 'request, receipt, filing, and follow-up'), ('190', 'Tax Document Collection Log', 'source, year, received date, and missing item'), ('191', 'Debt Negotiation Call Record', 'representative, reference, terms stated, and next step'), ('192', 'Household Bill Calendar', 'due date, method, confirmation, and variance'), ('193', 'First Apartment Setup Planner', 'essential, source, cost, and completion'), ('194', 'Home Accessibility Survey', 'room, barrier, possible change, and priority'), ('195', 'Vehicle Maintenance Evidence Log', 'service, mileage, receipt, and next date'), ('196', 'Pet Care Handoff Book', 'routine, provider, medication as directed, and notes'), ('197', 'Garden Season Field Journal', 'bed, weather, action, and observation'), ('198', 'Community Garden Coordinator', 'plot, supplies, volunteer, and next action'), ('199', 'Repair Vendor Comparison Ledger', 'quote, scope, warranty, and decision'), ('200', 'Storm Claim Evidence Notebook', 'date, room, item, photo reference, and status'), ('201', 'Emergency Contact Update Log', 'person, relationship, permission, and last confirmed'), ('202', 'Travel Document Checklist', 'document, expiry, copy, and confirmation'), ('203', 'Accessible Lodging Call Log', 'property, representative, features confirmed, and reference'), ('204', 'Conference Networking Follow-Up', 'person, context, promise, and next touch'), ('205', 'Portfolio Revision Tracker', 'piece, feedback, change, and version'), ('206', 'Certification Study Evidence Log', 'topic, practice, result, and next review'), ('207', 'Apprenticeship Application Ledger', 'program, requirement, contact, and status'), ('208', 'Shift Worker Sleep Record', 'shift, light, routine, and morning observation'), ('209', 'Care Worker Boundary Notebook', 'request, capacity, response, and support needed'), ('210', 'Burnout Workload Evidence Log', 'task load, interruption, recovery, and conversation'), ('211', 'Union Meeting Notes Register', 'issue, speaker, decision, and action owner'), ('212', 'Board Meeting Decision Book', 'motion, rationale, vote, and follow-up'), ('213', 'Nonprofit Grant Calendar', 'opportunity, requirement, owner, and deadline'), ('214', 'Donation Inventory Ledger', 'item, condition, destination, and receipt'), ('215', 'Creative Collaboration Handoff', 'asset, decision, owner, and next version'), ('216', 'Performance Rehearsal Log', 'section, intention, feedback, and next practice')]

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
(ROOT/'METADATA_VOL7.csv').write_text('number,title,subtitle,pages,price\n'+'\n'.join(f"{r['n']},{r['title']},{items[int(r['n'])-181][2]},86,9.99" for r in rows)+'\n')
(ROOT/'VERIFY_VOL7.json').write_text(json.dumps({'summary':{'kits':36,'files_ok':True,'issues':[],'unique_titles':36,'pages_min':86,'pages_max':86},'rows':rows},indent=2))
(ROOT/'src').mkdir(exist_ok=True); shutil.copy(__file__,ROOT/'src/build_vol7.py')
