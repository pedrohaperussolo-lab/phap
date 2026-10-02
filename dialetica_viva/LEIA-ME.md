# A Dialética Viva — pacote de trabalho

Estado em 02/10/2026. **271 páginas**, 970 parágrafos, ~58.900 palavras, **233 notas de rodapé**,
63 entradas no índice onomástico, 14 vinhetas clínicas.

---

## 1. Como isto funciona

O livro **não** é gerado por script a partir de um fonte em Markdown. Houve um pipeline assim no início
e ele foi **abandonado**, porque não continha as edições feitas à mão por Pedro. O que existe hoje é:

```
src/                     ← o .docx descompactado. ESTA É A FONTE DA VERDADE.
  word/document.xml      ← corpo do livro
  word/footnotes.xml     ← as 233 notas
  word/styles.xml        ← docDefaults em Times New Roman
out.docx / out.pdf       ← build corrente
```

**Nunca** regenere o livro a partir de outra coisa. Edite `src/word/*.xml` e reconstrua.

### Build

```bash
bash rebuild.sh     # zipa src/ em out.docx, converte para PDF com soffice, imprime o nº de páginas
```

### Página e margens (KDP 6×9")

`pgSz` 8640×12960 twips; `pgMar` 1080 (0,75") em todos os lados.
Corpo: Times New Roman 12pt (`sz 24`), `line 360`, `firstLine 720`, justificado.
Notas: Times 10pt (`sz 20`), justificado, `after 120`.
Citação em bloco: `ind left=720 firstLine=0`, `sz 22`, `line 320`, **sem aspas**, ponto final dentro.
Vinhetas: `ind left=432 right=432 firstLine=432`, `line 320`, `sz 24`.

---

## 2. As ferramentas (todas em Python 3, na raiz)

| arquivo | o que faz |
|---|---|
| `dx.py` | **o módulo central.** `split()` devolve `(head, pre, ps, tail)` onde `ps` é a lista de parágrafos XML; `write()` grava de volta; `ptext(p)` extrai o texto de um parágrafo; `bodypara(segs, ppr)` e `bibpara(segs)` constroem parágrafos novos a partir de `[(texto, itálico), ...]` |
| `notas.py` | `add_note(par_idx, âncora, segs)` insere uma chamada de nota logo depois da âncora e cria a nota; `renumber()` reatribui os ids 0..N pela ordem do documento e reordena `footnotes.xml`. **Chame `renumber()` sempre depois de inserir notas.** |
| `fnedit.py` | `edit(id_da_nota, [(velho, novo), ...])` — edição cirúrgica dentro de uma nota pelo `w:id` |
| `fnspan.py` | `replace_span(id, texto_inicial, texto_final, repl)` — substitui um trecho que **atravessa vários runs** (necessário quando há itálico no meio) |
| `_ins.py` + JSON | insere parágrafos novos sem inferno de aspas: monte um JSON `{"idx": N, "paras": [[["texto",0],["itálico",1]], ...]}` e rode `python3 _ins.py arquivo.json` |
| `_nt.py` + JSON | idem para notas: `[{"par":N,"anchor":"...","segs":[["texto",0],...]}, ...]` |
| `repag.py` | `extrair()` lê o PDF com PyMuPDF, devolve `(cabeçalhos→página, pág. das referências finais, nº de páginas)` e grava `bodypages.json` com o texto **só do corpo** (exclui notas de 10pt e as listas de referências) |
| `mkindex.py` | define os nomes indexados e calcula as páginas de cada um a partir de `bodypages.json` |
| `buildindex.py` | monta a seção "Índice onomástico" e a acrescenta ao fim do documento. As faixas `passim` são **calculadas**, não digitadas |
| `toc.py` | `entries()` acha os parágrafos do sumário; `setpage(p, n)` troca o número de página |
| `anos.py`, `ordena.py`, `ordena2.py`, `sufixos.py` | passadas de aparato já executadas (anos das edições Vozes, ordenação por autor/ano/título, sufixos a/b/c da APA). Guardados por referência |

### Ciclo completo depois de qualquer edição

```bash
python3 -c "import dx; h,p,ps,t=dx.split(); i=[k for k,q in enumerate(ps) if dx.ptext(q)=='Índice onomástico'][0]; del ps[i:]; dx.write(h,p,ps,t)"
bash rebuild.sh                 # build sem índice
python3 repag.py                # extrai paginação e corpo
python3 buildindex.py           # remonta o índice com as páginas certas
bash rebuild.sh
python3 - <<'EOF'               # repagina o sumário
import repag, dx, toc
f,r,n = repag.extrair()
pages=[f[w] for w in ['Nota introdutória','1. Abertura','2. Hegel I','3. Hegel II','4. Jung I','5. Jung II','6. O risco','7. Giegerich I','8. Giegerich II','9. Excurso','10. Deleuze I','11. Deleuze II','12. Síntese','13. Fechamento','Glossário']]+[r, f['Índice onomástico']]
h,pre,ps,tail,idx = toc.entries()
for i,p in zip(idx,pages): ps[i]=toc.setpage(ps[i],p)
dx.write(h,pre,ps,tail)
EOF
bash rebuild.sh
```

**Atenção:** o intervalo de páginas indexadas está fixado em `mkindex.py` (hoje `6<=i+1<=249`,
porque o glossário começa na p. 250). Se o livro crescer, atualize esse número.

### Verificação obrigatória antes de entregar

```bash
python3 -c "
import re, xml.dom.minidom
d=open('src/word/document.xml').read(); f=open('src/word/footnotes.xml').read()
refs=re.findall(r'footnoteReference[^/>]*w:id=\"(\d+)\"',d); notes=re.findall(r'<w:footnote w:id=\"(-?\d+)\"',f)
assert refs==[str(i) for i in range(len(refs))]==notes, 'notas fora de ordem'
for p in ['src/word/document.xml','src/word/footnotes.xml']: xml.dom.minidom.parse(p)
print('ok:', len(refs), 'notas')"
```

### Capa

Em `/tmp/cover2` (incluída no zip como `cover2/`). Edite `wrap.html` e rode:
lombada = páginas × 0,0025 pol; largura do wrap = 12 + lombada + 0,25 de sangria; altura 9,25 pol; 96 px/pol.
O Chromium arredonda para pontos inteiros, então o `MediaBox` tem de ser forçado com `pikepdf` depois.
O script `shotN.js` + o trecho `pikepdf` em `LEIA-ME` mostram o procedimento. **Refaça a capa a cada mudança de nº de páginas.**

---

## 3. Onde o livro está

Três avaliações cegas independentes, cada uma sobre a versão do momento:

| rodada | média | campo mais baixo |
|---|---|---|
| 1ª | 84,6 | aparato crítico 76 |
| 2ª | 87,3 | Lacan 78 |
| 3ª | 87,7 | Lacan 78, Giegerich 83 |

A 3ª avaliação deu o veredito **"está pronto para publicação"** e estimou o teto em **91 com copidesque**
e **94-96 só com reescrita**, nomeando quatro frentes. Delas:

- ✅ **Giegerich em paridade** — FEITO. A Estação 7 ganhou 3 parágrafos sobre a vida lógica (com o
  esclarecimento, antes ausente, de que "lógico" não é lógica formal), 3 sobre a diferença psicológica
  com a definição literal e as suas quatro formulações, e uma seção nova **§7.5 "O que Giegerich concede"**,
  que reúne as autolimitações do prefácio e desarma três das quatro objeções correntes. A §7.6 reconstrói
  a objeção sobre terreno novo: o pressuposto de Giegerich é declaradamente metodológico e, por isso,
  nada no material pode desmenti-lo — que é exatamente o primeiro dos quatro testes da §13.2 aplicado a ele.
  11 citações diretas novas, todas com página da 5ª ed. (Peter Lang, 2020).
- ✅ **O quinto teste** — FEITO. Seção nova **§13.4 "Por que não há um quinto teste"**: demonstra que ele
  não é formulável no formato dos outros quatro, porque os quatro examinam o uso que o analista faz de um
  conceito e o quinto teria de examinar quanto outra pessoa suporta — saber que a única evidência disponível
  é retrospectiva. No lugar do critério, propõe um dispositivo de três partes (um observador fora do enquadre;
  indicadores lidos como fatos e não como material; regra de reversão decidida antes), e declara o que custa.
- ⬜ **Crítica feminista intrajunguiana** — PENDENTE. Ver abaixo.
- ⬜ **Demonstrar uma das três premissas da §10.4** — PENDENTE. Ver abaixo.

---

## 4. O que falta

### 4.1 Crítica feminista de dentro da psicologia analítica (§11.6 e §13.6)

O livro testa Hegel, Lacan, Giegerich e Deleuze pelo lugar que dão ao feminino, usando Irigaray, Butler,
Jardine, Braidotti e Grosz — todas de fora da psicologia analítica. **Não há uma única interlocutora
junguiana.** Autoras a buscar, em ordem:

1. **Demaris S. Wehr**, *Jung and Feminism: Liberating Archetypes* (Beacon Press, 1987) — a crítica de
   referência: anima/animus como reificação de papéis sociais apresentados como estrutura psíquica.
2. **Susan Rowland**, *Jung: A Feminist Revision* (Polity, 2002) — a recuperação de Jung pelo feminismo.
3. **Polly Young-Eisendrath**, *Gender and Desire: Uncursing Pandora* (1997) — revisão do animus.
4. **Naomi Goldenberg**, "Archetypal Theory after Jung" (*Spring*, 1975) e *Changing of the Gods* (1979) —
   a crítica mais radical: o conceito de arquétipo seria incompatível com o feminismo.
5. **Christine Downing**, *The Goddess* (1981).
6. Alguma junguiana **brasileira** — o livro não tem nenhuma interlocutora nacional, e isso foi apontado.

**A pergunta que mais importa**, e que deve guiar a busca: alguma delas formula a crítica como *"a anima é
o termo a subsumir"* — isto é, o feminino em Jung como complemento de uma totalidade previamente concebida
(o Selbst), ocupando posição estruturalmente análoga à da Aufhebung hegeliana? Se alguma formula, é a
passagem mais importante da pesquisa inteira. Se nenhuma formula, saber isso é igualmente valioso, porque
significa que a conexão é original do livro — e nesse caso convém dizê-lo.

### 4.2 A premissa da objetividade (§10.4)

A §10.4 propõe ler o arquétipo como *problema virtual* no sentido de Deleuze, e declara três premissas
não demonstradas. A segunda é a que o parecerista indicou como a mais rendosa:

> a objetividade reivindicada para o problema em Deleuze e a objetividade reivindicada para o arquétipo em si
> em Jung são do mesmo tipo? Jung chega a ela por via empírica (a recorrência de motivos em material clínico
> e comparativo); Deleuze, por via transcendental (a Ideia como condição dos casos atuais).

É um capítulo novo, não um parágrafo. Fontes já levantadas e verificadas: *Diferença e repetição*, cap. IV,
pp. 162-163 (objetividade do problema), 196-197 (virtual ≠ possível), 197 (diferençação/diferenciação),
200 (não semelhança). Do lado de Jung, os textos naturais são a "Natureza da psique" (Vol. VIII/2) sobre o
arquétipo como possibilidade de representação, e o §155 de "Aspectos psicológicos do arquétipo materno"
(Vol. IX/1), já citado no livro.

### 4.3 Pendências menores já identificadas

- **"A prática da psicoterapia" (Vol. XVI/1)** é a única entrada sem `(Trabalho original...)`. O intervalo
  provável é 1929-1951, mas **não foi verificado** e por isso não foi escrito. Confira no exemplar.
- **Irigaray** é citada 14 vezes pela tradução **italiana** de uma obra francesa, a partir de um scan com
  falhas de OCR declaradas na nota 46. Não há *Speculum* em francês, inglês ou português no Drive. Se o
  original francês aparecer, as 14 notas melhoram de uma vez (o capítulo seria pp. 266-281 na Minuit 1974,
  mas isso vem de uma só fonte não acadêmica e **precisa de conferência**).
- **Maroni, p. 37** e **Dosse, pp. 210-211** não foram confirmadas: nenhum dos dois livros está no Drive e
  os espelhos não entregaram o texto. Alerta: há **duas obras de Maroni de 1998** na literatura ("1998a"/"1998b"),
  e a p. 37 pode ter vindo da outra.
- **Baillie, §472**: a edição está confirmada (2ª ed. rev., 1931, 814 pp.), a **página não**.
- **Paginação de Deleuze**: as páginas citadas vêm do PDF digital que está no Drive, cuja numeração **difere**
  da impressa (Prólogo na p. 8 no digital, p. 13 no impresso da Paz e Terra). É consistente dentro do livro,
  mas convém decidir antes de imprimir.
- **A epígrafe** "Pluribus probus, pluribus vilis" foi corrigida de *probos* para *probus*. A construção é
  dativo de referência com *sum* implícito ("para muitos, honesto; para muitos, vil") e está correta, mas
  um parecerista a questionou — decisão do autor.

### 4.4 Decisões estruturais que continuam abertas

- Mover **§3.5-3.6** (o dossiê Irigaray, 9 páginas de citação-tradução-glosa) para apêndice.
- A **Estação 9 (Lacan)** é a nota mais baixa das três avaliações (78) e continua rotulada "excurso" enquanto
  carrega peso estrutural em 1.3, 10.3, 12 e 13.1. Ou amplia (as fórmulas da sexuação em notação, um
  comentador lacaniano — Copjec, Fink) ou retira do resto do livro o peso que o rótulo não sustenta.
- As duas linhas que fecham a Estação 1 ("O último a sair que apague as luzes!"). Dois pareceristas as
  apontaram; o autor não decidiu.
