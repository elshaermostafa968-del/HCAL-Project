"""Generate print reports and diagram previews from the editable course materials."""
from pathlib import Path
import html
import re
import subprocess
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
ROOT=Path(__file__).resolve().parents[1]
INK=HexColor('#251f21'); GREEN=HexColor('#315d50'); SAND=HexColor('#f4efec')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX',fontName='Helvetica',fontSize=9.5,leading=14,spaceAfter=6,textColor=INK))
styles.add(ParagraphStyle(name='H1X',fontName='Times-Roman',fontSize=27,leading=31,spaceBefore=12,spaceAfter=18,textColor=INK))
styles.add(ParagraphStyle(name='H2X',fontName='Helvetica-Bold',fontSize=14,leading=19,spaceBefore=16,spaceAfter=8,textColor=GREEN,keepWithNext=True))
styles.add(ParagraphStyle(name='H3X',fontName='Helvetica-Bold',fontSize=11,leading=15,spaceBefore=10,spaceAfter=7,textColor=INK,keepWithNext=True))
styles.add(ParagraphStyle(name='CellX',fontName='Helvetica',fontSize=8,leading=12,textColor=INK))
def safe(s):
 s=html.escape(s).replace('≥','&gt;=').replace('≤','&lt;=').replace('·',' | ').replace('–','-')
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'<font face="Courier">\1</font>',s)
 # Long URLs wrap in reportlab when splitLongWords is enabled.
 return s

def footer(canvas,doc):
 canvas.setStrokeColor(HexColor('#d3d5d1'));canvas.line(42,39,553,39)
 canvas.setFont('Helvetica',7);canvas.setFillColor(HexColor('#585254'))
 canvas.drawString(42,27,'Academic Writing Coach | Transparency | Teaching prototype')
 canvas.drawRightString(553,27,str(doc.page))

def report(md,dest,extras=None):
 lines=Path(md).read_text().splitlines();story=[];i=0
 while i<len(lines):
  line=lines[i].strip();i+=1
  if not line:continue
  if line.startswith('|'):
   rows=[line]
   while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
   parsed=[[c.strip() for c in r.strip('|').split('|')] for r in rows]
   parsed=[r for r in parsed if not all(re.fullmatch(r'[-: ]+',c) for c in r)]
   n=len(parsed[0]);widths=[511/n]*n
   table=Table([[Paragraph(safe(c),styles['CellX']) for c in r] for r in parsed],colWidths=widths,repeatRows=1,hAlign='LEFT')
   table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),SAND),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d3d5d1'))]))
   story.extend([table,Spacer(1,10)]);continue
  if line.startswith('### '):style='H3X';line=line[4:]
  elif line.startswith('## '):style='H2X';line=line[3:]
  elif line.startswith('# '):style='H1X';line=line[2:]
  else:style='BodyX'
  if line.startswith('- '):line='• '+line[2:]
  story.append(Paragraph(safe(line),styles[style]))
 if extras:
  from PIL import Image as PILImage
  for title,path in extras:
   story.extend([PageBreak(),Paragraph(title,styles['H2X'])]);w,h=PILImage.open(path).size
   factor=min(511/w,650/h);story.append(Image(str(path),width=w*factor,height=h*factor))
 SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=55,title=Path(md).stem.replace('-',' ').title(),author='Academic Writing Coach project').build(story,onFirstPage=footer,onLaterPages=footer)

FLOW='''digraph G {
 graph [rankdir=TB,bgcolor="white",pad=".3",nodesep=".25",ranksep=".3"];
 node [shape=box,style="rounded,filled",fillcolor="#f4efec",color="#315d50",fontname="Helvetica",fontsize=12,margin=".18,.12"];
 edge [fontname="Helvetica",fontsize=10,color="#6c7e73"];
 start [shape=oval,label="START: AI greeting, scope, worked example"];
 quick [label="Quick replies + style / focus selection"];
 input [label="Student fictional excerpt + question"];
 check [shape=diamond,label="S1: scope + context?"];
 scope [label="Refuse assignment generation\nRe-offer coaching"];
 context [label="Ask one clarifying question"];
 retrieve [shape=diamond,label="S2: strong rule match?"];
 unsure [label="UNCERTAINTY\nMore context or official source",style="rounded,dashed"];
 call [label="S3 prompt + S4 call\nExplicit local OR configured live provider"];
 retry [label="Error: 10-second timeout\nRetry once, then calm fallback",style="rounded,dashed"];
 validate [shape=diamond,label="S5: grounded JSON?"];
 card [label="S6: feedback card\nRule + source + text label + hint + evidence"];
 follow [label="Previous / next hint | Why? | Source only\nEdit last | Check another | Done"];
 human [label="HUMAN OPTIONS (always reachable)\nInstructor / writing center / librarian\nAfter two unhelpful ratings or failed retry",peripheries=2];
 end [shape=oval,label="CLOSURE: summary + rating + Clear chat"];
 start -> quick -> input -> check;
 check -> scope [label="Out of scope"]; scope -> quick;
 check -> context [label="Too little"]; context -> input;
 check -> retrieve [label="Enough context"];
 retrieve -> unsure [label="Weak / conflict"]; retrieve -> call [label="Strong"];
 call -> retry [label="API failure"]; call -> validate [label="Response"];
 retry -> validate [label="Retry works"];retry -> human [label="Fails"];
 validate -> unsure [label="Reject"];validate -> card [label="Accept"];
 card -> follow; follow -> call [label="Hint"];follow -> quick [label="Another"];
 follow -> end [label="Done"];unsure -> human; quick -> human [style=dashed];card -> human [style=dashed,label="2 unhelpful"];
 human -> end;
}'''
ARCH='''digraph G {
 graph [rankdir=TB,bgcolor="white",pad=".3",nodesep=".35",ranksep=".35"];
 node [shape=box,style="rounded,filled",fillcolor="#f4efec",color="#315d50",fontname="Helvetica",fontsize=13,margin=".2,.15"];
 edge [fontname="Helvetica",fontsize=10,color="#6c7e73"];
 browser [label="STUDENT INTERFACE\nHTML5 / CSS3 / JS\nChat log, quick replies, labels, source panel, human route"];
 s1 [label="S1 SAFEGUARD\nLength, scope, context checks"];
 s2 [label="S2 TRANSPARENCY\nLexical retriever: rule + source + similarity score",penwidth=2];
 s3 [label="S3 PROMPT BUILDER\nOne retrieved rule, no rewrite, JSON, text label"];
 s4 [label="S4 SAFEGUARD\nBackend LLM client: 10 seconds + one retry\nOR explicitly labelled deterministic local mode"];
 s5 [label="S5 TRANSPARENCY\nExact extractive JSON validator\nReject unsupported rule ID or content",penwidth=2];
 s6 [label="S6 TRANSPARENCY\nCompose evidence + label + hint + uncertainty",penwidth=2];
 data [shape=cylinder,label="DATASET\n40 fictional cases\nAPA / MLA / IEEE / university guidance"];
 api [label="HOSTED API\nGemini or OpenAI\nServer-side .env key only"];
 log [shape=cylinder,label="POST /feedback\nCategory-only local ratings\nNo drafts or session IDs persisted"];
 eval [label="EVALUATION\n40 labelled fixture prompts\nSaved outputs + honest test limits"];
 health [label="GET /health\nMode + configuration + counts\nNever exposes secrets"];
 browser -> s1 [label="POST /chat"];s1 -> s2 -> s3 -> s4 -> s5 -> s6;
 data -> s2 [label="lookup"];s4 -> api [label="Configured live mode"];api -> s4 [label="JSON response"];
 s6 -> browser [label="JSON + evidence",constraint=false]; browser -> log [style=dashed];browser -> health [style=dashed]; eval -> s1 [style=dashed,label="TestClient"];
}'''
if __name__=='__main__':
 for name,source in [('flow',FLOW),('architecture',ARCH)]:
  path=ROOT/'docs'/f'{name}.dot';path.write_text(source)
  subprocess.run(['dot','-Tpng','-Gdpi=140',str(path),'-o',str(ROOT/'docs'/f'{name}.png')],check=True)
  subprocess.run(['dot','-Tpdf',str(path),'-o',str(ROOT/'docs'/f'{name}.pdf')],check=True)
 for name in ['week3-users-and-data','week4-plan-and-metrics','week5-implementation']:
  if not (ROOT/'docs'/f'{name}.md').exists(): continue
  extras=[('Implemented system architecture',ROOT/'docs'/'architecture.png'),('Conversation flow and recovery',ROOT/'docs'/'flow.png')] if name.startswith('week5') else None
  report(ROOT/'docs'/f'{name}.md',ROOT/'docs'/f'{name}.pdf',extras)
