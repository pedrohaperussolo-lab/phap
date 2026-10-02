# -*- coding: utf-8 -*-
import dx, re, unicodedata
def chave(t):
    m=re.match(r'Jung, C\. G\. \((\d{4})(?:, [^)]*)?\)\.\s*(.*)', t)
    ano=int(m.group(1)); resto=m.group(2)
    tit=re.split(r'\s*\(Obras completas|\s*\(\w\.|\s*\(R\. F\.|\s*\(S\. Shamdasani|\s*\(A\. Jaffé', resto)[0].strip(' .')
    tit=unicodedata.normalize('NFD',tit).encode('ascii','ignore').decode().lower()
    return (ano, tit)
def ordenar():
    h,pre,ps,tail=dx.split()
    T=[dx.ptext(p) for p in ps]
    hdr=[i for i,t in enumerate(T) if t.startswith('Referências')]
    total=0
    for j,ini in enumerate(hdr):
        fim = hdr[j+1] if j+1<len(hdr) else len(ps)
        # blocos contíguos de entradas Jung
        i=ini+1
        while i < fim:
            if T[i].startswith('Jung, C. G.') and 'w:hanging="720"' in ps[i]:
                k=i
                while k+1 < fim and T[k+1].startswith('Jung, C. G.') and 'w:hanging="720"' in ps[k+1]: k+=1
                if k>i:
                    bloco=list(zip(T[i:k+1], ps[i:k+1]))
                    bloco.sort(key=lambda x: chave(x[0]))
                    ps[i:k+1]=[b[1] for b in bloco]
                    T[i:k+1]=[b[0] for b in bloco]
                    total += k-i+1
                i=k+1
            else: i+=1
    dx.write(h,pre,ps,tail)
    return total
