# -*- coding: utf-8 -*-
"""Converte citações longas em citações recuadas (padrão APA) e uniformiza as existentes."""
import io, re

PARA=re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>|<w:p/>', re.S)
RUN =re.compile(r'<w:r(?: [^>]*)?>.*?</w:r>', re.S)
TEL =re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
PPR =re.compile(r'<w:pPr>.*?</w:pPr>', re.S)
def unesc(s): return s.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'")
def esc(s):   return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

FONT='<w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>'
BQ_PPR=('<w:pPr><w:spacing w:after="160" w:before="140" w:line="320" w:lineRule="auto"/>'
        '<w:ind w:left="720" w:right="0" w:firstLine="0"/><w:jc w:val="both"/>'
        '<w:rPr>'+FONT+'<w:color w:val="000000"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:pPr>')

def shrink(run_xml):
    """Força corpo 11pt nos runs da citação recuada."""
    s=run_xml
    s=re.sub(r'<w:sz w:val="\d+"/>','<w:sz w:val="22"/>',s)
    s=re.sub(r'<w:szCs w:val="\d+"/>','<w:szCs w:val="22"/>',s)
    if '<w:sz ' not in s:
        if '<w:rPr>' in s:
            s=s.replace('<w:rPr>','<w:rPr>'+FONT+'<w:sz w:val="22"/><w:szCs w:val="22"/>',1)
        else:
            s=re.sub(r'(<w:r(?: [^>]*)?>)',r'\1<w:rPr>'+FONT+'<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>',s,1)
    return s

def split_para(p, qstart, qend):
    """Divide o parágrafo em (antes, citação, depois)."""
    ppr_m = PPR.search(p)
    ppr = ppr_m.group(0) if ppr_m else ''
    body_start = ppr_m.end() if ppr_m else re.match(r'<w:p(?: [^>]*)?>', p).end()
    body_end = p.rfind('</w:p>')
    items=[]; pos=body_start
    for m in RUN.finditer(p, body_start, body_end):
        if m.start()>pos: items.append(('x', p[pos:m.start()], ''))
        items.append(('r', m.group(0), unesc(''.join(TEL.findall(m.group(0))))))
        pos=m.end()
    if pos<body_end: items.append(('x', p[pos:body_end], ''))
    A=[];B=[];C=[]; off=0
    for kind, xml, txt in items:
        a, b = off, off+len(txt)
        off = b
        if kind!='r' or not txt:
            (A if b<=qstart else (B if a<qend else C)).append(xml)
            continue
        pre = txt[:max(0,min(len(txt), qstart-a))] if a < qstart else ''
        mid = txt[max(0,qstart-a):min(len(txt), qend-a)] if b>qstart and a<qend else ''
        post= txt[max(0,qend-a):] if b>qend else ''
        def rewrite(t):
            return re.sub(r'<w:t(?: [^>]*)?>.*?</w:t>', '<w:t xml:space="preserve">%s</w:t>'%esc(t), xml, count=1, flags=re.S)
        if pre:  A.append(rewrite(pre))
        if mid:  B.append(rewrite(mid))
        if post: C.append(rewrite(post))
    # notas que vêm logo depois do fecho das aspas migram para dentro da citação
    while C and 'footnoteReference' in C[0]:
        B.append(C.pop(0))
    return ppr, A, B, C

def text_of(runs):
    return unesc(''.join(''.join(TEL.findall(r)) for r in runs))

def set_text_first(runs, fn):
    for i,r in enumerate(runs):
        ts=TEL.findall(r)
        if ts:
            t=unesc(ts[0]); runs[i]=re.sub(r'<w:t(?: [^>]*)?>.*?</w:t>','<w:t xml:space="preserve">%s</w:t>'%esc(fn(t)),r,count=1,flags=re.S); return
def set_text_last(runs, fn):
    for i in range(len(runs)-1,-1,-1):
        ts=TEL.findall(runs[i])
        if ts:
            t=unesc(ts[-1]); 
            parts=list(TEL.finditer(runs[i])); m=parts[-1]
            runs[i]=runs[i][:m.start()]+'<w:t xml:space="preserve">%s</w:t>'%esc(fn(t))+runs[i][m.end():]; return
