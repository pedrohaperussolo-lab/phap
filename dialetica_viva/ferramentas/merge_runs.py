# -*- coding: utf-8 -*-
import io, re, sys

P = re.compile(r'<w:p [^>]*>.*?</w:p>|<w:p/>', re.S)
R = re.compile(r'<w:r(?: [^>]*)?>(.*?)</w:r>', re.S)
RPR = re.compile(r'^(<w:rPr>.*?</w:rPr>)', re.S)
TONLY = re.compile(r'^(?:<w:rPr>.*?</w:rPr>)?(?:<w:t[^>]*>.*?</w:t>)+$', re.S)
T = re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)

def merge_para(p):
    out=[]; last=0; runs=[]
    for m in R.finditer(p):
        runs.append(m)
    if not runs: return p
    # group consecutive runs (adjacent in source, nothing between but whitespace)
    res=[]; i=0
    while i < len(runs):
        m=runs[i]; inner=m.group(1)
        if not TONLY.match(inner):
            res.append((m.start(), m.end(), None)); i+=1; continue
        rpr = RPR.match(inner)
        rpr = rpr.group(1) if rpr else ''
        j=i+1; txt=''.join(T.findall(inner)); end=m.end()
        while j < len(runs):
            m2=runs[j]
            if p[end:m2.start()].strip(): break
            in2=runs[j].group(1)
            if not TONLY.match(in2): break
            r2=RPR.match(in2); r2=r2.group(1) if r2 else ''
            if r2 != rpr: break
            txt += ''.join(T.findall(in2)); end=m2.end(); j+=1
        if j>i+1:
            new='<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, txt)
            res.append((m.start(), end, new))
        else:
            res.append((m.start(), m.end(), None))
        i=j
    buf=[]; pos=0
    for s,e,new in res:
        buf.append(p[pos:s]); buf.append(new if new is not None else p[s:e]); pos=e
    buf.append(p[pos:])
    return ''.join(buf)

def process(path):
    x=io.open(path,encoding='utf-8').read()
    out=[]; pos=0; n=0
    for m in P.finditer(x):
        np=merge_para(m.group(0))
        if np!=m.group(0): n+=1
        out.append(x[pos:m.start()]); out.append(np); pos=m.end()
    out.append(x[pos:])
    io.open(path,'w',encoding='utf-8').write(''.join(out))
    print("%s: %d parágrafos com runs fundidos" % (path, n))

for p in sys.argv[1:]:
    process(p)
