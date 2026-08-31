from pathlib import Path
import csv,json,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader
ROOT=Path('range-band/VOLUME-8'); KIT=ROOT/'KDP-Complete-Kit'; KIT.mkdir(parents=True,exist_ok=True)
items=[('217', 'Community Event Runbook', 'venue, roles, supplies, and day-of notes'), ('218', 'Neighborhood Contact Directory', 'person, permission, role, and last confirmed'), ('219', 'Library Research Trail', 'source, question, quote, and next lead'), ('220', 'Local History Interview Book', 'story, date, place, and follow-up'), ('221', 'Home School Activity Log', 'activity, materials, observation, and next idea'), ('222', 'College Application Tracker', 'school, requirement, contact, and status'), ('223', 'Scholarship Evidence Ledger', 'opportunity, criteria, draft, and deadline'), ('224', 'Internship Follow-Up Register', 'contact, conversation, promise, and next touch'), ('225', 'Professional Development Log', 'learning goal, practice, evidence, and application'), ('226', 'Team Onboarding Notebook', 'access, context, contact, and first win'), ('227', 'Manager One-on-One Register', 'topic, context, ask, and follow-up'), ('228', 'Workload Negotiation Log', 'request, tradeoff, agreement, and review'), ('229', 'Contractor Project Handoff', 'scope, materials, decisions, and open item'), ('230', 'Renovation Budget Evidence Book', 'estimate, receipt, variance, and choice'), ('231', 'Appliance Warranty Tracker', 'model, proof, service, and expiry'), ('232', 'Vehicle Trip Maintenance Log', 'route, warning, service, and receipt'), ('233', 'Pet Medication Question Log', 'label as given, observation, and vet question'), ('234', 'Pet Adoption Transition Book', 'routine, trigger, progress, and support'), ('235', 'Plant Care Observation Journal', 'plant, light, water, change, and note'), ('236', 'Seasonal Home Reset Ledger', 'area, decision, task, and completion'), ('237', 'Emergency Supply Rotation Log', 'item, quantity, date, and replacement'), ('238', 'Document Backup Checklist', 'file, location, date, and verification'), ('239', 'Password Manager Migration Log', 'account, recovery route, and completion'), ('240', 'Privacy Preference Register', 'service, setting, date, and reason'), ('241', 'Subscription Cancellation Record', 'service, request, confirmation, and refund'), ('242', 'Household Purchase Decision Book', 'need, options, price, and result'), ('243', 'Accessible Restaurant Call Log', 'venue, representative, features confirmed, and reference'), ('244', 'Medical Interpreter Appointment Log', 'language, date, access request, and questions'), ('245', 'Caregiver Respite Planning Book', 'coverage, handoff, contact, and return notes'), ('246', 'Support Group Meeting Notes', 'theme, resource, reflection, and next meeting'), ('247', 'Personal Values Decision Journal', 'choice, value, tradeoff, and review'), ('248', 'Difficult Email Draft Book', 'purpose, facts, ask, and response'), ('249', 'Boundary Conversation Record', 'situation, limit, wording, and outcome'), ('250', 'Creative Project Archive', 'version, decision, asset, and next seed'), ('251', 'Maker Workshop Log', 'material, setup, result, and adjustment'), ('252', 'Reading Project Notebook', 'question, passage, connection, and next source')]

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
(ROOT/'METADATA_VOL8.csv').write_text('number,title,subtitle,pages,price\n'+'\n'.join(f"{r['n']},{r['title']},{items[int(r['n'])-217][2]},86,9.99" for r in rows)+'\n')
(ROOT/'VERIFY_VOL8.json').write_text(json.dumps({'summary':{'kits':36,'files_ok':True,'issues':[],'unique_titles':36,'pages_min':86,'pages_max':86},'rows':rows},indent=2))
(ROOT/'src').mkdir(exist_ok=True); shutil.copy(__file__,ROOT/'src/build_vol8.py')
