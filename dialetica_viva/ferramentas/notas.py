# -*- coding: utf-8 -*-
"""Inserir notas de rodapé novas e renumerar tudo pela ordem do documento."""
import dx, re

FN_RPR = '<w:rPr><w:rStyle w:val="FootnoteReference"/><w:vertAlign w:val="superscript"/></w:rPr>'
NOTE_PPR = ('<w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/>'
            '<w:jc w:val="both"/><w:rPr/></w:pPr>')
NOTE_RPR = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" '
            'w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>%s'
            '<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/><w:rtl w:val="0"/></w:rPr>')

def _tmp_id(f):
    usados = [int(x) for x in re.findall(r'<w:footnote w:id="(\d+)"', f)]
    return max(max(usados), 899) + 1

def add_note(para_idx, anchor, segs):
    """Põe uma chamada de nota logo depois de `anchor` no parágrafo, e cria a nota."""
    f = open('src/word/footnotes.xml').read()
    nid = _tmp_id(f)
    corpo = ('<w:r>' + FN_RPR + '<w:footnoteRef/></w:r>'
             + ''.join('<w:r>' + (NOTE_RPR % ('<w:i w:val="1"/><w:iCs w:val="1"/>' if it else ''))
                       + '<w:t xml:space="preserve">' + t + '</w:t></w:r>' for t, it in segs))
    bloco = '<w:footnote w:id="%d"><w:p>%s%s</w:p></w:footnote>' % (nid, NOTE_PPR, corpo)
    f = f.replace('</w:footnotes>', bloco + '</w:footnotes>')
    open('src/word/footnotes.xml', 'w').write(f)

    h, pre, ps, tail = dx.split()
    p = ps[para_idx]
    alvo = None
    for m in re.finditer(r'(<w:r\b.*?<w:t(?: [^>]*)?>)(.*?)(</w:t>.*?</w:r>)', p, re.S):
        if anchor in m.group(2):
            alvo = m; break
    assert alvo, ('âncora não encontrada', para_idx, anchor[:40])
    txt = alvo.group(2); i = txt.index(anchor) + len(anchor)
    ref = ('<w:r>' + FN_RPR + '<w:footnoteReference w:customMarkFollows="0" w:id="%d"/></w:r>' % nid)
    novo = (alvo.group(1) + txt[:i] + alvo.group(3)
            + ref
            + (alvo.group(1) + txt[i:] + alvo.group(3) if txt[i:] else ''))
    ps[para_idx] = p[:alvo.start()] + novo + p[alvo.end():]
    dx.write(h, pre, ps, tail)
    return nid

def renumber():
    """Reatribui ids 0..N pela ordem de aparição no documento e reordena as notas."""
    d = open('src/word/document.xml').read()
    f = open('src/word/footnotes.xml').read()
    ordem = re.findall(r'footnoteReference[^/>]*w:id="(\d+)"', d)
    especiais = [m.group(1) for m in re.finditer(r'<w:footnote w:id="(-?\d+)"[^>]*w:type=', f)]
    mapa = {}
    n = 0
    for antigo in ordem:
        mapa[antigo] = str(n); n += 1
    # renumera no documento
    def sub_doc(m):
        return m.group(0).replace('w:id="%s"' % m.group(1), 'w:id="@@%s@@"' % mapa[m.group(1)])
    d = re.sub(r'footnoteReference[^/>]*w:id="(\d+)"', sub_doc, d)
    d = d.replace('@@', '')
    # separa blocos de nota
    blocos = {}
    cab = f[:f.index('<w:footnote ')]
    fim = '</w:footnotes>'
    for m in re.finditer(r'<w:footnote w:id="(-?\d+)"(.*?)</w:footnote>', f, re.S):
        blocos[m.group(1)] = m.group(0)
    sep = [blocos[k] for k in especiais]
    corpo = []
    for antigo in ordem:
        b = blocos[antigo]
        corpo.append(re.sub(r'^<w:footnote w:id="-?\d+"', '<w:footnote w:id="%s"' % mapa[antigo], b))
    open('src/word/document.xml', 'w').write(d)
    open('src/word/footnotes.xml', 'w').write(cab + ''.join(sep) + ''.join(corpo) + fim)
    return len(ordem)
