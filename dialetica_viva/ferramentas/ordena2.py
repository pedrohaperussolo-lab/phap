# -*- coding: utf-8 -*-
"""Ordena cada bloco de mesmo autor, em cada lista de referências, por ano e depois título."""
import dx, re, unicodedata
def _n(s):
    s=unicodedata.normalize('NFD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9 ]','',s).strip()
def _chave(t):
    m=re.match(r'(.{0,70}?)\s*\((\d{4})([a-z]?)(?:,[^)]*)?\)\.\s*(.{0,60})', t)
    if not m: return None
    return _n(m.group(1)), (int(m.group(2)), m.group(3), _n(m.group(4)))
def ordenar():
    h,pre,ps,tail=dx.split()
    T=[dx.ptext(p) for p in ps]
    hdr=[i for i,t in enumerate(T) if t.startswith('Referências')]
    movidos=0
    for j,ini in enumerate(hdr):
        fim=hdr[j+1] if j+1<len(hdr) else len(ps)
        i=ini+1
        while i < fim:
            if 'w:hanging="720"' not in ps[i] or not _chave(T[i]): i+=1; continue
            aut=_chave(T[i])[0]
            k=i
            while (k+1 < fim and 'w:hanging="720"' in ps[k+1] and _chave(T[k+1])
                   and _chave(T[k+1])[0]==aut): k+=1
            if k>i:
                bloco=sorted(zip(T[i:k+1], ps[i:k+1]), key=lambda x:_chave(x[0])[1])
                if [b[1] for b in bloco] != ps[i:k+1]: movidos += k-i+1
                ps[i:k+1]=[b[1] for b in bloco]; T[i:k+1]=[b[0] for b in bloco]
            i=k+1
    dx.write(h,pre,ps,tail)
    return movidos
