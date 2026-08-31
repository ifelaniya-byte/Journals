"""Generate The Ritual Library production-batch interiors, cover-wrap drafts, and deluxe component files.

Outputs are locally author-attributed provisional content/layout PDFs. Before release, a named human must approve identity and any URL/QR route, obtain legal/claims review, and validate every KDP wrap against the current Cover Calculator.
"""
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from pathlib import Path
from datetime import date
import math, textwrap, json

ROOT = Path('/home/user/ritual-library-production-batch')
KDP = ROOT / 'kdp-scouts'
DELUXE = ROOT / 'deluxe-heroes'
SOURCE = ROOT / 'source'
for d in [KDP, DELUXE, SOURCE]: d.mkdir(parents=True, exist_ok=True)

# KDP scout specification — black-and-white interiors on white paper
TRIM_W, TRIM_H = 6*inch, 8*inch
MARGIN_X, TOP, BOTTOM = .55*inch, .56*inch, .52*inch
# Greys only in interiors: keeps scout interiors appropriate for black-and-white KDP print.
INK = colors.Color(.14,.14,.14)
MID = colors.Color(.38,.38,.38)
LIGHT = colors.Color(.72,.72,.72)
FAINT = colors.Color(.90,.90,.90)
PAPER = colors.white
AUTHOR = 'Arden Vellor'  # owner-directed provisional local attribution; not public-use clearance

PALETTE = {
    'dose': {'bg':'20313D', 'accent':'A4C3B2', 'sub':'DDE8E0'},
    'softer': {'bg':'49354A', 'accent':'E3B4A5', 'sub':'F5E6E1'},
    'back': {'bg':'35443A', 'accent':'D8B887', 'sub':'EDE6D8'},
    'rest': {'bg':'294A52', 'accent':'A7D2D0', 'sub':'E2F2F0'},
    'night': {'bg':'172338', 'accent':'C8CEE8', 'sub':'E8EAF5'},
    'money': {'bg':'443C2B', 'accent':'E6C778', 'sub':'FAF0D0'},
    'pocket': {'bg':'314944', 'accent':'D7AE86', 'sub':'F3E7D9'},
}

class JournalPDF:
    def __init__(self, path, title, subtitle, size=(TRIM_W,TRIM_H), grayscale=True):
        self.path = str(path)
        self.c = canvas.Canvas(self.path, pagesize=size, pageCompression=1)
        self.w, self.h = size
        self.title = title
        self.subtitle = subtitle
        self.count = 0
        self.grayscale = grayscale

    def page_frame(self, section='', number=True):
        c=self.c
        c.setFillColor(PAPER); c.rect(0,0,self.w,self.h,fill=1,stroke=0)
        c.setStrokeColor(FAINT); c.setLineWidth(.35)
        c.line(MARGIN_X, self.h-TOP+.05*inch, self.w-MARGIN_X, self.h-TOP+.05*inch)
        c.setFont('Helvetica', 7.2); c.setFillColor(MID)
        c.drawString(MARGIN_X, self.h-TOP+.14*inch, section.upper() if section else self.title.upper())
        if number and self.count>0:
            c.drawRightString(self.w-MARGIN_X, BOTTOM-.13*inch, str(self.count+1))
        c.setStrokeColor(FAINT); c.line(MARGIN_X, BOTTOM, self.w-MARGIN_X, BOTTOM)

    def end(self):
        self.c.showPage(); self.count += 1

    def title_page(self, color_name='dose', author=AUTHOR):
        c=self.c; pal=PALETTE[color_name]
        c.setFillColor(HexColor('#'+pal['bg']));c.rect(0,0,self.w,self.h,fill=1,stroke=0)
        # restrained arcs
        c.setStrokeColor(HexColor('#'+pal['accent']));c.setLineWidth(1.2)
        for r in [1.25, 1.62, 1.99]:
            c.circle(self.w*.79,self.h*.76,r*inch,stroke=1,fill=0)
        c.setFillColor(colors.white);c.setFont('Helvetica-Bold',24)
        draw_centered(c,self.title,self.w/2,self.h*.58,24,colors.white,'Helvetica-Bold',max_width=self.w-1.1*inch)
        c.setFillColor(HexColor('#'+pal['sub']));
        draw_centered(c,self.subtitle,self.w/2,self.h*.49,11,HexColor('#'+pal['sub']),'Helvetica',max_width=self.w-1.15*inch,leading=14)
        if author:
            c.setFont('Helvetica',9);c.setFillColor(colors.white);c.drawCentredString(self.w/2,self.h*.23,author)
        c.setFont('Helvetica',7);c.setFillColor(HexColor('#'+pal['sub']));c.drawCentredString(self.w/2,.54*inch,'THE RITUAL LIBRARY')
        self.end()

    def copyright_page(self, disclaimer, extra=''):
        self.page_frame('Before you begin',number=False)
        c=self.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(MARGIN_X,self.h-TOP-.28*inch,'A note before you begin')
        y=self.h-TOP-.65*inch
        y=draw_paragraph(c, disclaimer, MARGIN_X,y,self.w-2*MARGIN_X,10,13,INK)
        if extra:
            y-=.20*inch; y=draw_paragraph(c,extra,MARGIN_X,y,self.w-2*MARGIN_X,9,12,MID)
        y-=.5*inch;c.setStrokeColor(LIGHT);c.line(MARGIN_X,y,self.w-MARGIN_X,y)
        c.setFont('Helvetica',8);c.setFillColor(MID);c.drawString(MARGIN_X,y-.28*inch,f'Copyright © 2026 {AUTHOR}. All rights reserved.')
        self.end()

    def section_page(self, eyebrow, heading, body, number=False):
        self.page_frame(eyebrow,number=number)
        c=self.c;c.setFillColor(INK)
        c.setFont('Helvetica-Bold',8);c.setFillColor(MID);c.drawString(MARGIN_X,self.h-TOP-.22*inch,eyebrow.upper())
        y=self.h-TOP-.63*inch
        y=draw_wrapped_heading(c,heading,MARGIN_X,y,self.w-2*MARGIN_X,20,24,INK)
        y-=.18*inch;draw_paragraph(c,body,MARGIN_X,y,self.w-2*MARGIN_X,10.2,14,INK)
        self.end()

    def ruled_notes(self, title='Notes', prompt='Use this page in any way that helps.', lines=18, section='Notes'):
        self.page_frame(section)
        c=self.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(MARGIN_X,self.h-TOP-.32*inch,title)
        c.setFillColor(MID);c.setFont('Helvetica-Oblique',8.5);c.drawString(MARGIN_X,self.h-TOP-.52*inch,prompt)
        y=self.h-TOP-.86*inch;c.setStrokeColor(FAINT);c.setLineWidth(.35)
        for _ in range(lines):
            c.line(MARGIN_X,y,self.w-MARGIN_X,y);y-=.27*inch
        self.end()

    def check_in(self, title, fields, prompt='', section='Check-in'):
        self.page_frame(section)
        c=self.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,self.h-TOP-.3*inch,title)
        if prompt:
            c.setFont('Helvetica-Oblique',8.8);c.setFillColor(MID);draw_paragraph(c,prompt,MARGIN_X,self.h-TOP-.52*inch,self.w-2*MARGIN_X,8.8,11,MID)
        y=self.h-TOP-.93*inch
        for label,lines in fields:
            c.setFillColor(INK);c.setFont('Helvetica-Bold',9.2);c.drawString(MARGIN_X,y,label)
            y-=.18*inch;c.setStrokeColor(FAINT);c.setLineWidth(.35)
            for _ in range(lines):
                c.line(MARGIN_X,y,self.w-MARGIN_X,y);y-=.25*inch
            y-=.08*inch
        self.end()


def wrap_lines(c,text,font,size,max_width):
    words=text.replace('\n',' \n ').split(' '); lines=[];cur=''
    for word in words:
        if word=='\n':
            lines.append(cur);cur='';continue
        test=(cur+' '+word).strip()
        if stringWidth(test,font,size)<=max_width or not cur:cur=test
        else:lines.append(cur);cur=word
    if cur:lines.append(cur)
    return lines

def draw_paragraph(c,text,x,y,max_width,size=10,leading=13,color=INK,font='Helvetica'):
    c.setFont(font,size);c.setFillColor(color)
    for line in wrap_lines(c,text,font,size,max_width):
        c.drawString(x,y,line);y-=leading
    return y

def draw_wrapped_heading(c,text,x,y,max_width,size=20,leading=24,color=INK):
    c.setFont('Helvetica-Bold',size);c.setFillColor(color)
    for line in wrap_lines(c,text,'Helvetica-Bold',size,max_width):
        c.drawString(x,y,line);y-=leading
    return y

def draw_centered(c,text,cx,y,size,color,font='Helvetica',max_width=None,leading=None):
    max_width=max_width or 9999;leading=leading or size*1.2
    lines=wrap_lines(c,text,font,size,max_width)
    c.setFont(font,size);c.setFillColor(color)
    offset=(len(lines)-1)*leading/2
    for i,line in enumerate(lines):c.drawCentredString(cx,y+offset-i*leading,line)

def label_line(c,label,x,y,width,lines=1):
    c.setFillColor(INK);c.setFont('Helvetica-Bold',8.6);c.drawString(x,y,label)
    y-=.16*inch;c.setStrokeColor(FAINT);c.setLineWidth(.35)
    for _ in range(lines):c.line(x,y,x+width,y);y-=.23*inch
    return y

def checkbox(c,x,y,label):
    c.setStrokeColor(MID);c.rect(x,y-7,7,7,fill=0,stroke=1);c.setFillColor(INK);c.setFont('Helvetica',8);c.drawString(x+12,y-5,label)

# Editorial content
DISCLAIMERS = {
'dose': 'This journal is a personal reflection tool for adults using prescribed GLP-1 medication. It does not provide dosing, injection, nutrition, exercise, or medical advice. Follow the instructions supplied by your prescriber and pharmacist, and bring health questions or concerning symptoms to an appropriate professional. In an emergency, seek urgent help.',
'softer': 'This diary is for personal reflection. It is not psychotherapy, crisis support, medical care, or a substitute for support from a qualified professional. Skip any prompt that feels unhelpful and seek appropriate help when needed.',
'back': 'This workbook offers gentle planning and self-reflection. It does not diagnose or treat burnout, depression, anxiety, or any medical or workplace condition. Adapt, pause, or seek professional support as needed.',
'rest': 'This planner offers optional grounding and paced-breathing practices for personal reflection. It does not treat anxiety, change the nervous system, improve HRV, or replace medical or mental-health care. Choose a natural, comfortable breath; stop any practice that feels unpleasant.',
'night': 'This journal is a wind-down and reflection tool. It does not diagnose or treat sleep conditions or give medical advice. If sleep changes, symptoms, or distress are concerning, speak with an appropriate health professional.',
'money': 'This workbook supports personal reflection about money feelings and choices. It is not financial, legal, tax, investment, or mental-health advice. Consult qualified professionals for decisions that require them.',
'pocket': 'This book and deck are personal reflection tools. They are not therapy, medical care, diagnosis, crisis support, or a substitute for professional advice. Skip any prompt that does not fit; seek appropriate professional or urgent support when needed.'
}

DOSE_WEEK_PROMPTS=[
'What would make this week feel a little more manageable?',
'What is one cue that helps me return to the present?',
'What kind of support would make the next few days gentler?',
'What does “enough” look like for me this week?',
'What did my body ask for that I can listen to with curiosity?',
'What can I simplify before I try to optimize anything?',
'Where can I make room for a slower answer?',
'What is already helping, even a little?',
'What is one kind sentence I can practice believing?',
'What might I bring up with my care team, if anything?',
'What would feel like a realistic act of care today?',
'What am I allowed to stop carrying this week?',
'What helps me feel accompanied rather than assessed?',
'What small comfort is available without earning it?',
'What is one thing I can notice without needing to judge it?',
'What would a supportive schedule look like this week?',
'What is a signal that I need more rest or help?',
'What does progress mean beyond a number?',
'What can I celebrate quietly?',
'What would make this appointment, errand, or routine easier?',
'What does a good-enough meal or moment of rest look like?',
'Who could I let in, even a little?',
'What is a boundary that protects my energy?',
'How can I make the next step smaller?',
'What is one thing I want to remember about myself?',
'What will I thank myself for next week?'
]

SOFTER_PROMPTS=[
'What felt tender today?', 'What did I do with care, even if no one saw it?',
'What is one sentence I wish I could hear?', 'Where did I make room for myself?',
'What did I survive, soften, or begin?', 'What deserves less judgment from me?',
'What moment was ordinary and still good?', 'What can be true without being fixed tonight?',
'How did I protect my energy?', 'What did I notice with curiosity?',
'What would “kind enough” sound like here?', 'What brought even a flicker of ease?',
'What did my future self need from me today?', 'What can I release from the story of this day?',
'What am I learning to trust?', 'Where did I choose gentleness over perfection?',
'What would I tell someone I love in this exact moment?', 'What is one small proof that I kept going?',
]

BACK_DAILY=[
'What is the smallest version of today that still counts?', 'What must happen, what could happen, and what can wait?',
'Where is my capacity right now—low, medium, or generous?', 'What is one task I can make easier before I start?',
'What would a 10-minute reset change?', 'What can be delegated, delayed, deleted, or done imperfectly?',
'What boundary would protect my next hour?', 'What is the actual next physical action?',
'What is not mine to solve today?', 'What deserves a “not now” instead of a “never”?',
'What did I finish that I almost failed to count?', 'What would make tomorrow less heavy?',
]

REST_PROMPTS=[
'Name three things you can see. What changes when you let your eyes rest on one?',
'Let your exhale be unforced. What is one word for how you arrive?',
'Notice your hands. Are they holding, resting, warming, moving?',
'Look for one neutral thing, not a positive thing. What is simply here?',
'If your shoulders could send a note, what would it say?',
'Choose a pace that feels natural. What helps you feel less rushed?',
'What sound is closest? What sound is farthest away?',
'What is one permission you can give yourself for the next hour?',
'Feel the support under you. What is holding you up right now?',
'Name a place or person that helps you feel more settled.',
'Where could you create two inches more space—in your schedule or posture?',
'What is one ordinary comfort you can choose on purpose?',
]

NIGHT_PROMPTS=[
'Today is over enough for now.', 'What can wait until morning?', 'What helped you feel a little more at home in your day?',
'What is one thing you do not need to solve in bed?', 'What would make the room feel softer?',
'What can you thank your body for carrying?', 'What is one thought you can set on the page instead of carrying to sleep?',
'What does a gentle tomorrow need from tonight?', 'Where did you find a small pause?',
'What would “no more for today” sound like?', 'What was one sensory moment worth remembering?', 'What can become smaller now?'
]

MONEY_PROMPTS=[
'What happened, in plain facts?', 'What story did my mind add to those facts?',
'What feeling wants acknowledgement before a decision?', 'What is one next step I can take without solving everything?',
'What does “enough information for now” look like?', 'What value do I want this choice to serve?',
'What conversation might reduce uncertainty?', 'What can I postpone until I am calmer?',
'What is within my control this week?', 'What support or resource would be useful to find?',
'What cost am I afraid to name?', 'What is a kinder interpretation of my own financial learning curve?',
]

# Common page builders
def dose_week(j, n, prompt, deluxe=False):
    j.page_frame('Weekly ritual')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.30*inch,f'Week {n} · arrive before you begin')
    c.setFont('Helvetica',8.5);c.setFillColor(MID);c.drawString(MARGIN_X,j.h-TOP-.51*inch,'Optional routine notes only. Follow your prescriber’s guidance for medication questions.')
    y=j.h-TOP-.86*inch
    y=label_line(c,'DATE / ROUTINE NOTE',MARGIN_X,y,j.w-2*MARGIN_X,1)
    y-=.02*inch;y=label_line(c,'HOW I FEEL ARRIVING',MARGIN_X,y,j.w-2*MARGIN_X,2)
    y-=.02*inch;y=label_line(c,'A QUESTION OR OBSERVATION FOR MY CARE TEAM',MARGIN_X,y,j.w-2*MARGIN_X,2)
    # boxed breath visual
    bx=MARGIN_X;by=.88*inch;side=.58*inch;c.setStrokeColor(MID);c.setLineWidth(.9)
    for ix in range(4):
        for iy in range(4):
            c.setFillColor(colors.white);c.rect(bx+ix*side,by+iy*side,side,side,fill=1,stroke=1)
    c.setFont('Helvetica-Bold',8);c.setFillColor(INK);c.drawString(bx,by+4*side+.12*inch,'FOUR-COUNT BOX BREATH · optional')
    c.setFont('Helvetica',7.8);c.setFillColor(MID);c.drawString(bx+4*side+.18*inch,by+4*side+.12*inch,'Inhale · pause · exhale · pause')
    j.end()
    j.page_frame('Weekly ritual')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',14);c.drawString(MARGIN_X,j.h-TOP-.30*inch,'Notice, soothe, continue')
    c.setFillColor(MID);c.setFont('Helvetica-Oblique',9);draw_paragraph(c,'“'+prompt+'”',MARGIN_X,j.h-TOP-.55*inch,j.w-2*MARGIN_X,9,12,MID)
    y=j.h-TOP-.95*inch
    for label,lines in [('HYDRATION / COMFORT NOTES',2),('ENERGY / REST NOTES',2),('ONE THING THAT SUPPORTED ME',2),('ONE KIND NEXT STEP',2)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.04*inch
    j.end()

def monthly_reflection(j,n,kind='month'):
    j.page_frame('Pattern page')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.3*inch,f'{kind.title()} {n} · patterns, not verdicts')
    y=j.h-TOP-.7*inch
    for label,lines in [('WHAT FELT SUPPORTIVE?',3),('WHAT FELT HARD OR UNCLEAR?',3),('WHAT DO I WANT TO ASK, ADJUST, OR REMEMBER?',3),('ONE WAY I CAN MAKE NEXT MONTH GENTLER',2)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.05*inch
    j.end()

def daily_gratitude(j,day,prompt):
    j.page_frame('Daily softening')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.31*inch,f'Day {day}')
    c.setFont('Helvetica-Oblique',9.5);c.setFillColor(MID);draw_paragraph(c,'“'+prompt+'”',MARGIN_X,j.h-TOP-.55*inch,j.w-2*MARGIN_X,9.5,12,MID)
    y=j.h-TOP-.94*inch
    for label,lines in [('WHAT FELT HARD?',3),('WHAT DID I DO WITH CARE?',3),('A KIND SENTENCE I CAN BELIEVE',2),('ONE SMALL GRATITUDE',2)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.05*inch
    j.end()

def back_day(j,day,prompt):
    j.page_frame('Capacity planner')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.30*inch,f'Day {day} · rescue the day, not the whole life')
    c.setFont('Helvetica-Oblique',9);c.setFillColor(MID);draw_paragraph(c,'“'+prompt+'”',MARGIN_X,j.h-TOP-.54*inch,j.w-2*MARGIN_X,9,12,MID)
    y=j.h-TOP-.9*inch
    c.setFont('Helvetica-Bold',8);c.setFillColor(INK);c.drawString(MARGIN_X,y,'CAPACITY TODAY')
    checkbox(c,MARGIN_X,y-.12*inch,'low');checkbox(c,MARGIN_X+1.1*inch,y-.12*inch,'medium');checkbox(c,MARGIN_X+2.45*inch,y-.12*inch,'generous')
    y-=.48*inch
    for label,lines in [('MUST HAPPEN',2),('COULD HAPPEN',2),('CAN WAIT / DELEGATE / DELETE',2),('A 10-MINUTE RESET',1),('ONE WIN I WILL COUNT',1)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.04*inch
    j.end()

def rest_day(j,day,prompt):
    j.page_frame('Daily practice')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.30*inch,f'Day {day} · a small return')
    c.setFont('Helvetica-Oblique',9);c.setFillColor(MID);draw_paragraph(c,'“'+prompt+'”',MARGIN_X,j.h-TOP-.55*inch,j.w-2*MARGIN_X,9,12,MID)
    y=j.h-TOP-.92*inch
    c.setFont('Helvetica-Bold',8);c.setFillColor(INK);c.drawString(MARGIN_X,y,'CHOOSE A GENTLE PRACTICE')
    y-=.18*inch
    checkbox(c,MARGIN_X,y,'look around slowly');checkbox(c,MARGIN_X+2.0*inch,y,'lengthen the exhale');
    y-=.27*inch;checkbox(c,MARGIN_X,y,'feel my feet / support');checkbox(c,MARGIN_X+2.0*inch,y,'take a brief pause')
    y-=.38*inch
    for label,lines in [('BEFORE: WHAT AM I NOTICING?',2),('AFTER: WHAT, IF ANYTHING, SHIFTED?',2),('ONE KIND NEXT STEP',2),('NOTES',3)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.04*inch
    j.end()

def night_page(j,day,prompt):
    j.page_frame('Evening and morning')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.30*inch,f'Night {day} · a small landing place')
    c.setFont('Helvetica-Oblique',9);c.setFillColor(MID);draw_paragraph(c,'“'+prompt+'”',MARGIN_X,j.h-TOP-.55*inch,j.w-2*MARGIN_X,9,12,MID)
    y=j.h-TOP-.93*inch
    for label,lines in [('EVENING · WHAT I AM READY TO SET DOWN',3),('WIND-DOWN I CHOSE',1),('MORNING · HOW REST FELT',2),('ONE GENTLE INTENTION',2),('PATTERN / QUESTION TO REMEMBER',2)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.04*inch
    j.end()

def money_day(j,day,prompt):
    j.page_frame('Calm money practice')
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',15);c.drawString(MARGIN_X,j.h-TOP-.30*inch,f'Practice {day} · facts before fear')
    c.setFont('Helvetica-Oblique',9);c.setFillColor(MID);draw_paragraph(c,'“'+prompt+'”',MARGIN_X,j.h-TOP-.55*inch,j.w-2*MARGIN_X,9,12,MID)
    y=j.h-TOP-.93*inch
    for label,lines in [('THE FACTS I KNOW',3),('THE STORY MY MIND IS ADDING',3),('WHAT I FEEL IN MY BODY / EMOTIONS',2),('ONE SMALL, CONCRETE NEXT STEP',2),('WHO / WHAT COULD SUPPORT ME?',1)]:
        y=label_line(c,label,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.04*inch
    j.end()

# Individual interiors
def build_dose(path,deluxe=False):
    j=JournalPDF(path,'Dose & Breathe','A mindful weekly companion for your GLP-1 journey')
    j.title_page('dose')
    j.copyright_page(DISCLAIMERS['dose'],'Use only the pages that serve you. Blank space is a complete entry.')
    j.section_page('Welcome','This is a ritual, not a report card.','Before a routine, appointment, or difficult week, pause. Notice what is here. Choose one small thing that helps. Keep only what is useful.')
    j.check_in('My support map',[('MY CARE TEAM / IMPORTANT CONTACTS',4),('WHAT I WANT TO REMEMBER ABOUT MY PREFERENCES',4)],'This page is for your own notes. It is not a replacement for medical instructions.','My support map')
    j.section_page('How to use','A two-minute weekly rhythm.','On the first page, make an optional routine note and follow the box-breath visual only if it feels comfortable. On the second, notice comfort, rest, support, and one kind next step.')
    j.check_in('My reasons for gentleness',[('WHAT I HOPE THIS JOURNAL MAKES EASIER',4),('WHAT I DO NOT WANT THIS JOURNAL TO BECOME',3),('A SENTENCE TO RETURN TO',2)],'You can revise these at any time.','Beginning')
    j.check_in('Personal compass',[('WHEN I FEEL OVERWHELMED, WHAT HELPS?',3),('WHEN I NEED SUPPORT, WHO OR WHAT CAN I TURN TO?',3),('A REMINDER I WANT TO KEEP CLOSE',2)],'There is no need to use every field.','Beginning')
    j.check_in('Before week one',[('WHAT WOULD “ENOUGH” LOOK LIKE THIS MONTH?',3),('WHAT AM I CURIOUS TO NOTICE?',3),('WHAT DO I WANT TO LEAVE OUT OF THIS JOURNAL?',2)],'Your data belongs to you. Curiosity is enough.','Beginning')
    weeks=26 if deluxe else 24
    for n in range(1,weeks+1):
        dose_week(j,n,DOSE_WEEK_PROMPTS[(n-1)%len(DOSE_WEEK_PROMPTS)],deluxe)
        if n%4==0 and n//4<=6:monthly_reflection(j,n//4,'month')
    extras=26 if deluxe else 20
    for n in range(extras):
        j.check_in('A gentle return', [('WHAT AM I NOTICING?',3),('WHAT WOULD HELP RIGHT NOW?',3),('ONE THING I CAN LET BE ENOUGH',2)], DOSE_WEEK_PROMPTS[n%len(DOSE_WEEK_PROMPTS)],'Return')
    notes=36 if deluxe else 40
    for n in range(notes):j.ruled_notes('Open notes','Use this space for questions, observations, or anything you want to set down.',section='Notes')
    # pad to desired even count
    target=160 if deluxe else 128
    while j.count<target:j.ruled_notes('Open notes','This page is yours.',section='Notes')
    if j.count%2:j.ruled_notes('Open notes','This page is yours.',section='Notes')
    j.c.save();return j.count

def build_softer(path):
    j=JournalPDF(path,'Softer Words','A gratitude and self-talk diary for ordinary hard days')
    j.title_page('softer')
    j.copyright_page(DISCLAIMERS['softer'],'This book makes room for the whole truth: gratitude and grief, progress and pause, tenderness and uncertainty.')
    j.section_page('Welcome','You do not have to earn a kinder voice.','This diary does not ask you to turn every day into a lesson. It asks only: what happened, what helped, and what sentence would make the day gentler to carry?')
    j.check_in('My believable affirmations',[('WORDS THAT FEEL TRUE ENOUGH TO PRACTICE',5),('WHAT I WANT MORE OF IN MY SELF-TALK',3)],'Try sentences that are kind and plausible, not grand.','Beginning')
    for day in range(1,91):
        daily_gratitude(j,day,SOFTER_PROMPTS[(day-1)%len(SOFTER_PROMPTS)])
        if day%7==0:
            j.check_in(f'Week {day//7} · evidence of care',[('WHAT I DID THAT MATTERED',3),('WHAT I WANT TO CARRY FORWARD',3),('A KIND PLAN FOR THE NEXT WEEK',2)],'Look for evidence, not perfection.','Weekly reflection')
    for m in range(1,7):monthly_reflection(j,m,'monthly letter')
    while j.count<128:j.ruled_notes('Free write','Nothing to perform here.',section='Notes')
    if j.count%2:j.ruled_notes('Free write','Nothing to perform here.',section='Notes')
    j.c.save();return j.count

def build_back(path):
    j=JournalPDF(path,'Back to Enough','A compassionate productivity rescue workbook')
    j.title_page('back')
    j.copyright_page(DISCLAIMERS['back'],'This workbook is designed for low-capacity days. You are invited to make the plan smaller until it becomes possible.')
    j.section_page('Welcome','When capacity is low, the answer is not more pressure.','Use these pages to decide what matters today, what can wait, and how to build a little recovery into the day you actually have.')
    j.check_in('My early signs',[('SIGNS I MAY NEED A SMALLER PLAN',4),('WHAT RESTORATION CAN LOOK LIKE FOR ME',4)],'Recognizing the signal early is a form of skill, not failure.','Starting point')
    j.section_page('The four moves','Delay. Delegate. Delete. Do imperfectly.','When a task feels immovable, try one of the four moves. This is not a test of willpower; it is an invitation to work with the resources you have.')
    for day in range(1,85):
        back_day(j,day,BACK_DAILY[(day-1)%len(BACK_DAILY)])
        if day%7==0:
            j.check_in(f'Week {day//7} · reset',[('WHAT DRAINED CAPACITY?',2),('WHAT RESTORED A LITTLE CAPACITY?',2),('WHAT WILL I PROTECT NEXT WEEK?',2),('ONE THING I CAN RELEASE',1)],'A review is information, not a verdict.','Weekly reset')
    for n in range(12):
        j.check_in('Mini-break plan',[('WHEN I NOTICE THIS CUE...',1),('I CAN TAKE THIS 2–10 MINUTE BREAK...',2),('I WILL RETURN WITH THIS ONE SMALL ACTION...',1)],'Tear-out cards belong in the deluxe edition; use this page as your paperback version.','Rescue card')
    while j.count<160:j.ruled_notes('Working notes','A place for the things that do not need to be solved right now.',section='Notes')
    if j.count%2:j.ruled_notes('Working notes','A place for the things that do not need to be solved right now.',section='Notes')
    j.c.save();return j.count

def build_rest(path):
    j=JournalPDF(path,'Rest & Regulate','A 90-day breath-paced planner for small returns')
    j.title_page('rest')
    j.copyright_page(DISCLAIMERS['rest'],'There is no perfect breath. Let the practices remain optional, easy, and adapted to the day you have.')
    j.section_page('Welcome','A practice can be small enough to keep.','This planner does not measure your calm. It gives you a place to notice: how did I arrive, what did I try, and what might support me next?')
    j.check_in('Choose your practices',[('PRACTICES I LIKE',3),('PRACTICES I PREFER TO SKIP OR ADAPT',3),('MY PERSONAL SIGNS OF “A LITTLE MORE SETTLED”',3)],'Breath holds are never required. A natural exhale, visual orientation, or a pause can be enough.','Practice menu')
    for day in range(1,91):
        rest_day(j,day,REST_PROMPTS[(day-1)%len(REST_PROMPTS)])
        if day%7==0:
            j.check_in(f'Week {day//7} · pattern page',[('WHAT SUPPORTED ME THIS WEEK?',2),('WHAT FELT LIKE TOO MUCH?',2),('A PRACTICE TO KEEP OR ADAPT',2),('ONE KIND NEXT STEP',1)],'Small, repeatable practices count.','Weekly reflection')
    while j.count<144:j.ruled_notes('Practice notes','A few words are enough.',section='Notes')
    if j.count%2:j.ruled_notes('Practice notes','A few words are enough.',section='Notes')
    j.c.save();return j.count

def build_night(path):
    j=JournalPDF(path,'Night Harbor','An evening wind-down and sleep reflection companion')
    j.title_page('night')
    j.copyright_page(DISCLAIMERS['night'],'Use this book as a bedside landing place. You do not need to complete a page for it to have done its job.')
    j.section_page('Welcome','Let the day end on paper.','Write one thought, choose one comfort, or simply read the prompt and close the book. The aim is not a perfect night; it is a gentler transition.')
    j.check_in('My wind-down menu',[('THINGS THAT HELP THE ROOM FEEL SOFTER',3),('THINGS I CAN DO IN TWO MINUTES OR LESS',3),('A NOTE FOR DIFFICULT NIGHTS',3)],'Keep this practical and personal: light, a glass of water, a page, a text, a pause.','Beginning')
    for day in range(1,85):
        night_page(j,day,NIGHT_PROMPTS[(day-1)%len(NIGHT_PROMPTS)])
        if day%7==0:
            j.check_in(f'Week {day//7} · morning light',[('WHAT FELT SUPPORTIVE AT NIGHT?',2),('WHAT FELT HARD OR UNCLEAR?',2),('WHAT WOULD I LIKE TO TRY OR ASK ABOUT?',2),('ONE THING I CAN KEEP SIMPLE',1)],'Notice patterns without turning them into a verdict.','Weekly reflection')
    while j.count<168:j.ruled_notes('Night notes','Leave a little room for the day to be over.',section='Notes')
    if j.count%2:j.ruled_notes('Night notes','Leave a little room for the day to be over.',section='Notes')
    j.c.save();return j.count

def build_money(path):
    j=JournalPDF(path,'Enough Money, Enough Calm','A financial-anxiety mindset workbook')
    j.title_page('money')
    j.copyright_page(DISCLAIMERS['money'],'You are allowed to slow down before reacting. This book separates facts, feelings, and next steps; it does not require a particular financial outcome.')
    j.section_page('Welcome','Money feelings deserve a steadier place to land.','Use this workbook before a money task, after a difficult conversation, or when a thought keeps looping. Begin with facts. Make the next step small. Ask for support where it belongs.')
    j.check_in('My calm-money supports',[('PEOPLE, TOOLS, OR RESOURCES I CAN TURN TO',4),('MONEY MOMENTS THAT TEND TO FEEL ACTIVATING',3),('A SENTENCE I WANT TO REMEMBER BEFORE I DECIDE',2)],'This page is not a budget or advice. It is a map of support.','Beginning')
    for day in range(1,61):
        money_day(j,day,MONEY_PROMPTS[(day-1)%len(MONEY_PROMPTS)])
        if day%10==0:
            j.check_in(f'Practice review {day//10}',[('WHAT I AM LEARNING ABOUT MY PATTERNS',3),('WHAT RESOURCE OR CONVERSATION WOULD HELP?',2),('A SMALL NEXT STEP I CAN SCHEDULE',2)],'Clarity can arrive in pieces.',section='Reflection')
    for m in range(1,7):
        j.check_in(f'Month {m} · clarity review',[('WHAT FACTS DO I WANT TO GATHER?',2),('WHAT FEELINGS NEED ROOM?',2),('WHAT DECISION, IF ANY, IS ACTUALLY NEXT?',2),('WHAT CAN WAIT?',1)],'Facts, feelings, and next steps can coexist.','Monthly review')
    while j.count<168:j.ruled_notes('Decision notes','Pause before panic. Write down only what helps.',section='Notes')
    if j.count%2:j.ruled_notes('Decision notes','Pause before panic. Write down only what helps.',section='Notes')
    j.c.save();return j.count

POCKET_FAMILIES = [
('ARRIVE','Notice your body and surroundings.'),
('SOFTEN','Practice a more humane sentence with yourself.'),
('NOURISH','Become curious about comfort and care.'),
('REACH','Name the support or boundary you need.'),
('CONTINUE','Recognize what is already working.'),
('RESET','Find one small next step on a hard day.'),
]
POCKET_PROMPTS = {
'ARRIVE':[
'Name three things in this room that make you feel a little more here.',
'Let your eyes land on one ordinary object. What do you notice about it?',
'Where is your body being supported right now?',
'What sound is closest? What sound is farthest away?',
'If you could give this moment a weather report, what would it be?',
'Notice your hands. What are they doing, holding, or asking for?',
'Name one thing that is true in this exact minute.',
'What changes when you lengthen only the exhale, naturally and without force?',
'What is one place you could make two inches more comfortable?'],
'SOFTEN':[
'What is one sentence you would rather hear than the one your inner critic is offering?',
'What would “kind enough” sound like here?',
'What would you say to someone you love in this exact moment?',
'What are you allowed to be learning?',
'Which expectation could become a request instead?',
'What deserves less judgment today?',
'What can be true without being fixed tonight?',
'What is one thing you did that was quietly difficult?',
'What would it mean to take your own side for five minutes?'],
'NOURISH':[
'What kind of comfort sounds possible, not perfect?',
'What sensory cue might help: warmth, water, air, texture, quiet, or movement?',
'What would make the next hour five percent gentler?',
'What have you been needing but postponing?',
'What is one ordinary thing that helps you feel more like yourself?',
'If care were practical today, what would it look like?',
'What would a good-enough pause include?',
'What do you want less of around you right now?',
'What is one small pleasure you do not have to earn?'],
'REACH':[
'What kind of support would make this lighter to carry?',
'Who could receive one honest sentence from you?',
'What boundary would protect your next hour?',
'What question could you ask instead of trying to guess?',
'What task is not yours to solve alone?',
'What would a clear “not today” make room for?',
'Where could you ask for help before you are at capacity?',
'What conversation needs a softer beginning?',
'What do you need someone else to understand about today?'],
'CONTINUE':[
'What has been helping, even a little?',
'What did you do today that you almost failed to count?',
'Where did you choose a sustainable pace?',
'What is one thing you have already survived or learned?',
'What would make progress feel less like a scoreboard?',
'What is worth repeating tomorrow?',
'What part of your routine is quietly working?',
'What did you notice with curiosity instead of judgment?',
'What is one reason to trust your ability to continue?'],
'RESET':[
'If today needed to be smaller, what could become optional?',
'What is the next physical action—not the whole project?',
'What can wait until you have more information or energy?',
'What can you set down for ten minutes?',
'What is one kind way to end this loop?',
'What needs a list, a timer, a glass of water, or a message?',
'What would you like the next hour to feel like?',
'What is one decision you do not have to make right now?',
'What would “enough for today” look like?']
}

def pocket_log_entry(j,index,family,prompt,deluxe=False):
    j.page_frame(family.title())
    c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',8);c.drawString(MARGIN_X,j.h-TOP-.22*inch,f'{family} · CARD {index:02d}')
    y=j.h-TOP-.63*inch;y=draw_wrapped_heading(c,prompt,MARGIN_X,y,j.w-2*MARGIN_X,16,20,INK)
    y-=.22*inch;c.setFillColor(MID);c.setFont('Helvetica-Oblique',8.8);c.drawString(MARGIN_X,y,'You can write one word, fill the page, speak the answer, or simply keep the card nearby.')
    y-=.37*inch
    for lab,lines in [('DATE / MOMENT',1),('WHAT I NOTICE',4),('WHAT WOULD HELP NEXT?',3)]:y=label_line(c,lab,MARGIN_X,y,j.w-2*MARGIN_X,lines);y-=.04*inch
    j.end()
    if deluxe:
        j.ruled_notes('More room','Use this page for a longer reflection—or leave it blank.',section='Reflection')

def build_pocket_kdp(path):
    j=JournalPDF(path,'Pocket of Calm','A guided journaling companion for small returns')
    j.title_page('pocket')
    j.copyright_page(DISCLAIMERS['pocket'],'The boxed deck is optional. This paperback companion includes all 54 prompts as a stand-alone journal.')
    j.section_page('Welcome','When a blank journal is too much, begin with one small question.','Choose a prompt at random, start with the family that fits, or read one and close the book. There is no streak to keep and no right answer to find.')
    j.check_in('How I want to use this',[('PLACES I MAY KEEP THIS BOOK',2),('PROMPTS OR MOMENTS I WANT TO RETURN TO',3),('A SENTENCE I WANT TO PRACTICE',2)],'You can use this book in five minutes or over many months.','Beginning')
    n=1
    for family,_ in POCKET_FAMILIES:
        for prompt in POCKET_PROMPTS[family]:pocket_log_entry(j,n,family,prompt,False);n+=1
    while j.count<120:j.ruled_notes('Open reflection','Choose a card, a memory, a feeling, or nothing at all.',section='Notes')
    if j.count%2:j.ruled_notes('Open reflection','This page is yours.',section='Notes')
    j.c.save();return j.count

def build_pocket_deluxe_log(path):
    size=(5*inch,7*inch)
    j=JournalPDF(path,'Pocket of Calm','Companion logbook',size=size)
    # custom title works because JournalPDF uses own size
    j.title_page('pocket')
    j.copyright_page(DISCLAIMERS['pocket'],'Pair a card with an entry—or use the book on its own. The box set must be fully useful without the optional audio link.')
    j.section_page('How to begin','Choose. Pause. Respond. Continue.','Pick a card at random or choose a family. Read the invitation once. Write one line, fill the page, speak it aloud, or let the question stay with you.')
    j.check_in('A personal index',[('CARDS I WANT TO KEEP NEARBY',3),('PROMPTS I WANT TO SKIP OR ADAPT',2),('A NOTE TO MY FUTURE SELF',2)],'Your relationship with a prompt may change. That is allowed.','Beginning')
    j.section_page('The six families','Arrive, soften, nourish, reach, continue, reset.','The color and icon system on the cards helps you find a kind of question. The practice is always optional and belongs to you.')
    n=1
    for family,_ in POCKET_FAMILIES:
        for prompt in POCKET_PROMPTS[family]:pocket_log_entry(j,n,family,prompt,True);n+=1
    while j.count<144:j.ruled_notes('Open reflection','Choose a card or begin wherever you are.',section='Notes')
    if j.count%2:j.ruled_notes('Open reflection','This page is yours.',section='Notes')
    j.c.save();return j.count

# Covers
BOOKS = {
    'dose-and-breathe': {'title':'Dose & Breathe','subtitle':'A mindful weekly companion for your GLP-1 journey','tag':'dose','back':'A private place to meet a weekly routine with a little more ease. Notice what is here, choose one small calming ritual, and carry forward only what helps. This journal is for personal reflection alongside—not instead of—guidance from your care team.'},
    'softer-words': {'title':'Softer Words','subtitle':'A gratitude and self-talk diary for ordinary hard days','tag':'softer','back':'A warm, undated place for the whole truth of a day: what felt hard, what you did with care, and one sentence you can believe. No streaks. No perfection. Just a small, beautiful practice of returning to your own side.'},
    'back-to-enough': {'title':'Back to Enough','subtitle':'A compassionate productivity rescue workbook','tag':'back','back':'For days when the list is louder than your capacity. This undated workbook helps you make the next step smaller, protect your energy, and count the work that already matters. A practical, kind companion for returning to enough.'},
    'rest-and-regulate': {'title':'Rest & Regulate','subtitle':'A 90-day breath-paced planner for small returns','tag':'rest','back':'A low-pressure place to pause, notice, and choose one gentle practice. This undated planner pairs simple grounding invitations with room to observe what supports you. No performance metrics—just small returns to the present.'},
    'night-harbor': {'title':'Night Harbor','subtitle':'An evening wind-down and sleep reflection companion','tag':'night','back':'A bedside landing place for setting down the day. With brief evening prompts and quiet morning reflections, Night Harbor makes room for comfort, pattern noticing, and a gentler transition—one page at a time.'},
    'enough-money-enough-calm': {'title':'Enough Money, Enough Calm','subtitle':'A financial-anxiety mindset workbook','tag':'money','back':'A calm place to separate facts, feelings, and one next step. This workbook offers emotion-forward prompts for money moments without pretending there is a perfect answer. Pause before panic. Start with what is true.'},
    'pocket-of-calm-companion': {'title':'Pocket of Calm','subtitle':'A guided journaling companion for small returns','tag':'pocket','back':'When a blank journal is too much, begin with one small question. This companion includes 54 grounding prompts organized into six gentle families, with plenty of room to write—or simply pause.'},
}

def make_cover(path, title, subtitle, back, tag, pages, trim=(6,8), author=AUTHOR):
    trimw,trimh=trim
    bleed=.125
    spine=pages*.002252 # KDP white-paper B&W paperback formula; verify with the current KDP calculator before upload.
    width=(bleed+trimw+spine+trimw+bleed)*inch
    height=(bleed+trimh+bleed)*inch
    c=canvas.Canvas(str(path),pagesize=(width,height),pageCompression=1)
    pal=PALETTE[tag];bg=HexColor('#'+pal['bg']);acc=HexColor('#'+pal['accent']);sub=HexColor('#'+pal['sub'])
    c.setFillColor(bg);c.rect(0,0,width,height,fill=1,stroke=0)
    # subtle line art pattern on back/front
    c.setStrokeColor(acc);c.setLineWidth(.8)
    for rr in [1.0,1.35,1.7,2.05]:
        c.circle(width*.82,height*.80,rr*inch,stroke=1,fill=0)
    # spine boundaries for proofing only; very faint
    spine_x=(bleed+trimw)*inch
    c.setStrokeColor(colors.Color(1,1,1,alpha=.22));c.setLineWidth(.35)
    c.line(spine_x,0,spine_x,height);c.line(spine_x+spine*inch,0,spine_x+spine*inch,height)
    front_left=(bleed+trimw+spine)*inch
    fw=trimw*inch
    draw_centered(c,title,front_left+fw/2,height*.59,25,colors.white,'Helvetica-Bold',max_width=fw-.9*inch,leading=29)
    draw_centered(c,subtitle,front_left+fw/2,height*.47,10.5,sub,'Helvetica',max_width=fw-.95*inch,leading=13)
    if author:
        c.setFont('Helvetica',8);c.setFillColor(colors.white);c.drawCentredString(front_left+fw/2,height*.17,author)
    c.setFont('Helvetica',6.8);c.setFillColor(sub);c.drawCentredString(front_left+fw/2,.38*inch,'THE RITUAL LIBRARY')
    # back copy
    bx=bleed*inch+.42*inch;by=height*.66
    c.setFont('Helvetica-Bold',8);c.setFillColor(sub);c.drawString(bx,by,'THE RITUAL LIBRARY')
    draw_paragraph(c,back,bx,by-.26*inch,trimw*inch-.85*inch,9.2,12,colors.white)
    # Barcode keep-clear box; KDP will place its barcode here if no ISBN barcode is supplied.
    c.setFillColor(colors.white);c.rect(.35*inch,.36*inch,2.0*inch,1.20*inch,fill=1,stroke=0)
    c.setFillColor(bg);c.setFont('Helvetica',5.5);c.drawCentredString(1.35*inch,.29*inch,'BARCODE KEEP-CLEAR AREA')
    # spine text if legible
    if spine>=.18:
        c.saveState();c.translate(spine_x+spine*inch/2,.35*inch);c.rotate(90);c.setFillColor(colors.white);c.setFont('Helvetica-Bold',max(4,min(7,spine*30)));c.drawCentredString((trimh*inch)/2,0,title.upper());c.restoreState()
    c.save()
    return {'pages':pages,'spine_in':spine,'cover_width_in':bleed+trimw+spine+trimw+bleed,'cover_height_in':bleed+trimh+bleed}

# Deck components
def build_card_fronts(path):
    # 3.25x4.75 trim + .125 bleed each side = 3.5 x 5.0 inch art pages. Vendor imposes final sheets.
    W,H=3.5*inch,5*inch;bleed=.125*inch;c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
    family_cols=['416A67','815C65','A27C51','B86B5A','6B7F48','46556D']
    n=1
    for fi,(family,desc) in enumerate(POCKET_FAMILIES):
        bg=HexColor('#'+family_cols[fi]);accent=colors.white
        for prompt in POCKET_PROMPTS[family]:
            c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0)
            c.setStrokeColor(colors.Color(1,1,1,.45));c.setLineWidth(.5);c.roundRect(bleed,bleed,W-2*bleed,H-2*bleed,10,stroke=1,fill=0)
            c.setFillColor(accent);c.setFont('Helvetica-Bold',7.5);c.drawCentredString(W/2,H-.42*inch,f'{family}  ·  {n:02d}')
            c.setStrokeColor(colors.Color(1,1,1,.75));c.setLineWidth(.7);c.line(.48*inch,H-.61*inch,W-.48*inch,H-.61*inch)
            draw_centered(c,prompt,W/2,H*.55,14,accent,'Helvetica-Bold',max_width=W-.75*inch,leading=17)
            c.setFont('Helvetica-Oblique',7.5);c.setFillColor(colors.Color(1,1,1,.85));c.drawCentredString(W/2,.48*inch,desc)
            c.showPage();n+=1
    c.save();return n-1

def build_card_backs(path):
    W,H=3.5*inch,5*inch;c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
    for n in range(54):
        c.setFillColor(HexColor('#314944'));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setStrokeColor(HexColor('#D7AE86'));c.setLineWidth(.8)
        for r in [.45,.75,1.05]:c.circle(W/2,H/2,r*inch,stroke=1,fill=0)
        c.setFillColor(colors.white);c.setFont('Helvetica-Bold',15);c.drawCentredString(W/2,H/2+.08*inch,'POCKET')
        c.setFont('Helvetica',9);c.drawCentredString(W/2,H/2-.12*inch,'OF CALM')
        c.setFont('Helvetica',6.5);c.setFillColor(HexColor('#F3E7D9'));c.drawCentredString(W/2,.4*inch,'THE RITUAL LIBRARY')
        c.showPage()
    c.save();return 54

def build_quickstart(path):
    W,H=5*inch,7*inch;j=JournalPDF(path,'Pocket of Calm','Quick-start card',size=(W,H))
    j.title_page('pocket',author='A small ritual for hard days')
    j.page_frame('How to use',number=False);c=j.c;c.setFillColor(INK);c.setFont('Helvetica-Bold',17);c.drawString(.45*inch,H-.62*inch,'Choose. Pause. Respond.')
    y=H-1.05*inch
    for n,(head,body) in enumerate([('1 · Choose','Pick a card at random or find the family that fits.'),('2 · Pause','Read the prompt once. Skip it if it is not for you.'),('3 · Respond','Write one word, fill a page, say it aloud, or keep it private.'),('4 · Continue','Place the card where you will see it—or return it and move on.')]):
        c.setFont('Helvetica-Bold',10);c.setFillColor(INK);c.drawString(.45*inch,y,head);y-=.18*inch;y=draw_paragraph(c,body,.45*inch,y,W-.9*inch,8.8,11,MID);y-=.17*inch
    c.setFillColor(MID);c.setFont('Helvetica-Oblique',8);draw_paragraph(c,'Pocket of Calm is a personal reflection tool, not therapy, medical care, or crisis support. Seek appropriate professional or urgent support when needed.',.45*inch,.8*inch,W-.9*inch,8,10,MID)
    j.end();j.c.save();return j.count

# Run builds
manifest=[]
def save_book(slug, build_fn, metadata):
    folder=KDP/slug;folder.mkdir(exist_ok=True)
    interior=folder/(slug+'-interior.pdf')
    pages=build_fn(interior)
    cover=folder/(slug+'-cover-wrap.pdf')
    coverinfo=make_cover(cover,BOOKS[slug]['title'],BOOKS[slug]['subtitle'],BOOKS[slug]['back'],BOOKS[slug]['tag'],pages)
    m={'slug':slug,'format':'KDP black-and-white paperback scout','trim':'6 x 8 in','interior':interior.name,'cover':cover.name,'pages':pages,**coverinfo,**metadata}
    (folder/'metadata-and-preflight.md').write_text(make_metadata(m),encoding='utf-8')
    manifest.append(m)
    return m

def make_metadata(m):
    return f"""# {m['title']} — KDP scout release package

## Package contents
- `{m['interior']}` — {m['pages']}-page, 6 × 8 in. black-and-white interior PDF.
- `{m['cover']}` — full paperback cover wrap calculated for white paper at {m['cover_width_in']:.4f} × {m['cover_height_in']:.4f} in.; estimated spine {m['spine_in']:.4f} in.

## Listing draft
**Title:** {m['title']}
**Subtitle:** {m['subtitle']}
**Author:** {AUTHOR} *(owner-directed provisional local attribution; name/rights clearance remains required before public use)*  \
**Description:** {m['description']}

**Suggested keywords:** {m['keywords']}

## KDP upload preflight — do this after final edits
1. Choose 6 × 8 in., paperback, black-and-white interior, white paper, no-bleed interior, and confirm final page count is exactly **{m['pages']}**.
2. Download the current official KDP Cover Calculator template after selecting those exact settings. The wrap is sized from the current white-paper equation (page count × 0.002252 in.) but must be checked against the template before upload.
3. Before any release, a named human must approve author/imprint, any retained audio text, and a buyer-controlled URL/QR destination; verify each retained URL from a printed proof.
4. Obtain legal/claims review before publishing health-, sleep-, anxiety-, breathwork-, or finance-adjacent copy. This content is a design draft, not legal or clinical clearance.
5. Preview in KDP’s Print Previewer; order and inspect a physical proof before enabling ads.

## Claims boundary
{m['boundary']}
"""

save_book('dose-and-breathe',lambda p:build_dose(p,False),{
    'title':BOOKS['dose-and-breathe']['title'],'subtitle':BOOKS['dose-and-breathe']['subtitle'],
    'description':'A discreet, guided weekly reflection book for adults using prescribed GLP-1 medication. Each spread pairs optional routine notes with a simple breath visual and space to notice comfort, rest, support, and one kind next step. This is a journal for personal reflection alongside guidance from a care team—not a dosing guide or a diet plan.',
    'keywords':'GLP-1 journal, mindful wellness journal, weekly reflection, self compassion journal, medication routine companion, calming journal',
    'boundary':'Do not promise weight loss, symptom relief, safer medication use, or anxiety treatment. Keep GLP-1 copy generic and obtain trademark/healthcare-marketing review before public release.'})
save_book('softer-words',build_softer,{
    'title':BOOKS['softer-words']['title'],'subtitle':BOOKS['softer-words']['subtitle'],
    'description':'An undated gratitude and self-talk diary for the ordinary hard days. Brief prompts make room for what felt difficult, what you did with care, and one kind sentence you can believe. Designed as a low-pressure, giftable daily reflection practice.',
    'keywords':'self compassion journal, gratitude diary, positive self talk journal, gentle daily journal, mindful reflection, gift journal',
    'boundary':'Market as a personal reflection diary, not therapy, a treatment for anxiety or depression, or a substitute for professional care.'})
save_book('back-to-enough',build_back,{
    'title':BOOKS['back-to-enough']['title'],'subtitle':BOOKS['back-to-enough']['subtitle'],
    'description':'A compassionate productivity rescue workbook for low-capacity days. Use gentle task triage, capacity checks, mini-break planning, and weekly resets to make the next step smaller and more doable.',
    'keywords':'burnout workbook, compassionate productivity planner, task triage planner, overwhelm journal, recovery planning, self care workbook',
    'boundary':'Avoid claims to diagnose, treat, or cure burnout, anxiety, depression, or workplace harm. This is planning/reflection support.'})
save_book('rest-and-regulate',build_rest,{
    'title':BOOKS['rest-and-regulate']['title'],'subtitle':BOOKS['rest-and-regulate']['subtitle'],
    'description':'A 90-day undated reflection planner built around simple, optional grounding and paced-breathing practices. Notice how you arrive, choose a small return to the present, and record what supports you—without performance metrics.',
    'keywords':'breathwork journal, grounding practice planner, 90 day mindfulness journal, stress relief journal, nervous system journal, daily reflection',
    'boundary':'Do not claim to stimulate the vagus nerve, treat anxiety, improve HRV, regulate a medical condition, or create physiological outcomes.'})
save_book('night-harbor',build_night,{
    'title':BOOKS['night-harbor']['title'],'subtitle':BOOKS['night-harbor']['subtitle'],
    'description':'A bedside wind-down and morning reflection companion. Brief prompts help set down the day, choose a comfort, notice patterns, and approach tomorrow with one gentle intention.',
    'keywords':'sleep journal, bedtime journal, evening reflection, wind down routine, night journal, gentle self care gift',
    'boundary':'Do not claim to treat insomnia, solve sleep problems, or deliver medical sleep improvement.'})
save_book('enough-money-enough-calm',build_money,{
    'title':BOOKS['enough-money-enough-calm']['title'],'subtitle':BOOKS['enough-money-enough-calm']['subtitle'],
    'description':'An emotion-forward reflection workbook for money moments. Separate facts from the stories and feelings around them, identify one manageable next step, and make room for a calmer approach to financial decisions.',
    'keywords':'money anxiety journal, financial mindset workbook, money reflection journal, financial wellness journal, calm money planner, self reflection',
    'boundary':'Do not provide or imply financial, investment, legal, tax, or mental-health advice. Avoid promises of financial outcomes.'})
save_book('pocket-of-calm-companion',build_pocket_kdp,{
    'title':BOOKS['pocket-of-calm-companion']['title'],'subtitle':BOOKS['pocket-of-calm-companion']['subtitle'],
    'description':'A stand-alone guided journaling companion with 54 small prompts organized into six families: arrive, soften, nourish, reach, continue, and reset. Made for the moments when a blank page asks too much.',
    'keywords':'journaling prompts, mindfulness journal, self reflection book, calming gift, stress relief journal, prompt journal',
    'boundary':'Position as a general self-reflection product unless and until a separate GLP-1-specific edition has completed legal review and validation.'})

# Deluxe hero: Dose & Breathe
DB=DELUXE/'dose-and-breathe';DB.mkdir(exist_ok=True)
deluxe_dose_pages=build_dose(DB/'dose-and-breathe-deluxe-interior-160pp.pdf',True)
# Front-cover artwork only: vendor dieline required for final case wrap
c=canvas.Canvas(str(DB/'dose-and-breathe-deluxe-front-cover-art.pdf'),pagesize=(6*inch,8*inch),pageCompression=1)
pal=PALETTE['dose'];c.setFillColor(HexColor('#'+pal['bg']));c.rect(0,0,6*inch,8*inch,fill=1,stroke=0);c.setStrokeColor(HexColor('#'+pal['accent']));c.setLineWidth(1.2)
for rr in [1.25,1.62,1.99]:c.circle(4.7*inch,6.15*inch,rr*inch,stroke=1,fill=0)
draw_centered(c,'Dose & Breathe',3*inch,4.62*inch,24,colors.white,'Helvetica-Bold',max_width=4.9*inch,leading=29)
draw_centered(c,'A mindful weekly companion for your GLP-1 journey',3*inch,3.68*inch,11,HexColor('#'+pal['sub']),'Helvetica',max_width=4.8*inch,leading=14)
c.setFillColor(colors.white);c.setFont('Helvetica',9);c.drawCentredString(3*inch,1.78*inch,AUTHOR);c.setFillColor(HexColor('#'+pal['sub']));c.setFont('Helvetica',7);c.drawCentredString(3*inch,.5*inch,'THE RITUAL LIBRARY');c.save()
(DB/'dose-and-breathe-deluxe-production-notes.md').write_text(f'''# Dose & Breathe — deluxe production package

## Included artwork
- `dose-and-breathe-deluxe-interior-160pp.pdf` — **{deluxe_dose_pages} pages**, finished 6 × 8 in. interior; two-color intent, supplied in grayscale layout draft.
- `dose-and-breathe-deluxe-front-cover-art.pdf` — finished-size front-cover art (6 × 8 in.).

## Final-vendor inputs still required
A casebound full-wrap cover, spine/back layout, endpaper file, pocket dieline, ribbon location, and elastic placement **must be built on the selected vendor’s dielines and board/cloth specifications**. Do not send front-cover art as a finished case-wrap file.

## Baseline construction
- 6 × 8 in. casebound book; 160 pages / 80 leaves; sewn signatures preferred.
- 100 gsm warm-white uncoated writing stock; 140–160 gsm endpapers.
- Cloth or cloth-textured wrap; blind deboss title + one-color foil line element.
- Two 6 mm ribbons, tonal elastic closure, expandable rear pocket, die-cut 350 gsm breath bookmark.
- Recyclable belly band; no fragrance/scent treatment in first run.

## Release blockers
Obtain a named-human author/imprint decision; approve any audio/domain route, claims/naming review, physical paper/pen test, binding dummy, foil/deboss proof, and final vendor dielines before production.
''',encoding='utf-8')

# Deluxe hero: Pocket of Calm
PC=DELUXE/'pocket-of-calm';PC.mkdir(exist_ok=True)
fronts=build_card_fronts(PC/'pocket-of-calm-card-fronts-54up-individual-bleed.pdf')
backs=build_card_backs(PC/'pocket-of-calm-card-backs-54up-individual-bleed.pdf')
logpages=build_pocket_deluxe_log(PC/'pocket-of-calm-companion-logbook-144pp.pdf')
quick=build_quickstart(PC/'pocket-of-calm-quick-start-card.pdf')
(PC/'pocket-of-calm-production-notes.md').write_text(f'''# Pocket of Calm — deluxe production package

## Included artwork
- `pocket-of-calm-card-fronts-54up-individual-bleed.pdf` — {fronts} individual card-front art pages, **3.5 × 5 in. including 0.125 in. bleed** for 3.25 × 4.75 in. finished cards.
- `pocket-of-calm-card-backs-54up-individual-bleed.pdf` — {backs} common card-back pages, same art size.
- `pocket-of-calm-companion-logbook-144pp.pdf` — {logpages}-page finished 5 × 7 in. logbook interior.
- `pocket-of-calm-quick-start-card.pdf` — 5 × 7 in. folded-card layout proof; vendor should impose to final fold/bleed template.

## Vendor-imposition requirement
Card sheets, box wrap, box insert, and logbook cover are intentionally **not imposed**. The chosen printer must provide exact dielines, safe zones, stock/bleed requirements, and duplex alignment rules. Supply the included individual art only after proofing against that template.

## Baseline construction
- 54 3.25 × 4.75 in. rounded-corner cards on 330–350 gsm durable matte/linen-feel stock.
- Six prompt families of nine cards; color plus text family name used as redundant navigation.
- 5 × 7 in. 144-page companion logbook, 100 gsm natural writing paper, lay-flat-friendly PUR or sewn softcover.
- Paper-wrapped rigid magnetic box with paperboard insert. Box dimensions determined only after physical card and book sample.
- Baseline packaging is paper belly band/tissue; price magnetic box alternatives separately.

## Release blockers
Choose one positioning: collection-neutral or GLP-1-specific. The current content and companion/KDP copy are collection-neutral. Do not add GLP-1 health claims without a separate cleared copy pass. Obtain final brand domain before adding QR/audio destination; verify every printed code from a physical proof.
''',encoding='utf-8')

# Source content / manifest
(SOURCE/'pocket-of-calm-prompts.md').write_text('# Pocket of Calm — 54 final deck prompts\n\n'+ '\n\n'.join(f'## {f}\n{d}\n\n'+'\n'.join(f'{i+1}. {x}' for i,x in enumerate(POCKET_PROMPTS[f])) for f,d in POCKET_FAMILIES),encoding='utf-8')
(SOURCE/'production-status.md').write_text('''# Production status — current batch

## Files generated now
All KDP scout interiors, KDP paperback cover-wrap drafts, the deluxe Dose & Breathe interior/front art, and Pocket of Calm card/logbook/quick-start content are included in this folder.

## Not yet final-for-release by design
- Author/imprint name, ISBN/barcode decisions, imprint/contact pages, and brand-owned audio URL are placeholders.
- Every health-, sleep-, anxiety-, breathwork-, and finance-adjacent line requires the planned legal/claims review.
- KDP cover wraps must be checked against the current official template after final page count/paper/trim selection.
- Deluxe case wraps, card imposition, logbook covers, magnetic-box/insert art, and shipping cartons require selected-vendor dielines and physical proof approval.
- Pocket of Calm needs a deliberate positioning choice: general Ritual Library core object (current copy) or GLP-1-specific version (requires revised copy/review).

This is the fastest honest form of “publish-ready”: final authored content and formatted artwork, with release blockers visible rather than hidden.
''',encoding='utf-8')

# Main package readme
summary=[]
for m in manifest:
    summary.append(f"| {m['title']} | KDP paperback scout | {m['pages']} | 6 × 8 in. | {m['cover_width_in']:.4f} × {m['cover_height_in']:.4f} in. cover wrap |")
(ROOT/'README.md').write_text(f'''# The Ritual Library — production batch 01

**Scope delivered:** six KDP scout books, a KDP *Pocket of Calm* companion, and two deluxe-hero production packages for *Dose & Breathe* and *Pocket of Calm*.

## Read this first
The PDFs are complete, formatted content/layout drafts suitable for proofing. They are **not blindly safe to publish or manufacture** until the visible release blockers are completed: author/imprint replacement, legal/claims review, final brand domain/QR destination, KDP Cover Calculator validation, vendor dielines, and physical proofs.

## KDP scout packages
| Title | Format | Pages | Trim | Full-cover wrap |
|---|---|---:|---|---|
{chr(10).join(summary)}

Each `kdp-scouts/[title]` folder includes an interior PDF, full-wrap paperback cover draft, and `metadata-and-preflight.md` with listing text and upload QA.

## Deluxe hero packages
- `deluxe-heroes/dose-and-breathe/` — 160-page 6 × 8 in. interior, front-cover art, and casebound construction/production notes.
- `deluxe-heroes/pocket-of-calm/` — 54 front cards, 54 backs, 144-page logbook interior, quick-start card, and card/box production notes.

## File truthfulness
- **KDP interior PDFs:** ready to upload after replacing placeholders and checking in Print Previewer.
- **KDP cover-wrap PDFs:** calculated to current KDP white-paper formula ({'{'}page count × 0.002252 in. spine{'}'}); validate on KDP’s generated template for exact final settings before upload.
- **Deluxe interiors/cards:** authored and sized artwork; final press-ready files need the chosen vendor’s specific dielines/imposition and signed physical proof.

## Immediate next steps
1. Complete Week 1 legal/trademark/domain tasks in the launch kit.
2. Obtain a named-human author/imprint decision and choose an approved rights-page convention before release.
3. Decide whether *Pocket of Calm* is a collection-neutral core object (current content) or a GLP-1-specific edition.
4. Run the KDP PDFs through Print Previewer and order one proof of each approved scout.
5. Send vendor RFQs; use their templates to finish deluxe cover, box, and card-imposition files.

Generated: {date.today().isoformat()}.
''',encoding='utf-8')

print('Generated',ROOT)
print(json.dumps([{'slug':m['slug'],'pages':m['pages'],'cover':m['cover_width_in']} for m in manifest],indent=2))
