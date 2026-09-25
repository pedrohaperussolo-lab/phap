# A Dialética Viva — Pedro Perússolo

Pacote de trabalho para continuar a edição do livro no Claude Code.
Estado em 25/09/2026: **250 páginas, 216 notas, 34 verbetes de glossário, 15 listas de referências + bibliografia geral.**

---

## 1. Onde está o livro

**A fonte da verdade é o .docx descompactado em `docx_src/`.** O pipeline Node.js
(`build_parts.js` + `chapters/*.js`) que gerou as versões anteriores **está aposentado**:
o Pedro editou o .docx à mão no Word e essas edições não existem no pipeline. Quem
voltar ao pipeline perde o trabalho dele. Edite sempre o XML em `docx_src/word/`.

```
docx_src/            # o .docx aberto (é isto que se edita)
  word/document.xml  # corpo do texto
  word/footnotes.xml # as 216 notas
  word/styles.xml    # docDefaults: Times New Roman 12pt
entrega/             # o .docx e o .pdf prontos da última build
capa/                # HTML da capa + PDF pronto para o KDP
ferramentas/         # os scripts de edição (ver adiante)
texto_extraido/      # o livro em texto puro, para leitura e busca
avaliacoes/          # a avaliação 94/100 que o Pedro recebeu
```

### Rebuild

```bash
cp -r docx_src /tmp/book/src        # ou ajuste os caminhos nos scripts
bash ferramentas/rebuild.sh         # gera out.docx e out.pdf e imprime o nº de páginas
```

O `rebuild.sh` zipa `docx_src/` em `.docx` e converte com `soffice --headless`.
Confira sempre o número de páginas depois de editar: a lombada da capa depende dele.

### Formato do miolo (KDP 6×9")

- Página 8640×12960 twips, margens 1080 (0,75").
- Corpo: Times New Roman 12pt, entrelinha 360, recuo de primeira linha 720, justificado.
- Notas: Times 10pt, **justificadas, com `after=120` entre elas** (exigência do Pedro).
- Citações recuadas (17 no livro): recuo esquerdo 720, 11pt, entrelinha 320, sem aspas,
  ponto final dentro, chamada de nota ao fim.
- Vinhetas clínicas: recuo 432 dos dois lados, 320 de entrelinha.

---

## 2. As ferramentas

Todas em Python, todas operam no XML preservando os runs (e portanto os itálicos).

| script | para quê |
|---|---|
| `wedit.py` | `Doc(path).replace(old, new, expect=n)` — substitui texto atravessando runs. Falha alto se a contagem não bater. |
| `wclean.py` | limpeza tipográfica (espaço duplo, espaço antes de pontuação, aspas curvas) sem destruir runs |
| `merge_runs.py` | funde runs adjacentes de mesma formatação (o Word fragmenta) |
| `italic.py` | `italicize_in(xml, frase)` — põe uma expressão em itálico dividindo o run |
| `italiza.py` | `aplicar(path, termos)` — itálico em massa, pulando o que já está em itálico e as listas de referências |
| `blockquotes.py` | divide um parágrafo em antes / citação recuada / depois |
| `scan.py` | `scan([termos])` — relatório de quantas ocorrências de cada termo estão em itálico e quantas não |
| `rebuild.sh` | zipa + converte para PDF + conta páginas |

**Cuidado com `wedit.replace`:** ele põe o texto novo no primeiro `<w:t>` atingido e
esvazia os demais. Se o trecho substituído contiver itálicos, eles se perdem — reponha
com `italic.italicize_in` depois. Aconteceu uma vez (nota 155) e foi consertado assim.

---

## 3. O que já foi feito nesta rodada

**Copidesque.** Leitura integral dos 841 parágrafos e das 216 notas.
- Sumário: retirada a linha "Roteiro de estudo" (o Pedro eliminou a seção).
- Fechamento: duas remissões a uma epígrafe que não existe mais.
- Estação 1: "A paciente também quer resolver" → "O analista…" (era ele quem propunha).
- Estação 2: "para me entregar em segredo" (1ª pessoa numa vinheta em 3ª) → "para entregar ao analista".
- *Históriogênese da consciência* → *História da origem da consciência* (Neumann 1949).
- §475 em 3.3: "propriedade universal **da comunidade**" → "**do Estado**" (3.5 já trazia o correto e a nota 43 dá o original de Miller).
- "imediatidade" → "imediaticidade" em duas citações de Hegel (o comentário ao lado afirma ser "a mesma palavra").
- 3.4: a tese forte contradizia a retratação de 3.7 palavra por palavra; a frase foi reescrita para anunciar o exame em vez de concluí-lo.
- Diversos: "pólos"→"polos", "banda e etc.", "passa a se tornar", vírgula em "reconhecer, foi", espaços duplos, aspas curvas.

**APA.** 17 citações recuadas padronizadas; páginas de Mills corrigidas (62 e 64);
nota 155 com locus real de *Less Than Nothing* (cap. 9, seção "From Differentiality to
the Phallic Signifier"); itálico reposto em 13 títulos nas notas; ordem alfabética
conferida nas 15 listas (uma correção, Derrida na Estação 11).

**Itálicos** (última passada). Todos os termos estrangeiros em itálico em 100% das
ocorrências — antes era irregular (*Selbst* 4 em itálico contra 45 em redondo,
*Aufhebung* 13 contra 18, *anima* 10 contra 28). Lista aplicada:
*Aufhebung, aufheben, aufgehoben, Selbst, Geist, Sittlichkeit, Erinnerung, Grenzbegriff,
Bestimmung, Etwas, Zeichen, Symbol, Auseinandersetzung, transitus, esse in anima/intellectu/re,
imago Dei, unus mundus, tertium non datur, coniunctio (oppositorum), in consensu omnium,
quantum, participation mystique, pas-toute, différentiation, différenciation, anima, animus, persona.*
Exceção deliberada: "a libido refluída **anima** imagens" (4.6) é verbo, ficou em redondo.
Termos em português: itálico só onde o texto os apresenta nomeando-os ("o que ele chama
de *diferença psicológica*"), 14 casos.

**Capa.** Tipográfica em bordô (#6E1420, acento #E8B23C), capa completa com contracapa
e lombada de 0,625" (250 × 0,0025). Wrap 12,875 × 9,25 pol; MediaBox forçada em
pikepdf para 927 × 666 pt, porque o Chromium arredonda para pontos inteiros.
**Se o número de páginas mudar, refaça:** ajuste a largura em `capa/wrap.html`
(`@page`, `.wrap` width, e as posições dos painéis) e rode `node capa/shot.js`.

---

## 4. O que ficou pendente

O Pedro aprovou, e ficou por fazer, o seguinte. Em ordem de retorno:

### 4.1 Definir "dialética viva" na Abertura
A expressão aparece **duas vezes no corpo inteiro, ambas na seção 13.6**, na página ~245.
O título nunca é explicado antes disso. Falta um parágrafo na Estação 1 — provavelmente
ao fim de 1.3, antes de "O que se segue, portanto, não é uma introdução comparada" —
dizendo o que torna uma dialética viva, de modo que 13.6 se leia como retorno.
Candidatos de resposta, todos presentes no livro de forma dispersa: a impossibilidade
de estabilização; a tensão que muda de forma sem ser suprimida; o conceito que
permanece aberto à experiência que pretende descrever.

### 4.2 Declaração metodológica na Nota introdutória
Acrescentar ao parágrafo que já enfrenta a objeção da homonímia (é o quinto da Nota,
começa em "Uma objeção previsível a esse método") duas ou três frases recusando
explicitamente a tese de continuidade: não se pretende demonstrar continuidade
histórica nem identidade conceitual entre os autores, e sim pô-los sob tensão em
torno de um problema comum.

### 4.3 Marcadores de nível de afirmação
Diagnóstico medido no texto: o **aparato** está muito bem marcado ("tradução nossa"
106×, "paráfrase nossa" 22×), mas a **interpretação** não: "uma leitura possível"
aparece 0 vezes, "proponho" 1 vez. Faltam cerca de vinte inserções curtas nos pontos
em que o texto passa de reconstrução do autor para consequência própria. Use
`scan.py` para localizar os saltos. Não exagerar: a voz autoral é o que os dois
avaliadores mais elogiaram.

### 4.4 Cortar redundâncias (5–8%)
Alvos: conclusões reafirmadas sem acréscimo; o mesmo contraste explicado duas ou três
vezes (símbolo × *Aufhebung*; negatividade que avança × negatividade que insiste);
transições que só recapitulam. **Não cortar:** as vinhetas clínicas, as concessões a
objeções (Pippin, Pinkard, Malabou, Butler, Jones, Brooks, Shamdasani, Segal, Fordham,
Hallward, Badiou, Jardine, Braidotti, Grosz, Marlan) e a seção 13.1, que é retomada
deliberada.

### 4.5 Sumário dinâmico
O sumário atual não tem paginação. O certo é aplicar estilos de título (`Heading1`/
`Heading2`) aos títulos de Estação e de seção e inserir um campo `TOC` no Word, com
resultado em cache para que o PDF também saia correto. Hoje os títulos são parágrafos
formatados à mão, sem estilo — é preciso criar os estilos em `styles.xml` e marcá-los
em `document.xml`.

### 4.6 Conferência de paginação — **NÃO FOI FEITA**
Este é o item de maior risco editorial. `texto_extraido/inventario_notas.txt` traz as
216 notas, com marca `[PAG]` nas 108 que trazem página ou parágrafo. Fontes primárias
digitalizadas estão em `/root/.claude/uploads/9c828e7c-d516-57c5-a1ec-f39162111021/`
(Irigaray it., Lacan S11 e S20, Deleuze *D&R*, Kojève, Sófocles, Buber, Hillman,
Kerslake, Samuels, Braidotti, Jardine, Grosz, Simondon, Žižek *LTN*). O resto (Hegel,
Jung, Giegerich, Neumann, Edinger, Fordham, Butler, Pippin, Pinkard, Mills) só por web.
**Regra:** três veredictos, *confere* / *não confere* (com o valor certo) / *não
verificável*. Nunca estimar página. Os .txt vêm de OCR e quebram palavras
("ful ly", "control led"), então busque fragmentos curtos e tolere espaços.

### 4.7 Pontas soltas conhecidas
- **Giegerich (2026), *The airtight construction of a neurosis***: o livro existe
  (ISBN 978-1-7388-6068-5), mas **o ano não foi confirmado**. A nota 3 e a lista da
  Estação 1 afirmam 2026.
- **Dez notas** (6, 10, 14–22, 71) localizam Hegel por número de parágrafo "da edição
  em hipertexto do Marxists Internet Archive" — numeração que não existe em edição
  impressa. Trocar pela paginação de Miller ou di Giovanni.
- **Política de citação da Nota introdutória** declara que Hegel e Deleuze são citados
  "a partir das traduções brasileiras, quando disponíveis"; na prática há 26 ocorrências
  de "tradução nossa a partir da versão inglesa", toda a *Ciência da lógica* vem do
  inglês e Deleuze é citado em espanhol duas vezes.
- ***Tipos psicológicos*** é citado sob dois sistemas de numeração de parágrafo
  (§§903/905/906 e §§825/827), sem nota geral que avise.
- **Subtítulo:** a folha de rosto e a capa dizem quatro nomes (Hegel, Jung, Giegerich,
  Deleuze); Lacan entra como Excurso. Se quiser cinco, mude nos dois lugares.

---

## 5. As duas avaliações

Um avaliador cego, que **conferiu citações contra as fontes**, deu **89/100**:
rigor conceitual 88, rigor de citação 87, método/estrutura 84, fluência 92,
aparência de IA 90 (nota alta = pouca), densidade clínica 88, epistemologia 93.
Apontou como defeito mais caro a retratação de 3.7 que continuava a operar como
premissa em 3.4, 8.3, aberturas de 9 e 11 e 13.1 — 3.4 foi corrigida nesta rodada;
as outras quatro **não**, e valem revisão.

Outro leitor, que leu arquitetura e voz sem conferir fontes, deu **94/100**
(`avaliacoes/avaliacao_94.txt`), com a lista de melhorias que gerou os itens 4.1 a 4.4.

Os dois concordam no essencial: a voz autoral e a disciplina de importar a objeção
mais forte contra si são o que o livro tem de melhor, e não devem ser mexidas.
