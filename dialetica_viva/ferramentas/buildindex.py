# -*- coding: utf-8 -*-
import dx, mkindex, re

def _faixas():
    """Calcula as faixas de exposição principal a partir do PDF atual."""
    import repag
    f, refs, n = repag.extrair()
    H = f
    def ate(ini, prox):   # última página antes do capítulo seguinte, descontando as refs
        return prox - 2
    return {
     "Jung, C. G.": "passim; exposição principal nas Estações 4, 5 e 6, pp. %d-%d" % (H['4. Jung I'], ate(H['4. Jung I'], H['7. Giegerich I'])),
     "Hegel, G. W. F.": "passim; exposição principal nas Estações 2 e 3, pp. %d-%d" % (H['2. Hegel I'], ate(H['2. Hegel I'], H['4. Jung I'])),
     "Deleuze, Gilles": "passim; exposição principal nas Estações 10 e 11, pp. %d-%d" % (H['10. Deleuze I'], ate(H['10. Deleuze I'], H['12. Síntese'])),
     "Giegerich, Wolfgang": "passim; exposição principal nas Estações 7 e 8, pp. %d-%d" % (H['7. Giegerich I'], ate(H['7. Giegerich I'], H['9. Excurso'])),
     "Lacan, Jacques": "passim; exposição principal na Estação 9, pp. %d-%d" % (H['9. Excurso'], ate(H['9. Excurso'], H['10. Deleuze I'])),
    }
PASSIM = _faixas()


def ranges(pgs):
    out=[]; i=0
    while i < len(pgs):
        j=i
        while j+1 < len(pgs) and pgs[j+1]==pgs[j]+1: j+=1
        out.append(str(pgs[i]) if j==i else ('%d-%d'%(pgs[i],pgs[j])))
        i=j+1
    return ', '.join(out)

def key(d):
    s=d.split('(')[0].strip().rstrip(',')
    import unicodedata
    return unicodedata.normalize('NFD',s).encode('ascii','ignore').decode().lower()

entries=[]
for disp,pgs in mkindex.res.items():
    if not pgs: continue
    entries.append((key(disp), disp, PASSIM.get(disp) or ranges(pgs)))
entries.sort()

HEAD='<w:pPr><w:pStyle w:val="Heading1"/><w:pageBreakBefore w:val="1"/><w:spacing w:after="120" w:before="480" w:lineRule="auto"/><w:jc w:val="center"/><w:rPr/></w:pPr>'
def heading(t):
    return ('<w:p>'+HEAD+'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>'
            '<w:b w:val="1"/><w:bCs w:val="1"/><w:color w:val="000000"/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rtl w:val="0"/></w:rPr>'
            '<w:t xml:space="preserve">'+t+'</w:t></w:r></w:p>')
NOTEPPR='<w:pPr><w:spacing w:after="240" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/><w:rPr/></w:pPr>'
ENTPPR='<w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/><w:ind w:left="432" w:hanging="432"/><w:jc w:val="left"/><w:rPr/></w:pPr>'

h,pre,ps,tail=dx.split()
new=[heading('Índice onomástico')]
new.append(dx.bodypara([('As páginas remetem ao corpo do texto e às citações em destaque. Ficam fora as listas de referências, o glossário e as notas de rodapé — estas porque remetem, na sua quase totalidade, às mesmas obras arroladas nas listas. Personagens trágicas e figuras religiosas discutidas no argumento aparecem na mesma ordem alfabética dos autores.',False)], NOTEPPR))
for _,disp,pg in entries:
    new.append(dx.bodypara([(disp.replace('&','&amp;')+', '+pg,False)], ENTPPR))
ps.extend(new)
dx.write(h,pre,ps,tail)
print('entradas:',len(entries))
for _,d,p in entries[:6]: print(d,'—',p)
