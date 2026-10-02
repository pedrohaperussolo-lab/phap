# A Dialética Viva — pacote de trabalho

Estado em 02/10/2026 (após a rodada de 4.1, 4.2 e 4.3 parcial). **284 páginas**, ~62.000 palavras, **258 notas de rodapé**,
69 entradas no índice onomástico, 14 vinhetas clínicas. Seções novas: **§10.5** (dois regimes de objetividade) e
**§11.7** (a crítica feminista de dentro da psicologia analítica); as antigas §10.5-10.8 viraram §10.6-10.9 e a antiga
§11.7 virou §11.8.

---

## 1. Como isto funciona

O livro **não** é gerado por script a partir de um fonte em Markdown. Houve um pipeline assim no início
e ele foi **abandonado**, porque não continha as edições feitas à mão por Pedro. O que existe hoje é:

```
src/                     ← o .docx descompactado. ESTA É A FONTE DA VERDADE.
  word/document.xml      ← corpo do livro
  word/footnotes.xml     ← as 258 notas
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
| `novas_secoes.py` | script **já executado** que inseriu §10.5, §11.7, o parágrafo da §13.6, as referências novas e as 25 notas. Fica como registro; **não rodar de novo**. Lição técnica: `notas.add_note` duplica chamadas de nota anteriores se se inserem várias notas no mesmo parágrafo em ordem crescente; insira da última âncora para a primeira |
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

**Atenção:** o intervalo de páginas indexadas está fixado em `mkindex.py` (hoje `6<=i+1<=262`,
porque o glossário começa na p. 263). Se o livro crescer, atualize esse número.

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

Em `/tmp/cover2` (arquivos em `capa/`; a versão corrente é `wrap284.html` / `shot284.js`, spine 284 × 0,0025 = 0,71 pol, largura 12,96 pol; a PDF final tem o `MediaBox` forçado para 933,12 × 666 pt). Edite `wrap.html` e rode:
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
- ✅ **Crítica feminista intrajunguiana** — FEITO (§11.7 e parágrafo novo na §13.6), com ressalvas listadas em 4.1.
- ✅ **Demonstrar uma das três premissas da §10.4** — FEITO (§10.5). A conclusão é que a premissa, como enunciada, é falsa;
  sobrevive uma homologia de estatuto. A §10.4 foi ajustada para apontar para a §10.5. Ver 4.2.

---

## 4. O que falta

### 4.1 Crítica feminista de dentro da psicologia analítica — FEITO (§11.7, §13.6)

**Fontes lidas** (todas no Drive de Pedro): Wehr, *Jung and Feminism* (Beacon, 1987; páginas impressas = página do PDF − 14);
Young-Eisendrath, *Gender and Desire* (Texas A&M, 1997; página lida no cabeçalho corrente); Rowland, *Jung: uma revisão
feminista* (Vozes, 2024; o PDF é reflowed e **não tem paginação impressa**, então as citações vão por capítulo e seção);
Downing (org.), *Espelhos do Self* (Cultrix; só a introdução, sem página). Jung, via Vozes IX/1 §142.

**Resultado da busca**, tal como está no livro: nenhuma das autoras consultadas formula a anima como "o termo a subsumir",
e nenhuma recorre a Hegel. O núcleo da objeção aparece em vocabulário próprio: Wehr pp. 67-68 ("ilusão de equilíbrio") e p. 132
("insistência no modelo da complementaridade sexual"); Young-Eisendrath p. 33 (divisão "complementar", via Jacqueline Rose
lendo Lacan); Rowland (em resumo de Claremont de Castillejo: a mulher como quem "possibilita a individuação masculina pela
encarnação da anima"). Dentro do próprio Jung, IX/1 §142: "a sizígia masculino-feminino é apenas um dos possíveis pares de
opostos". O livro diz que a conexão com a *Aufhebung* é, nas fontes consultadas, original, **com a reserva de busca não exaustiva**.

**O que Pedro precisa conferir ou decidir**
- A frase de Jung citada por Wehr, p. 64 ("Since the anima is an archetype that is found in men…"), foi traduzida a partir
  do inglês de Wehr. A nota de Wehr com a fonte está ilegível no PDF (OCR). Localizar a passagem na OC (provavelmente *Aion*, IX/2)
  e trocar a nota por citação direta com §.
- Rose, via Young-Eisendrath: a referência completa (introdução a *Feminine Sexuality*, Lacan/Mitchell & Rose) está nas notas do
  cap. 2 de Young-Eisendrath, que o texto lido não traz. Completar.
- Goldenberg só entra via Wehr (nota diz isso). Não foram lidos *The Goddess* (Downing, 1981) nem Goldenberg no original.
- Rowland: pôr as páginas da edição impressa da Vozes, se houver exemplar.
- **Junguiana brasileira**: não foi incluída nenhuma. O livro ainda não tem interlocutora nacional na crítica feminista.
- O parágrafo final da §11.7 declara os limites da busca em primeira pessoa ("Goldenberg só é citada aqui através de Wehr, e as
  autoras brasileiras ficaram de fora"). Ajustar ao que Pedro realmente leu.

### 4.2 A premissa da objetividade — FEITO (§10.5; §10.4 ajustada)

Argumento: **a premissa, tal como a §10.4 a enunciava, é falsa**. Deleuze chega à objetividade do problema por via transcendental
("condições da experiência real", DR cap. III p. 150; cap. IV pp. 162-163), Jung por via empírica (OC IX/1 §92) refinada em modelo
(OC VIII/2 §417: "o mesmo que a Física, quando constrói um modelo atômico"; IX/1 §143: "como se" teórico). Sobrevive uma
**homologia de estatuto** (estrutura objetiva indeterminada que só se determina nas respostas: Deleuze p. 163 × Jung IX/1 §142),
que tropeça no terceiro momento da Ideia (Deleuze p. 197: o virtual é "completamente determinado"). A leitura do arquétipo como
problema passa a valer como "como se" teórico sujeito ao "teste do achado que falta" da §13.2.

Páginas de Deleuze: numeração do PDF digital do Drive (a mesma do resto do livro). Páginas conferidas no texto extraído do PDF:
pp. 73, 142, 150, 162, 163, 197. **Não foram lidas**: Kerslake, pp. 94-99 (o PDF de 17 MB não pôde ser baixado; o texto
extraído pelo conector termina antes do cap. 3).

### 4.3 Pendências menores

- ✅ **"A prática da psicoterapia" (XVI/1)**: faixa **1929-1951** conferida no exemplar (Vozes, 2013), pelas notas de
  primeira publicação de cada ensaio (1929 "Problemas da psicoterapia moderna"… 1951 "Questões básicas", *Dialectica*).
  Acrescentada às duas listas de referências. (O prólogo dos editores diz "1939 a 1950", o que não confere com as notas.)
- ⬜ **Irigaray** continua citada pela tradução italiana (OCR com falhas). Nenhum exemplar francês no Drive.
- ⬜ **Maroni, p. 37** e **Dosse, pp. 210-211**: não confirmadas. O Drive só tem outro livro de Maroni (*Vestígios*, 2020), não o
  *Jung: o poeta da alma* (Summus, 1998). Dosse não está no Drive.
- ⬜ **Baillie, §472**: página não confirmada (não há Baillie no Drive).
- ⬜ **Paginação de Deleuze** (digital × impressa): decisão do autor antes de imprimir.
- ⬜ **Epígrafe** "Pluribus probus, pluribus vilis": decisão do autor.

### 4.4 Decisões estruturais que continuam abertas

- Mover **§3.5-3.6** (o dossiê Irigaray, 9 páginas de citação-tradução-glosa) para apêndice.
- A **Estação 9 (Lacan)** é a nota mais baixa das três avaliações (78) e continua rotulada "excurso" enquanto
  carrega peso estrutural em 1.3, 10.3, 12 e 13.1. Ou amplia (as fórmulas da sexuação em notação, um
  comentador lacaniano — Copjec, Fink) ou retira do resto do livro o peso que o rótulo não sustenta.
- As duas linhas que fecham a Estação 1 ("O último a sair que apague as luzes!"). Dois pareceristas as
  apontaram; o autor não decidiu.
