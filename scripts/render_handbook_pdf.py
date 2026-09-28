from pathlib import Path
import re, textwrap, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

root=Path(__file__).resolve().parents[1]
fontroot=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('NW','DejaVuSans.ttf'),('NWB','DejaVuSans-Bold.ttf'),('NWI','DejaVuSans-Oblique.ttf'),('NWM','DejaVuSansMono.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(fontroot/file)))
pdfmetrics.registerFontFamily('NW',normal='NW',bold='NWB',italic='NWI',boldItalic='NWB')
ink=colors.HexColor('#183446');teal=colors.HexColor('#147c72');muted=colors.HexColor('#607382')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyNW',fontName='NW',fontSize=9.2,leading=14.1,textColor=ink,spaceAfter=8,splitLongWords=True))
styles.add(ParagraphStyle(name='H1NW',fontName='NWB',fontSize=20,leading=26,textColor=ink,spaceAfter=17,spaceBefore=6,keepWithNext=True))
styles.add(ParagraphStyle(name='H2NW',fontName='NWB',fontSize=13,leading=18,textColor=teal,spaceAfter=10,spaceBefore=17,keepWithNext=True))
styles.add(ParagraphStyle(name='H3NW',fontName='NWB',fontSize=10.5,leading=15,textColor=ink,spaceAfter=8,spaceBefore=12,keepWithNext=True))
styles.add(ParagraphStyle(name='CodeNW',fontName='NWM',fontSize=7.3,leading=11,textColor=ink,backColor=colors.HexColor('#edf3f5'),borderPadding=10,spaceBefore=8,spaceAfter=13))
styles.add(ParagraphStyle(name='SmallNW',fontName='NW',fontSize=8,leading=12,textColor=muted,spaceAfter=8))
styles.add(ParagraphStyle(name='CoverTitle',fontName='NWB',fontSize=38,leading=43,textColor=ink,spaceAfter=18))
styles.add(ParagraphStyle(name='CoverSub',fontName='NW',fontSize=16,leading=23,textColor=teal,spaceAfter=16))

def inline(text):
 t=html.escape(text)
 t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
 t=re.sub(r'`([^`]+)`',r'<font name="NWM" size="8">\1</font>',t)
 return t

pdf=root/'NeuroWeave_English_Handbook.pdf'
story=[]
story.append(Spacer(1,45))
story.append(Paragraph('ENGLISH RESEARCH RELEASE / VERSION 1.0.0',styles['SmallNW']))
story.append(Spacer(1,20))
story.append(Paragraph('DIKWP<br/>NeuroWeave Lab',styles['CoverTitle']))
story.append(Paragraph('The executable companion to<br/><i>A Brief History of the Brain</i>',styles['CoverSub']))
story.append(Spacer(1,16))
story.append(Paragraph('Engineering and Research Handbook',styles['H2NW']))
story.append(Paragraph('Book authors: Yucong Duan and Zhongdao Wu',styles['BodyNW']))
story.append(Paragraph('18 chapter-linked experiments<br/>Reconstructive memory and state-pinned plans<br/>Label-isolated evaluation and reproducible artifacts',styles['BodyNW']))
story.append(Spacer(1,23))
story.append(Paragraph('Prepared 27 September 2026',styles['BodyNW']))
story.append(Paragraph('Original English companion software and documentation. The named book authors are credited for the manuscript; author review or independent validation of this new implementation is not asserted.',styles['SmallNW']))
story.append(Spacer(1,16))
story.append(Paragraph('Source code: MIT licence. Local Python execution. All bundled experimental evidence is synthetic. The manuscript and upstream archives are not redistributed.',styles['SmallNW']))
story.append(PageBreak())
story.append(Paragraph('Reader navigation',styles['H1NW']))
for text in ['1. The central engineering contribution','2. What readers can run immediately','3. Architectural map','4. Executing the book\'s minimal state model','5. Two finite propositions made executable','6. Numerical models and their equations','7. Complete 18-chapter laboratory curriculum','8. Memory, provenance and runtime API','9. Evaluation and explicit denominators','10. Verification and release integrity','11. Practical extension','12. Attribution and primary sources','Appendix A. Bounded upstream source audit']:
 story.append(Paragraph(text,styles['BodyNW']))
story.append(Spacer(1,10))
story.append(Paragraph('Start with section 2 to run the system. Use chapter 10 for dependency-aware memory, chapter 13 for competing functional realizations, chapter 16 for the integrated state loop, and chapter 17 for the consent protocol.',styles['BodyNW']))
text=(root/'docs/HANDBOOK.md').read_text();text=text[text.index('# 1. The central'):]
# Limit page-break frequency while keeping each main section easy to locate.
para=[];code=[];in_code=False
htmlparts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NeuroWeave English Handbook</title><style>body{font:17px/1.7 system-ui;color:#183446;background:#f0f4f6;margin:0}main{max-width:940px;margin:auto;background:white;padding:55px}h1{font-size:33px;line-height:1.25;border-bottom:2px solid #147c72;padding-bottom:15px;margin-top:55px}h2{color:#147c72;margin-top:35px;font-size:24px}h3{font-size:20px}pre{font:13px/1.6 monospace;padding:20px;background:#edf3f5;overflow:auto}p{overflow-wrap:anywhere}header{background:#183446;color:white;padding:45px;font-size:30px}code{font-size:.85em}footer{font-size:13px;padding:40px;text-align:center}@media(max-width:700px){main{padding:24px}}</style><header>DIKWP NeuroWeave Lab<br>English Engineering and Research Handbook</header><main>']

def flush():
 if para:
  raw=' '.join(para);story.append(Paragraph(inline(raw),styles['BodyNW']));htmlparts.append('<p>'+inline(raw)+'</p>');para.clear()

for line in text.splitlines():
 if line.startswith('```'):
  flush()
  if in_code:
   wrapped=[]
   for x in code:
    wrapped+=textwrap.wrap(x,width=92,replace_whitespace=False,drop_whitespace=False) or ['']
   story.append(Preformatted('\n'.join(wrapped),styles['CodeNW']))
   htmlparts.append('<pre>'+html.escape('\n'.join(code))+'</pre>')
   code=[]
  in_code=not in_code;continue
 if in_code:code.append(line);continue
 if not line.strip():flush();continue
 if line.startswith('#'):
  flush();level=len(line)-len(line.lstrip('#'));heading=line[level:].strip()
  if level==1:
   story.append(PageBreak());sty=styles['H1NW']
  elif level==2:sty=styles['H2NW']
  else:sty=styles['H3NW']
  story.append(Paragraph(inline(heading),sty));htmlparts.append(f'<h{min(level,3)}>{inline(heading)}</h{min(level,3)}>')
 elif line.startswith('- '):
  flush();story.append(Paragraph('• '+inline(line[2:]),styles['BodyNW']));htmlparts.append('<p>• '+inline(line[2:])+'</p>')
 else:para.append(line)
flush();htmlparts.append('</main><footer>Version 1.0.0 · 27 September 2026 · MIT companion software · Synthetic evidence</footer></html>')
(root/'docs/HANDBOOK.html').write_text(''.join(htmlparts),encoding='utf-8')

def footer(canvas,doc):
 canvas.saveState();W,H=doc.pagesize
 if doc.page>1:
  canvas.setStrokeColor(colors.HexColor('#d6e1e7'));canvas.line(48,43,W-48,43)
  canvas.setFont('NW',7);canvas.setFillColor(muted)
  canvas.drawString(48,29,'NEUROWEAVE LAB 1.0.0  |  ENGINEERING & RESEARCH HANDBOOK')
  canvas.drawRightString(W-48,29,str(doc.page))
 canvas.restoreState()

doc=SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=48,bottomMargin=57,
                     title='DIKWP NeuroWeave Lab: English Engineering and Research Handbook',author='NeuroWeave contributors')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(pdf)
