from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table,TableStyleInfo
import re,subprocess
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source' if (ROOT/'source').exists() else ROOT/'editable-source';OUT=ROOT/'deliverables'
META=json.loads((SOURCE/'team.json').read_text()) if (SOURCE/'team.json').exists() else {'team':'TEAM_NAME_PENDING','members':'MEMBERS_PENDING'}
TEAM=META['team'];PREFIX=TEAM+'_W6-7_'

def inline(p,s):
 for i,part in enumerate(re.split(r'(\*\*.*?\*\*)',s)):
  r=p.add_run(part[2:-2] if part.startswith('**') else part.replace('`',''));r.bold=part.startswith('**')

def create_doc(source,dest):
 doc=Document();sec=doc.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.7);sec.right_margin=Inches(.7)
 for name in ['Normal','Body Text']:
  st=doc.styles[name];st.font.name='Calibri';st.font.size=Pt(10);st.font.color.rgb=RGBColor.from_string('251F21');st.paragraph_format.space_after=Pt(6)
 for name,size in [('Title',27),('Heading 1',20),('Heading 2',14),('Heading 3',11)]:
  doc.styles[name].font.name='Calibri';doc.styles[name].font.size=Pt(size);doc.styles[name].font.color.rgb=RGBColor.from_string('315D50')
 text=source.read_text().replace('TEAM_NAME_PENDING',TEAM).replace('MEMBERS_PENDING',META['members'])
 lines=text.splitlines();i=0
 while i<len(lines):
  line=lines[i].strip();i+=1
  if not line:continue
  if line.startswith('|'):
   rows=[line]
   while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
   rows=[[c.strip() for c in s.strip('|').split('|')] for s in rows]
   rows=[r for r in rows if not all(re.fullmatch(r'[-: ]+',c) for c in r)]
   t=doc.add_table(rows=1,cols=len(rows[0]));t.style='Light Shading Accent 1'
   for n,r in enumerate(rows):
    cells=t.rows[0].cells if n==0 else t.add_row().cells
    for c,v in zip(cells,r):
     inline(c.paragraphs[0],v)
     for p in c.paragraphs:
      for run in p.runs:run.font.size=Pt(8.5)
    if n==0:
     trPr=t.rows[0]._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');trPr.append(repeat)
   doc.add_paragraph();continue
  if line.startswith('# '):doc.add_heading(line[2:],level=1)
  elif line.startswith('## '):doc.add_heading(line[3:],level=2)
  elif line.startswith('### '):doc.add_heading(line[4:],level=3)
  elif line.startswith('- '):inline(doc.add_paragraph(style='List Bullet'),line[2:])
  else:inline(doc.add_paragraph(),line)
  if line=='Storyboard descriptions accompany the working-screen captures in the final PDF. The images are examples of the actual local implementation, not substitutes for this text or for the required video.':
   for n,caption in [(1,'The system demonstrates a fictional APA citation through the actual backend. The screen identifies the local mode, scope, source-linked rule and first hint; Continue to co-pilot is available after a successful response.'),(2,'The co-pilot stage loads a synthetic task and gives short instructions. The learner submits the check, inspects its evidence, and chooses when to move on; the interface does not certify mastery.'),(3,'Independent mode removes the task scaffold without removing Help, sources, hints or the person control. The learner may enter a new fictional excerpt or restart guidance, so control stays explicit.')]:
    doc.add_heading('Working screen: stage '+str(n),level=3)
    path=ROOT/'chatbot'/'evidence'/f'onboarding-stage-{n}.png'
    if path.exists():
     shape=doc.add_picture(str(path),width=Inches(6.2));shape._inline.docPr.set('descr',caption)
    doc.add_paragraph(caption)
 footer=sec.footer.paragraphs[0];footer.text='Academic Writing Coach | Weeks 6 and 7 | Transparency';footer.style=doc.styles['Caption']
 doc.save(dest)
 return dest


def spreadsheet():
 rows=json.loads((SOURCE/'test_set.json').read_text());headers=['ID','Prompt','Expected behaviour','Type','Persona','Tests principle?']
 wb=Workbook();ws=wb.active;ws.title='Test Set';ws.append(headers)
 for row in rows:ws.append([row[k] for k in headers])
 ws.freeze_panes='B2';ws.sheet_view.zoomScale=85
 for c in ws[1]:c.font=Font(name='Calibri',size=11,bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='315D50');c.alignment=Alignment(wrap_text=True,vertical='center')
 widths=[9,66,82,18,20,20]
 for i,width in enumerate(widths,1):ws.column_dimensions[chr(64+i)].width=width
 ws.row_dimensions[1].height=34
 for row in ws.iter_rows(min_row=2):
  ws.row_dimensions[row[0].row].height=80
  for c in row:c.font=Font(name='Calibri',size=11,color='251F21');c.alignment=Alignment(wrap_text=True,vertical='top');c.fill=PatternFill('solid',fgColor='F4F6F1' if c.row%2==0 else 'FFFFFF')
 tab=Table(displayName='W67TestSet',ref=f'A1:F{ws.max_row}');tab.tableStyleInfo=TableStyleInfo(name='TableStyleMedium4',showRowStripes=True);ws.add_table(tab)
 for formula,col in [('"normal,edge case,out of scope,unsafe"','D'),('"yes,no"','F')]:
  dv=DataValidation(type='list',formula1=formula);ws.add_data_validation(dv);dv.add(f'{col}2:{col}{ws.max_row}')
 ws.print_title_rows='1:1';ws.sheet_properties.pageSetUpPr.fitToPage=True;ws.page_setup.orientation='landscape';ws.page_setup.paperSize=ws.PAPERSIZE_A3;ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=0;ws.print_options.horizontalCentered=True
 notes=wb.create_sheet('Read me');notes.append(['Test-set notes','Value']);notes.append(['Project','Academic Writing Coach']);notes.append(['Team',META.get('display_team',TEAM)]);notes.append(['Cases',len(rows)]);notes.append(['Data','Fictional/synthetic only. Each row is one prompt, not a real student record.']);notes.append(['Styles','Prompts mentioning APA/MLA/IEEE must use that selector in the app.']);notes.append(['Labels','Expected behaviour is a human-authored test oracle, not a claimed result.']);notes.append(['Principle','Transparency: scope, evidence, rule type, uncertainty and user control.']);notes.append(['Evaluation','Actual local outputs are separate JSON; human semantic review and live API capture are not claimed.']);notes.append(['Limits','Lexical prototype. Context requests and uncertainty are acceptable where the oracle says so; inspect source/rule match.']);notes.column_dimensions['A'].width=23;notes.column_dimensions['B'].width=105
 for row in notes:
  notes.row_dimensions[row[0].row].height=38
  for c in row:c.alignment=Alignment(wrap_text=True,vertical='top');c.font=Font(name='Calibri',size=11)
 path=OUT/(PREFIX+'Test_Set.xlsx');wb.save(path)
 assert ws.max_row==41 and [c.value for c in ws[1]]==headers
 return path

if __name__=='__main__':
 OUT.mkdir(exist_ok=True)
 for source,suffix in [('design_pack.md','Design_Pack'),('prompt_log.md','Prompt_Log')]:create_doc(SOURCE/source,OUT/(PREFIX+suffix+'.docx'))
 spreadsheet()
 print('Generated editable documents and 40-row workbook for',TEAM)
