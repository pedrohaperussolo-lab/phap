# -*- coding: utf-8 -*-
import io, re
RUN=re.compile(r'<w:r(?: [^>]*)?>.*?</w:r>', re.S)
TEL=re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
RPR=re.compile(r'<w:rPr>(.*?)</w:rPr>', re.S)
def unesc(s): return s.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'")
def esc(s):   return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def italicize_in(xml, phrase, expect=1):
    """Põe `phrase` em itálico, dividindo o run que a contém."""
    hits=0; out=[]; pos=0
    for m in RUN.finditer(xml):
        r=m.group(0)
        ts=list(TEL.finditer(r))
        if len(ts)!=1: continue
        t=unesc(ts[0].group(1))
        if phrase not in t: continue
        i=t.find(phrase); j=i+len(phrase)
        rpr_m=RPR.search(r); rpr=rpr_m.group(0) if rpr_m else '<w:rPr/>'
        rpr_i=rpr.replace('</w:rPr>','<w:i w:val="1"/><w:iCs w:val="1"/></w:rPr>') if rpr!='<w:rPr/>' else '<w:rPr><w:i w:val="1"/><w:iCs w:val="1"/></w:rPr>'
        def mk(pr, txt): return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (pr, esc(txt))
        new = (mk(rpr, t[:i]) if t[:i] else '') + mk(rpr_i, phrase) + (mk(rpr, t[j:]) if t[j:] else '')
        out.append(xml[pos:m.start()]); out.append(new); pos=m.end(); hits+=1
        if hits>=expect: break
    out.append(xml[pos:])
    if hits!=expect: raise SystemExit("FALHA itálico (%d/%d): %s" % (hits,expect,phrase[:70]))
    return ''.join(out)

def in_footnote(path, fid, fn):
    x=io.open(path,encoding='utf-8').read()
    m=re.search(r'<w:footnote w:id="%d"[^>]*>.*?</w:footnote>'%fid, x, re.S)
    assert m, fid
    seg=fn(m.group(0))
    io.open(path,'w',encoding='utf-8').write(x[:m.start()]+seg+x[m.end():])
