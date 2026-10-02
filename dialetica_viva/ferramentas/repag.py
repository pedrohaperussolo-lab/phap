import pymupdf, re, json
def extrair(pdf='out.pdf'):
    d=pymupdf.open(pdf); body=[]; in_refs=False
    want=['Nota introdutória','1. Abertura','2. Hegel I','3. Hegel II','4. Jung I','5. Jung II','6. O risco',
          '7. Giegerich I','8. Giegerich II','9. Excurso','10. Deleuze I','11. Deleuze II','12. Síntese',
          '13. Fechamento','Glossário','Índice onomástico']
    found={}; last_refs=None
    for pi,p in enumerate(d):
        linhas=[]
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                sz=max(round(s['size'],1) for s in l['spans'])
                t=''.join(s['text'] for s in l['spans']).strip()
                if sz>=13:
                    for w in want:
                        if t.startswith(w) and w not in found: found[w]=pi+1
                    if t=='Referências': last_refs=pi+1
                if sz<11.5 and sz!=11.0: continue
                linhas.append((sz,t))
        keep=[]
        for sz,t in linhas:
            if re.match(r'^Referências( do capítulo)?$', t): in_refs=True; continue
            if in_refs:
                if re.match(r'^(\d+\.\s|\d+\.\d+\s|Glossário|Índice|Nota introdutória)', t) or sz>=13: in_refs=False
                else: continue
            keep.append(t)
        body.append('\n'.join(keep))
    json.dump(body, open('bodypages.json','w'))
    return found, last_refs, len(body)
if __name__=='__main__':
    f,r,n=extrair()
    print('páginas',n,'| refs finais',r)
    print(f)
