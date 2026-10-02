# -*- coding: utf-8 -*-
import re
ANO = {
 'V':'2016', 'VI':'2015', 'VII/1':'2013', 'VII/2':'2014',
 'VIII/1':'2014', 'VIII/2':'2014', 'IX/1':'2016', 'IX/2':'2015',
 'XI/1':'1978', 'XI/2':'2013', 'XI/3':'2013', 'XI/4':'2013',
 'XI/5':'2013', 'XI/6':'2013', 'XIV/1':'2015', 'XIV/2':'2015',
 'XVI/1':'2013', 'XVI/2':'2013', 'XVIII/1':'2015', 'XVIII/2':'2015',
}
RUN = re.compile(r'(<w:r\b.*?<w:t(?: [^>]*)?>)(.*?)(</w:t>.*?</w:r>)', re.S)
JUNG = re.compile(r'Jung, C\. G\. \((s\.d\.|\d{4})\)\. ')
VOL  = re.compile(r'Obras completas, Vol\. ([IVXL]+(?:/\d)?)')

def fix_block(b, log):
    runs=list(RUN.finditer(b))
    txts=[r.group(2) for r in runs]
    out=list(txts); changed=False
    for i,t in enumerate(txts):
        for m in JUNG.finditer(t):
            rest = t[m.end():] + ''.join(txts[i+1:i+6])
            vm = VOL.search(rest)
            if not vm: continue
            vol = vm.group(1); novo = ANO.get(vol)
            if not novo: log.append(('SEM MAPA', vol)); continue
            velho = m.group(1)
            if velho == novo: continue
            out[i] = out[i].replace('Jung, C. G. (%s). '%velho, 'Jung, C. G. (%s). '%novo, 1)
            txts[i] = out[i]
            log.append((vol, velho, novo)); changed=True
    if not changed: return b
    nb=b
    for r,new in reversed(list(zip(runs,out))):
        nb = nb[:r.start()] + r.group(1)+new+r.group(3) + nb[r.end():]
    return nb

def run(path, splitter):
    x=open(path).read()
    parts=re.split(splitter, x); log=[]
    parts=[fix_block(p, log) for p in parts]
    open(path,'w').write(''.join(parts))
    return log
