# -*- coding: utf-8 -*-
"""Aplica itálico a termos estrangeiros e títulos no corpo do texto, poupando o que já está em itálico e as listas de referências."""
import io, re
PARA=re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>|<w:p/>', re.S)
RUN =re.compile(r'<w:r(?: [^>]*)?>.*?</w:r>', re.S)
TEL =re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
RPR =re.compile(r'<w:rPr>.*?</w:rPr>', re.S)
def unesc(s): return s.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'")
def esc(s):   return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def eh_referencia(t):
    return bool(re.match(r'^[A-ZÀ-ÝŽ][^.]{0,45}[,.] ', t) or re.match(r'^(Sófocles|Jung, C\.)', t))

def aplicar(path, termos, excluir=()):
    x=io.open(path,encoding='utf-8').read()
    paras=list(PARA.finditer(x))
    ref=False; alvo=[]
    for i,m in enumerate(paras):
        t=unesc(''.join(TEL.findall(m.group(0)))).strip()
        if t in ('Referências do capítulo','Referências'): ref=True; continue
        if ref:
            if not t: continue
            if eh_referencia(t): continue
            ref=False
        alvo.append(i)
    alvo=set(alvo)
    excl=set(excluir)
    total=0; falhas=[]
    novos={}
    for i,m in enumerate(paras):
        if i not in alvo: continue
        p=m.group(0); mudou=False
        for termo in termos:
            rx=re.compile(r'(?<![\wÀ-ÿ])'+re.escape(termo)+r'(?![\wÀ-ÿ])')
            while True:
                runs=list(RUN.finditer(p)); achou=False
                for r in runs:
                    if '<w:i ' in r.group(0): continue
                    ts=list(TEL.finditer(r.group(0)))
                    if len(ts)!=1: continue
                    txt=unesc(ts[0].group(1))
                    mm=rx.search(txt)
                    if not mm: continue
                    if (i,termo) in excl:
                        # pula esta ocorrência específica marcando-a temporariamente
                        continue
                    a,b=mm.start(),mm.end()
                    rpr_m=RPR.search(r.group(0)); rpr=rpr_m.group(0) if rpr_m else '<w:rPr/>'
                    rpr_i=(rpr[:-len('</w:rPr>')]+'<w:i w:val="1"/><w:iCs w:val="1"/></w:rPr>') if rpr!='<w:rPr/>' else '<w:rPr><w:i w:val="1"/><w:iCs w:val="1"/></w:rPr>'
                    def mk(pr,s): return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'%(pr,esc(s))
                    novo=(mk(rpr,txt[:a]) if txt[:a] else '')+mk(rpr_i,txt[a:b])+(mk(rpr,txt[b:]) if txt[b:] else '')
                    p=p[:r.start()]+novo+p[r.end():]
                    total+=1; mudou=True; achou=True
                    break
                if not achou: break
        if mudou: novos[i]=p
    out=[];pos=0
    for i,m in enumerate(paras):
        if i in novos:
            out.append(x[pos:m.start()]); out.append(novos[i]); pos=m.end()
    out.append(x[pos:])
    io.open(path,'w',encoding='utf-8').write(''.join(out))
    return total
