# -*- coding: utf-8 -*-
"""Edição de texto em document.xml/footnotes.xml preservando a formatação dos runs."""
import io, re

PARA = re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>|<w:p/>', re.S)
TEL  = re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)

def unesc(s): return s.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'")
def esc(s):   return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

class Doc:
    def __init__(self, path):
        self.path = path
        self.xml = io.open(path, encoding='utf-8').read()
        self.count = 0
    def _paras(self):
        return list(PARA.finditer(self.xml))
    def replace(self, old, new, expect=1, quiet=False):
        """Substitui `old` por `new` no texto corrido dos parágrafos."""
        hits = 0
        out = []; pos = 0
        for pm in self._paras():
            p = pm.group(0)
            els = list(TEL.finditer(p))
            if not els:
                continue
            txt = ''.join(unesc(e.group(1)) for e in els)
            if old not in txt:
                continue
            # mapeia posições
            spans = []; off = 0
            for e in els:
                t = unesc(e.group(1))
                spans.append((off, off+len(t), e)); off += len(t)
            start = 0
            while True:
                i = txt.find(old, start)
                if i < 0: break
                j = i + len(old); hits += 1
                # aplica no primeiro elemento tocado; limpa o resto do intervalo
                newtexts = {}
                first = None
                for (a, b, e) in spans:
                    if b <= i or a >= j: continue
                    t = unesc(e.group(1))
                    lo = max(i, a) - a; hi = min(j, b) - a
                    if first is None:
                        first = e
                        newtexts[e] = t[:lo] + new + t[hi:]
                    else:
                        newtexts[e] = t[:lo] + t[hi:]
                # reconstrói o parágrafo
                buf = []; last = 0
                for e in els:
                    if e in newtexts:
                        buf.append(p[last:e.start()])
                        buf.append('<w:t xml:space="preserve">%s</w:t>' % esc(newtexts[e]))
                        last = e.end()
                buf.append(p[last:])
                p = ''.join(buf)
                els = list(TEL.finditer(p))
                txt = ''.join(unesc(e.group(1)) for e in els)
                spans = []; off = 0
                for e in els:
                    t = unesc(e.group(1)); spans.append((off, off+len(t), e)); off += len(t)
                start = i + len(new)
            out.append(self.xml[pos:pm.start()]); out.append(p); pos = pm.end()
        out.append(self.xml[pos:])
        if hits != expect:
            raise SystemExit("FALHA (%d ocorrências, esperado %d): %s" % (hits, expect, old[:80]))
        self.xml = ''.join(out); self.count += hits
        if not quiet: print("  ok  (%d) %s" % (hits, old[:60].replace('\n',' ')))
    def raw(self, old, new, expect=1):
        c = self.xml.count(old)
        if c != expect: raise SystemExit("FALHA raw (%d/%d): %s" % (c, expect, old[:80]))
        self.xml = self.xml.replace(old, new); print("  ok  raw (%d) %s" % (c, old[:60]))
    def save(self):
        io.open(self.path, 'w', encoding='utf-8').write(self.xml)
        print("gravado:", self.path)
