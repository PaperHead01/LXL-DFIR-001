#!/usr/bin/env python3
"""Markdown -> .docx for the LXL-DFIR-001 report.

Handles: h1-h3, paragraphs, bold/italic inline, bullet + numbered lists,
pipe tables, fenced code blocks, blockquotes, horizontal rules.
Adds a page footer carrying the classification, on every page.
"""
import re, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CLASSIFICATION = "SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE"

def add_footer(section):
    p = section.footer.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(CLASSIFICATION)
    r.font.size = Pt(7.5)
    r.font.color.rgb = RGBColor(0x99, 0x00, 0x00)
    r.bold = True

def add_borders(par, color="CCCCCC"):
    pPr = par._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    for edge in ('top', 'bottom'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '6')
        e.set(qn('w:space'), '4'); e.set(qn('w:color'), color)
        pbdr.append(e)
    pPr.append(pbdr)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto')
    sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)

INLINE = re.compile(r'(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`)')

def add_runs(par, text):
    for tok in INLINE.split(text):
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = par.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = par.add_run(tok[1:-1]); r.font.name = 'Consolas'; r.font.size = Pt(8.5)
        elif tok.startswith('*') and tok.endswith('*') and len(tok) > 2:
            r = par.add_run(tok[1:-1]); r.italic = True
        else:
            par.add_run(tok)

def build(md_path, out_path):
    lines = open(md_path, encoding='utf-8').read().split('\n')
    doc = Document()

    st = doc.styles['Normal']
    st.font.name = 'Calibri'; st.font.size = Pt(10)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.08

    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(0.8)
        s.left_margin = s.right_margin = Inches(0.85)
        add_footer(s)

    i, n = 0, len(lines)
    in_code = False
    code_buf = []

    while i < n:
        ln = lines[i]

        if ln.startswith('```'):
            if in_code:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(8)
                r = p.add_run('\n'.join(code_buf))
                r.font.name = 'Consolas'; r.font.size = Pt(8)
                add_borders(p)
                code_buf = []; in_code = False
            else:
                in_code = True
            i += 1; continue

        if in_code:
            code_buf.append(ln); i += 1; continue

        if not ln.strip():
            i += 1; continue

        if ln.strip() == '---':
            p = doc.add_paragraph(); add_borders(p, "999999"); i += 1; continue

        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(24)
                p.paragraph_format.space_after = Pt(10)
                r = p.add_run(txt); r.bold = True; r.font.size = Pt(18)
                r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
            elif lvl == 2:
                doc.add_page_break()
                h = doc.add_heading(txt, level=1)
                for r in h.runs: r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
            elif lvl == 3:
                h = doc.add_heading(txt, level=2)
                for r in h.runs: r.font.color.rgb = RGBColor(0x2E, 0x54, 0x94)
            else:
                h = doc.add_heading(txt, level=3)
                for r in h.runs: r.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
            i += 1; continue

        # table
        if ln.lstrip().startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i+1]):
            header = [c.strip() for c in ln.strip().strip('|').split('|')]
            i += 2
            rows = []
            while i < n and lines[i].lstrip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            tbl = doc.add_table(rows=1, cols=len(header))
            tbl.style = 'Table Grid'
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            for j, h in enumerate(header):
                cell = tbl.rows[0].cells[j]
                cell.text = ''
                par = cell.paragraphs[0]
                r = par.add_run(h); r.bold = True; r.font.size = Pt(8.5)
                shade(cell, 'E8EDF5')
            for row in rows:
                cells = tbl.add_row().cells
                for j in range(len(header)):
                    val = row[j] if j < len(row) else ''
                    cells[j].text = ''
                    par = cells[j].paragraphs[0]
                    par.paragraph_format.space_after = Pt(0)
                    add_runs(par, val)
                    for r in par.runs:
                        if r.font.size is None: r.font.size = Pt(8.5)
            doc.add_paragraph()
            continue

        if ln.startswith('>'):
            buf = []
            while i < n and lines[i].startswith('>'):
                buf.append(lines[i].lstrip('>').strip()); i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            add_runs(p, ' '.join(x for x in buf if x))
            for r in p.runs:
                r.italic = True
                if r.font.size is None: r.font.size = Pt(9.5)
            add_borders(p, "B0B0B0")
            continue

        mi = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', ln.strip())
        if mi:
            alt, src = mi.group(1), mi.group(2)
            try:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(2)
                p.add_run().add_picture(src, width=Inches(6.3))
                if alt:
                    cap = doc.add_paragraph()
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = cap.add_run(alt)
                    r.italic = True; r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)
                    cap.paragraph_format.space_after = Pt(10)
            except Exception as e:
                doc.add_paragraph(f"[image not embedded: {src} — {e}]")
            i += 1; continue

        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', ln)
        if m:
            indent = len(m.group(1)) // 2
            style = 'List Number' if re.match(r'\d+\.', m.group(2)) else 'List Bullet'
            p = doc.add_paragraph(style=style)
            p.paragraph_format.left_indent = Inches(0.3 + 0.25 * indent)
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, m.group(3))
            i += 1; continue

        p = doc.add_paragraph()
        add_runs(p, ln.strip())
        i += 1

    doc.save(out_path)
    print(f"wrote {out_path}")

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
