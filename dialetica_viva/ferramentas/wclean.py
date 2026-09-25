# -*- coding: utf-8 -*-
"""Limpeza tipográfica preservando integralmente os runs."""
import io, re
PARA=re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>|<w:p/>', re.S)
TEL =re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
def unesc(s): return s.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'")
def esc(s):   return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def run(path):
    x=io.open(path,encoding='utf-8').read()
    out=[]; pos=0; n=0
    for pm in PARA.finditer(x):
        p=pm.group(0); els=list(TEL.finditer(p))
        if not els: continue
        parts=[unesc(e.group(1)) for e in els]
        orig=list(parts)
        # 1) dentro de cada elemento
        for i,t in enumerate(parts):
            t=t.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'")
            t=re.sub(r'[ \t]{2,}',' ',t)
            t=re.sub(r' +([,;:.!?])',r'\1',t)
            t=re.sub(r'\( +','(',t); t=re.sub(r' +\)',')',t)
            parts[i]=t
        # 2) junções entre elementos
        for i in range(len(parts)-1):
            while parts[i].endswith(' ') and parts[i+1].startswith(' '):
                parts[i+1]=parts[i+1][1:]
            if parts[i].endswith(' ') and re.match(r'[,;:.!?)]', parts[i+1] or ' '):
                parts[i]=parts[i].rstrip(' ')
        # 3) bordas do parágrafo
        if parts: parts[0]=parts[0].lstrip(' ')
        for i in range(len(parts)-1,-1,-1):
            if parts[i].strip()=='' and parts[i]!='':
                parts[i]=''
            elif parts[i]:
                parts[i]=parts[i].rstrip(' '); break
        if parts==orig: continue
        n+=1
        buf=[]; last=0
        for e,np in zip(els,parts):
            buf.append(p[last:e.start()])
            buf.append('<w:t xml:space="preserve">%s</w:t>' % esc(np))
            last=e.end()
        buf.append(p[last:])
        out.append(x[pos:pm.start()]); out.append(''.join(buf)); pos=pm.end()
    out.append(x[pos:])
    io.open(path,'w',encoding='utf-8').write(''.join(out))
    print("%s: %d parágrafos limpos" % (path,n))
