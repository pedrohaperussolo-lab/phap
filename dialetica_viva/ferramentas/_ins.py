# -*- coding: utf-8 -*-
import dx, json, sys
PPR='<w:pPr><w:spacing w:line="360" w:lineRule="auto"/><w:ind w:firstLine="720"/><w:jc w:val="both"/><w:rPr/></w:pPr>'
def inserir(idx, paras):
    """paras: lista de listas de [texto, italico]"""
    h,pre,ps,tail=dx.split()
    for k,segs in enumerate(paras):
        ps.insert(idx+k, dx.bodypara([(t,bool(i)) for t,i in segs], PPR))
    dx.write(h,pre,ps,tail)
if __name__=='__main__':
    dados=json.load(open(sys.argv[1]))
    inserir(dados['idx'], dados['paras'])
    h,pre,ps,tail=dx.split()
    for i in range(dados['idx']-1, dados['idx']+len(dados['paras'])+1):
        print(i,'|',dx.ptext(ps[i])[:80])
