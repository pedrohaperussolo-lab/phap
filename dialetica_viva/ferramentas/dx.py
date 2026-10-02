import re
PATH='src/word/document.xml'
def raw(): return open(PATH).read()
def split(x=None):
    x = x if x is not None else raw()
    head,rest = x.split('<w:body>',1)
    head += '<w:body>'
    ps = re.split(r'(?=<w:p[ >])', rest)
    pre = ps[0]; ps=ps[1:]
    # last element contains tail after last </w:p>
    last = ps[-1]
    i = last.rindex('</w:p>')+len('</w:p>')
    tail = last[i:]; ps[-1]=last[:i]
    return head, pre, ps, tail
def join(head,pre,ps,tail): return head+pre+''.join(ps)+tail
def write(head,pre,ps,tail): open(PATH,'w').write(join(head,pre,ps,tail))
def ptext(p): return ''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>',p))
RPR='<w:rPr><w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>%s<w:color w:val="000000"/><w:sz w:val="%d"/><w:szCs w:val="%d"/><w:rtl w:val="0"/></w:rPr>'
def run(t,it=False,sz=24):
    return '<w:r>'+(RPR%('<w:i w:val="1"/><w:iCs w:val="1"/>' if it else '',sz,sz))+'<w:t xml:space="preserve">'+t+'</w:t></w:r>'
def bibpara(segs):
    ppr='<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:ind w:left="720" w:hanging="720"/><w:jc w:val="both"/><w:rPr/></w:pPr>'
    return '<w:p>'+ppr+''.join(run(t,i) for t,i in segs)+'</w:p>'
def bodypara(segs, ppr=None):
    ppr = ppr or '<w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="720"/><w:jc w:val="both"/><w:rPr/></w:pPr>'
    return '<w:p>'+ppr+''.join(run(t,i) for t,i in segs)+'</w:p>'

def rebuild(p, segs, sz=24, keep_tail_from_fn=True):
    """Rebuild paragraph p with new runs, preserving pPr and any trailing footnote run(s)."""
    m=re.match(r'(<w:p\b[^>]*>)(<w:pPr>.*?</w:pPr>)?',p,re.S)
    head=m.group(0)
    tail=''
    if keep_tail_from_fn:
        i=p.find('<w:r ')
        # locate first run containing footnoteReference
        for mm in re.finditer(r'<w:r\b.*?</w:r>',p,re.S):
            if 'footnoteReference' in mm.group(0):
                tail=p[mm.start():]
                break
        if not tail:
            tail='</w:p>'
    else:
        tail='</w:p>'
    return head+''.join(run(t,i,sz) for t,i in segs)+tail
