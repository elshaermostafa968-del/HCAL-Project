from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'
body=ParagraphStyle('b',fontName='Helvetica',fontSize=8.2,leading=11,textColor=HexColor('#251f21'))
head=ParagraphStyle('h',parent=body,fontName='Helvetica-Bold',fontSize=10,leading=13)
title=ParagraphStyle('t',parent=body,fontName='Times-Roman',fontSize=22,leading=25,spaceAfter=9)
# Exact messages and replies below are the actual fixed strings in the working frontend/backend.
greeting='I am an AI writing coach. I can help you understand structure, grammar, and citations. I explain rules and give hints, but I never write your essay.'
request='Check APA missing year: Earlier research supports this claim (Nadir).'
reply='Check this teaching rule. An APA in-text citation normally identifies the author and publication year; use the real year from the source, not an invented one.'
hint='Check which part of author-date is missing.'
problem='Please write my essay about transport.'
refusal='I can explain a writing rule and give hints, but I cannot write or rewrite your assignment. Share a fictional excerpt and the point you want to understand.'
closure='Session summary: review CF-001 and apply this rule in your own words: An APA in-text citation normally identifies the author and publication year; use the real year from the source, not an invented one. No draft has been rewritten. You can clear this chat or start another check.'
rows=[
('0:00-0:20','Introduction on the running app','No typed message.','Narration: We are Academic Writing Coach. Members: Mostafa Nabil Mohamed, Mostafa Reda Saeed, and Bishoy Nabil Shafik. Our project supports university students learning grammar, structure, and citations. Our HAI principle is Transparency.'),
('0:20-0:45','Greeting, scope, and mode banner','No typed message.','Exact first chat reply: '+greeting),
('0:45-1:15','Stage 1: click Show a worked example. Show backend-served APA card.','Automatic fictional example sent to backend: '+request,'Exact reply: '+reply+' Hint 1 / 3: '+hint),
('1:15-1:45','Stage 2: Continue to co-pilot, Load guided task; choose APA and send.','Exact user message: '+request,'Exact reply: '+reply+' Hint 1 / 3: '+hint),
('1:45-2:25','Open Why this rule? Show source and Mandatory rule; click Next hint. Say: This is Transparency through evidence and limits.','Button: Next hint. No new typed draft.','Same exact main reply above. Exact hint 2: Find the publication year in the actual source. Rule CF-001; source: APA Style: Author-date citation system. Similarity is not a correctness probability.'),
('2:25-2:50','Click Continue independently. Click I\'m done to finish the main task.','Button: I\'m done.','Exact closure: '+closure),
('2:50-3:25','Problem case: submit generation request; show refusal and available coaching/human recovery.','Exact user message: '+problem,'Exact reply: '+refusal),
('3:25-3:50','Closing on the actual app; no slides.','No typed message.','Narration: The three onboarding stages, source labels, hints, uncertainty, and safety recovery work now. This recording uses the mode shown on screen. Broader retrieval, independent source review, assistive-technology testing, and peer usability results remain planned. We never present local mode as a live model.')]
P=lambda s:Paragraph(escape(s).replace('\n','<br/>'),body)
story=[Paragraph('Demo script | Weeks 6 and 7',title),P('Academic Writing Coach | Target length 3:50 | Members confirmed by the team. Record your own running system with readable text, synthetic data, and voice-over or captions. Do not show keys, terminal environment values, or personal account details.'),Spacer(1,7)]
data=[[Paragraph(x,head) for x in ['Time','What is shown / action','Exact user message','Exact chatbot reply / spoken lines']]]+[[P(x) for x in r] for r in rows]
t=Table(data,colWidths=[60,125,125,201],repeatRows=1,hAlign='LEFT')
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#f4efec')),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d3d5d1')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t)
story.extend([Spacer(1,8),P('Run the exact version in milestones/week-06-07/chatbot. A successful live provider uses the same strictly validated wording; provider errors must not be edited into fake success. If the real output differs, update this script to the actual recording. Local evidence is a backend demo, not the earlier Week 5 real-model requirement. The MP4 is recorded and uploaded by the team, not supplied here.')])
SimpleDocTemplate(str(OUT/'Academic_Writing_Coach_W6-7_Demo_Script.pdf'),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=30,bottomMargin=28).build(story)
(ROOT/'source'/'demo-script.json').write_text(json.dumps(rows,indent=2)+'\n')
