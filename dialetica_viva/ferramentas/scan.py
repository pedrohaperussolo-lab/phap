# -*- coding: utf-8 -*-
import io, re
PARA=re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>|<w:p/>', re.S)
RUN =re.compile(r'<w:r(?: [^>]*)?>.*?</w:r>', re.S)
TEL =re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)
def unesc(s): return s.replace('&amp;','&').replace('&quot;','"').replace('&lt;','<').replace('&gt;','>')

def corpo(path='src/word/document.xml'):
    """Devolve [(idx, texto, [(ini,fim,italico)])] só dos parágrafos de texto corrido."""
    x=io.open(path,encoding='utf-8').read()
    saida=[]; ref=False
    for i,m in enumerate(PARA.finditer(x)):
        p=m.group(0); t=unesc(''.join(TEL.findall(p))).strip()
        if t in ('Referências do capítulo','Referências'): ref=True; continue
        if ref:
            if not t: continue
            if re.match(r'^[A-ZÀ-ÝŽ][^.]{0,45}[,.] ', t) or re.match(r'^(Sófocles|Jung, C)', t): continue
            ref=False
        spans=[]; off=0
        for r in RUN.finditer(p):
            s=unesc(''.join(TEL.findall(r.group(0))))
            if not s: continue
            it = '<w:i ' in r.group(0)
            spans.append((off, off+len(s), it)); off+=len(s)
        saida.append((i, ''.join(unesc(''.join(TEL.findall(r.group(0)))) for r in RUN.finditer(p)), spans))
    return saida

def status(txt, spans, a, b):
    """True se o intervalo [a,b) está inteiramente em itálico."""
    for s,e,it in spans:
        if e<=a or s>=b: continue
        if not it: return False
    return True

def scan(termos, path='src/word/document.xml'):
    C=corpo(path)
    for termo in termos:
        it=0; nit=0; exemplos=[]
        rx=re.compile(r'(?<![\wÀ-ÿ])'+re.escape(termo)+r'(?![\wÀ-ÿ])')
        for i,t,spans in C:
            for m in rx.finditer(t):
                if status(t,spans,m.start(),m.end()): it+=1
                else:
                    nit+=1
                    if len(exemplos)<2: exemplos.append((i, t[max(0,m.start()-45):m.end()+35]))
        if it or nit:
            print("%-52s itálico=%-4d sem=%-4d" % (termo[:52], it, nit))
            for i,e in exemplos: print("        %4d …%s…" % (i,e.replace('\n',' ')))
