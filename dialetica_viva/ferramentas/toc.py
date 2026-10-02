# -*- coding: utf-8 -*-
import dx, re, sys
def entries():
    h,pre,ps,tail=dx.split()
    out=[]
    for i,p in enumerate(ps):
        if '<w:tab/>' in p and 'w:leader="dot"' in p:
            out.append(i)
    return h,pre,ps,tail,out
def setpage(p, n):
    return re.sub(r'(<w:tab/><w:t xml:space="preserve">)\d+(</w:t>)', r'\g<1>%d\g<2>'%n, p, count=1)
def addentry(ps, after_idx, label, page):
    tmpl=ps[after_idx]
    new=re.sub(r'(<w:t xml:space="preserve">)[^<]*(</w:t></w:r><w:r>)', r'\g<1>'+label+r'\g<2>', tmpl, count=1)
    new=setpage(new, page)
    ps.insert(after_idx+1, new)
if __name__=='__main__':
    h,pre,ps,tail,idx=entries()
    print(len(idx), idx)
    for i in idx: print(i, dx.ptext(ps[i]))
