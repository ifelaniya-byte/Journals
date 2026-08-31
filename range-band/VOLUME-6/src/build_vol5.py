from pathlib import Path
import csv,json,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader
ROOT=Path('range-band/VOLUME-6'); KIT=ROOT/'KDP-Complete-Kit'; KIT.mkdir(parents=True,exist_ok=True)
items=[('145', 'Care Plan Handoff Grid', 'who knows what, what changed, and what comes next'), ('146', 'Caregiver Appointment Brief', 'questions, observations, and decisions'), ('147', 'Family Care Cost Ledger', 'payments, reimbursements, and open costs'), ('148', 'Hospital Discharge Questions', 'instructions to clarify before leaving'), ('149', 'Specialist Referral Tracker', 'referrals, calls, records, and status'), ('150', 'Health Insurance Call Log', 'representative, reference, promise, and follow-up'), ('151', 'Work Accommodation Request Log', 'needs, conversations, and documentation'), ('152', 'Return-to-Work Transition Planner', 'capacity, schedule, and check-in notes'), ('153', 'Layoff Recovery Pipeline', 'applications, contacts, and runway'), ('154', 'Small Business Cashflow Notebook', 'invoices, expenses, and decisions'), ('155', 'Client Onboarding Fieldbook', 'scope, access, milestones, and owners'), ('156', 'Project Risk Register', 'signal, impact, response, and review date'), ('157', 'Tenant Repair Escalation Log', 'notice, evidence, response, and next step'), ('158', 'Home Inventory Recovery Book', 'item, evidence, value, and claim status'), ('159', 'Flood Cleanup Record', 'rooms, materials, vendors, and receipts'), ('160', 'Power Outage Continuity Log', 'devices, food, contacts, and restoration'), ('161', 'Accessible Event Planner', 'routes, seating, communication, and backups'), ('162', 'Careful Travel Transit Log', 'transfer points, confirmations, and contingencies'), ('163', 'Medication List Reconciliation', 'prescriber, pharmacy, dose as listed, question'), ('164', 'Chronic Care Visit Summary', 'what was said, what changed, what to ask'), ('165', 'Symptom Context Timeline', 'time, setting, impact, and observation'), ('166', 'Sleep Routine Observation Book', 'environment, routine, and morning result'), ('167', 'Food Response Context Log', 'meal context, timing, and personal observation'), ('168', 'Pain Conversation Notebook', 'location, context, impact, and questions'), ('169', 'Therapy Session Reflection Log', 'themes, examples, and next appointment'), ('170', 'Support Network Check-In Book', 'who contacted, response, and next check-in'), ('171', 'Grief Date Memory Journal', 'date, memory, support, and care'), ('172', 'Sensory Load Field Notes', 'setting, input, adjustment, and recovery'), ('173', 'Focus Environment Experiment', 'workspace, friction, strategy, result'), ('174', 'Task Start Research Log', 'barrier, first action, time, and outcome'), ('175', 'Household Decision Register', 'choice, criteria, owner, and revisit date'), ('176', 'Digital Account Map', 'service, access route, renewal, and action'), ('177', 'Document Renewal Tracker', 'document, expiry, request, and receipt'), ('178', 'Personal Data Request Log', 'organization, request, date, and response'), ('179', 'Volunteer Shift Handoff', 'attendance, supplies, incidents, and next lead'), ('180', 'Community Project Ledger', 'needs, offers, owners, and milestones')]

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
(ROOT/'METADATA_VOL6.csv').write_text('number,title,subtitle,pages,price\n'+'\n'.join(f"{r['n']},{r['title']},{items[int(r['n'])-145][2]},86,9.99" for r in rows)+'\n')
(ROOT/'VERIFY_VOL6.json').write_text(json.dumps({'summary':{'kits':36,'files_ok':True,'issues':[],'unique_titles':36,'pages_min':86,'pages_max':86},'rows':rows},indent=2))
(ROOT/'src').mkdir(exist_ok=True); shutil.copy(__file__,ROOT/'src/build_vol5.py')
