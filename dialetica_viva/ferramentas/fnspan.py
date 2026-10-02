import re
P='src/word/footnotes.xml'
def note(fid, f=None):
    f = f if f is not None else open(P).read()
    m=re.search(r'<w:footnote w:id="%d">.*?</w:footnote>'%fid, f, re.S)
    return f, m
def replace_span(fid, start_txt, end_txt, repl=''):
    """Substitui, no texto concatenado da nota, de start_txt até o fim de end_txt."""
    f,m = note(fid)
    b=m.group(0)
    runs=list(re.finditer(r'(<w:r\b.*?<w:t(?: [^>]*)?>)(.*?)(</w:t>.*?</w:r>)', b, re.S))
    txts=[r.group(2) for r in runs]
    full=''.join(txts)
    i=full.find(start_txt); assert i>=0, ('start',fid)
    j=full.find(end_txt, i); assert j>=0, ('end',fid)
    j+=len(end_txt)
    # mapear offsets
    out=[]; pos=0
    for r,t in zip(runs,txts):
        a,b2=pos,pos+len(t)
        keep=''
        if b2<=i or a>=j: keep=t
        else:
            keep = t[:max(0,i-a)] + (repl if a<=i<b2 else '') + t[max(0,min(len(t),j-a)):]
        out.append((r,keep)); pos=b2
    nb=b; 
    for r,keep in reversed(out):
        nb = nb[:r.start()] + r.group(1)+keep+r.group(3) + nb[r.end():]
    f=f[:m.start()]+nb+f[m.end():]
    open(P,'w').write(f)
