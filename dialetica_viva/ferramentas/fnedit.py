import re,sys
PATH='src/word/footnotes.xml'
def load(): return open(PATH).read()
def save(x): open(PATH,'w').write(x)
def block(x,fid):
    m=re.search(r'<w:footnote w:id="%d">.*?</w:footnote>'%fid,x,re.S)
    return m
def edit(fid, pairs):
    x=load(); m=block(x,fid)
    if not m: raise SystemExit('no note %d'%fid)
    b=m.group(0); orig=b
    for old,new in pairs:
        n=b.count(old)
        if n!=1: raise SystemExit('note %d: %d matches for %r'%(fid,n,old[:70]))
        b=b.replace(old,new)
    save(x[:m.start()]+b+x[m.end():])
    print('note id %d ok'%fid)
