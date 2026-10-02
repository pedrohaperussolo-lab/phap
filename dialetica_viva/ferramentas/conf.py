# -*- coding: utf-8 -*-
"""Conferência de citações tolerante a OCR, com localização de marcador de página."""
import io, re, os, glob, unicodedata
U='/root/.claude/uploads/9c828e7c-d516-57c5-a1ec-f39162111021/'
CACHE={}
def fonte(frag):
    if frag in CACHE: return CACHE[frag]
    g=[p for p in glob.glob(U+'*') if frag.lower() in os.path.basename(p).lower()]
    assert g, "fonte não encontrada: "+frag
    t=io.open(g[0],encoding='utf-8',errors='replace').read()
    CACHE[frag]=t; return t

def flex(s):
    """regex que tolera espaços/quebras inseridos pelo OCR entre quaisquer caracteres"""
    s=unicodedata.normalize('NFC',s)
    out=[]
    for ch in s:
        if ch.isspace(): out.append(r'[\s\x00-\x08\x0b\x0c\x0e-\x1f\xad-]+')
        elif ch in '\'’‘': out.append(r"['’‘]")
        elif ch in '"“”': out.append(r'["“”]')
        elif ch in '-–—': out.append(r'[-–—]')
        else: out.append(re.escape(ch)+r'[\s\x00-\x08\x0b\x0c\x0e-\x1f\xad]*(?:-[\s]*)?')
    return ''.join(out)

def marcadores(txt):
    """posições dos números de página isolados numa linha, filtradas para
    manter só a maior subsequência crescente (elimina notas de rodapé e
    numeração de listas que o OCR deixa sozinhas numa linha)."""
    bruto=[(m.start(), int(m.group(1))) for m in re.finditer(r'(?m)^[\s]*(\d{1,4})[\s]*$', txt)]
    if not bruto: return []
    import bisect
    vals=[v for _,v in bruto]
    # maior subsequência crescente (índices)
    tails=[]; tidx=[]; pai=[-1]*len(vals)
    for i,v in enumerate(vals):
        j=bisect.bisect_left(tails,v)
        if j==len(tails): tails.append(v); tidx.append(i)
        else: tails[j]=v; tidx[j]=i
        pai[i]=tidx[j-1] if j>0 else -1
    seq=[]; k=tidx[len(tails)-1]
    while k!=-1: seq.append(k); k=pai[k]
    seq.reverse()
    return [bruto[i] for i in seq]

def pagina_de(txt, pos, marks):
    ant=[n for p,n in marks if p<pos]
    dep=[n for p,n in marks if p>pos]
    return (ant[-1] if ant else None, dep[0] if dep else None)

def checar(nota, fragmento_fonte, trecho, pag_alegada=None, rotulo=''):
    t=fonte(fragmento_fonte)
    m=re.search(flex(trecho), t, re.I)
    if not m:
        curto=' '.join(trecho.split()[:7])
        m=re.search(flex(curto), t, re.I)
        if not m:
            print("nota %-4s | %-42s | FRASE NÃO LOCALIZADA" % (nota, rotulo or trecho[:42])); return
        achado='parcial'
    else:
        achado='literal'
    marks=marcadores(t)
    if not marks:
        print("nota %-4s | %-42s | frase %s | sem marcador de página nesta cópia%s"
              % (nota, rotulo or trecho[:42], achado, (" (alegada p. %s)"%pag_alegada) if pag_alegada else ''))
        return
    ant,dep=pagina_de(t,m.start(),marks)
    ver = "p. %s–%s" % (ant,dep)
    if pag_alegada is not None:
        ok = (ant is not None and dep is not None and ant<=int(pag_alegada)<=dep) or ant==int(pag_alegada)
        print("nota %-4s | %-42s | frase %s | alegada p.%-5s | na cópia entre %s | %s"
              % (nota, rotulo or trecho[:42], achado, pag_alegada, ver, "CONFERE" if ok else "DIVERGE"))
    else:
        print("nota %-4s | %-42s | frase %s | na cópia entre %s" % (nota, rotulo or trecho[:42], achado, ver))
