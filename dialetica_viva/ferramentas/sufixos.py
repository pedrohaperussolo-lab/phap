# -*- coding: utf-8 -*-
import dx, re, unicodedata, collections

RUN = re.compile(r'(<w:r\b.*?<w:t(?: [^>]*)?>)(.*?)(</w:t>.*?</w:r>)', re.S)

def _norm(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9 ]', '', s).strip()

def construir_mapa():
    """Da bibliografia geral: (autor, ano) -> [(titulo_norm, sufixo)] ordenado por título."""
    h, pre, ps, tail = dx.split()
    T = [dx.ptext(p) for p in ps]
    hdr = [i for i, t in enumerate(T) if t.startswith('Referências')]
    ini = hdr[-1]
    grupos = collections.defaultdict(list)
    for i in range(ini + 1, len(ps)):
        if 'w:hanging="720"' not in ps[i]: continue
        m = re.match(r'([A-ZÀ-Ý][^(]{0,60}?)\s*\((\d{4})(?:,[^)]*)?\)\.\s*(.{0,70})', T[i])
        if m:
            grupos[(m.group(1).strip(), m.group(2))].append(_norm(m.group(3))[:60])
    mapa = {}
    for (aut, ano), tits in grupos.items():
        if len(tits) < 2: continue
        for k, t in enumerate(sorted(tits)):
            mapa[(aut, ano, t)] = chr(ord('a') + k)
    return mapa

def _sufixo(mapa, aut, ano, resto):
    """Escolhe o sufixo olhando primeiro o título-contêiner ('In …'), depois o título direto."""
    cand = []
    m = re.search(r'\bIn\s+(.{0,70})', resto)
    if m: cand.append(_norm(m.group(1))[:60])
    cand.append(_norm(resto)[:60])
    for c in cand:
        for (a, y, t), s in mapa.items():
            if a == aut and y == ano and (c.startswith(t) or t.startswith(c[:45])):
                return s
    return None

def aplicar(path, splitter, mapa):
    x = open(path).read()
    partes = re.split(splitter, x)
    log = collections.Counter()
    saida = []
    for b in partes:
        runs = list(RUN.finditer(b))
        txts = [r.group(2) for r in runs]
        novos = list(txts)
        mudou = False
        for i, t in enumerate(txts):
            for m in re.finditer(r'([A-ZÀ-Ý][^(<]{0,60}?)\s*\((\d{4})\)\.\s*$|([A-ZÀ-Ý][^(<]{0,60}?)\s*\((\d{4})\)\.\s', t):
                aut = (m.group(1) or m.group(3) or '').strip().lstrip('em ').lstrip('ver ').strip()
                ano = m.group(2) or m.group(4)
                resto = t[m.end():] + ''.join(txts[i+1:i+5])
                s = _sufixo(mapa, aut, ano, resto)
                if not s: continue
                alvo = '(%s). ' % ano
                if alvo in novos[i]:
                    novos[i] = novos[i].replace(alvo, '(%s%s). ' % (ano, s), 1)
                    txts[i] = novos[i]; mudou = True; log[(aut, ano, s)] += 1
        if mudou:
            nb = b
            for r, nv in reversed(list(zip(runs, novos))):
                nb = nb[:r.start()] + r.group(1) + nv + r.group(3) + nb[r.end():]
            saida.append(nb)
        else:
            saida.append(b)
    open(path, 'w').write(''.join(saida))
    return log
