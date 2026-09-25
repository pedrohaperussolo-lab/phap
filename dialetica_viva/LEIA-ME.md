# A Dialética Viva — Pedro Perússolo

Pacote de trabalho para continuar a edição do livro no Claude Code.
Estado em 25/09/2026: **251 páginas, 216 notas, 34 verbetes de glossário, 15 listas de referências + bibliografia geral.**
Itens 4.1–4.5 resolvidos nesta rodada (ver §4). Faltam 4.6 (paginação das notas,
precisa das fontes-primárias) e 4.7 (decisões do Pedro).

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

O `rebuild.sh` zipa `docx_src/` em `.docx` e chama `update_fields.py`, que abre o
documento via UNO (`soffice --accept=socket...`), atualiza o campo `TOC` do sumário
(§4.5) e só então exporta o PDF. **Não troque por `soffice --convert-to pdf` direto**:
ele não recalcula campos e o sumário sai com o texto de cache ("Atualize o sumário...").
Confira sempre o número de páginas depois de editar: a lombada da capa depende dele.

Ambiente: precisa do pacote `libreoffice-writer` (só `libreoffice-core` não abre
.docx — dá "Error: source file could not be loaded" em qualquer arquivo, não só
neste) e de `poppler-utils` (`pdfinfo`). `apt-get install libreoffice-writer
poppler-utils` resolve os dois.

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
| `scan.py` | `scan([termos])` — relatório de quantas ocorrências de cada termo estão em itálico e quantas não; `corpo()` devolve `[(idx, texto, spans)]` de cada parágrafo, útil para varrer o livro todo |
| `update_fields.py` | abre o docx via UNO, atualiza o campo `TOC` do sumário e exporta o PDF (chamado pelo `rebuild.sh`) |
| `rebuild.sh` | zipa + atualiza campos + converte para PDF + conta páginas |

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

O Pedro aprovou o seguinte. Em ordem de retorno. **4.1–4.5 resolvidos nesta rodada**,
ficam registrados os detalhes para o caso de precisar revisar a decisão.

### 4.1 Definir "dialética viva" na Abertura — ✅ feito
Parágrafo novo ao fim de 1.3 (antes de "O que se segue, portanto..."), definindo
"dialética viva" pela recusa à estabilização, pela tensão que muda de forma sem ser
suprimida e pelo conceito aberto à experiência, retomando a vinheta clínica de 1.1.
13.6 agora se lê como retorno.

### 4.2 Declaração metodológica na Nota introdutória — ✅ feito
Duas frases acrescentadas ao parágrafo que enfrenta a objeção da homonímia, recusando
explicitamente continuidade histórica ou identidade conceitual entre os quatro autores.

### 4.3 Marcadores de nível de afirmação — ✅ feito
Leitura integral dos 605 parágrafos de corpo. 13 inserções curtas (proponho / sustento
/ a meu ver / arrisco), concentradas nas Estações mais reconstrutivas (2, 4, 5, 6) —
as Estações 3, 9, 12 e 13 já tinham voz autoral bem marcada de rodadas anteriores e
foram deixadas como estavam. Ficou abaixo da estimativa de "~20": não forçar a marcação
onde ela já soava mecânica era mais importante que bater o número.

### 4.4 Cortar redundâncias (5–8%) — ✅ feito, corte conservador
Rodei detecção automática de sentenças quase-duplicadas no corpo inteiro. A maior parte
do que parecia redundância era ou verbete de glossário (fazendo o que devia) ou eco
estrutural deliberado (a "cartografia" da Nota ecoada no fechamento; o fio do feminino
retomado "uma última vez" em 13.5; a citação da "eterna ironia" requotada de propósito
com o contexto que faltava). **Único corte aplicado:** a pergunta que fecha o Cap. 7
("Giegerich não troca uma positividade por outra?") repetida quase palavra por palavra
na abertura do Cap. 8 — pura "transição que só recapitula". Isso não chega a 1%, longe
dos 5–8%; o Pedro decidiu não arriscar a voz autoral só para bater o número. Se quiser
revisitar com um line-edit mais extenso (economia de prosa dentro das frases, não corte
de parágrafos), é outro tipo de tarefa — avisar antes de começar.

### 4.5 Sumário dinâmico — ✅ feito
`Heading1` nas 16 Estações/seções de nível 1 (Nota introdutória, as 13 Estações,
Glossário, Referências) e `Heading2` nas 74 seções numeradas (2.1, 2.2...). O sumário
manual foi trocado por um campo `TOC \o "1-1" \h \z \u` (só nível 1 — o Pedro optou por
não listar as sub-seções nem manter os subtítulos de cada Estação no sumário impresso,
que ficaram só na abertura de cada capítulo). `update_fields.py` (novo, ver §2) resolve
o campo antes de exportar o PDF — **é por isso que o `rebuild.sh` mudou**, veja §1.

### 4.6 Conferência de paginação — **EM ANDAMENTO, ~48/108 conferidas**
Detalhe completo em `avaliacoes/conferencia_citacoes_4.6.md`. Regra: três
veredictos, *confere* / *não confere* (com o valor certo) / *não verificável*.
Nunca estimar página. 17 delas verificadas diretamente contra a fonte
primária nesta sessão (16 + nota 9 de Hegel/Miller, 26/09); ~31 (Irigaray,
Lacan S11/20, Deleuze *Diferença e repetição*, Jardine, Simondon, e a página
exata do Kojève) confirmadas pelo Pedro em 25/09/2026 depois de um episódio
com um arquivo ("versão 8") que alegava essa conferência mas não a continha
— ver a seção "Nota sobre o arquivo versão 8" e "Confirmado pelo Pedro" no
arquivo de detalhe.

**Hegel/Miller, *Science of Logic* (26/09)**: o Pedro subiu um PDF descrito
como a tradução Miller (Prometheus Books, 1991). Confirmei a nota 9 (§62,
conteúdo exato). As notas 13-21 continuam bloqueadas: esse PDF específico
não é uma cópia paginada — é um texto reflowed de só 170 páginas para um
livro de ~800, sem números de página originais, **e com trechos inteiros
faltando de verdade** (confirmei renderizando a página como imagem e rodando
OCR nela — não é bug de extração, o conteúdo não está no arquivo; os
§§135-183, por exemplo, têm só os títulos das Observações, não o corpo).
Ainda precisa de uma cópia com scan de página real (números de página
visíveis) para fechar isso e destravar o item de 4.7. Detalhe em
`avaliacoes/conferencia_citacoes_4.6.md`, seção "Hegel/Miller".

**Técnica que funcionou bem:** buscar o marcador de parágrafo ("§475 [", "748 [")
na fonte, não a frase citada — uma frase pode aparecer antes, como antecipação,
sem ser o trecho citado (me enganou uma vez, na nota 143, corrigido).

**Fontes já obtidas e conferidas** (baixadas via Google Drive do Pedro nesta
sessão, guardadas só no scratchpad — não committar, são obras com direitos
autorais): Hegel *Fenomenologia* (Meneses/Vozes), *O anti-Édipo* (Orlandi/Ed.34,
2010 — a mesma edição citada, 10/10 notas conferidas batendo exato), Hillman
*Anima* (só a edição PT/Cultrix, conteúdo bate mas página não é conferível
contra a inglesa que a nota cita), Giegerich *The airtight construction...*
(confirma o ano 2026, ver 4.7).

**Fontes obtidas mas que não servem:** Žižek *Less Than Nothing* — só achei
uma edição brasileira **condensada** (Boitempo, 8 capítulos), o cap. 9 que as
notas 149 e 155 citam nem existe nela. Precisa da edição inglesa (Verso, 2012).

**Fontes ainda faltando**: Grosz (nota 199), Kerslake (nota 172), Hegel em
**inglês** (Miller — várias notas citam essa paginação especificamente,
di Giovanni não serve, é outra tradução), *Mil Platôs*. Irigaray, Kojève,
Buber, Braidotti, Jardine, Simondon e Deleuze *Diferença e repetição* saíram
desta lista — conferência confirmada pelo Pedro (ver acima).

### 4.7 Pontas soltas conhecidas
- ~~**Giegerich (2026)**~~ — **resolvido**: copyright do PDF ("© 2026 Wolfgang
  Giegerich", ISBN 978-1-7388606-8-5 pbk) confirma o ano. Nada a corrigir.
- ~~**Política de citação da Nota introdutória**~~ — **resolvido**: a Nota agora
  documenta as duas exceções reais à regra "traduções brasileiras, quando
  disponíveis" — a *Ciência da lógica* inteira vem da edição inglesa de Miller
  (36 ocorrências de "tradução nossa a partir da versão inglesa" hoje, não mais
  as 26 do diagnóstico original — cresceu com as inserções de 4.3), e dois
  títulos de Deleuze sem tradução para o português (*Nietzsche y la filosofía*;
  *Spinoza: filosofía práctica*) são citados em espanhol.
- ~~***Tipos psicológicos*** com dois sistemas de numeração~~ — **resolvido**:
  acrescentada a advertência geral na Nota introdutória (verbete "Símbolo" ora
  §§903/905/906 da edição brasileira, ora §§825/827 da edição inglesa de Hull).
- ~~**Subtítulo**~~ — **decidido**: o Pedro confirmou manter os quatro nomes
  (Hegel, Jung, Giegerich, Deleuze); Lacan continua como Excurso. Nenhuma
  mudança necessária na folha de rosto nem na capa.
- **Pendente** — **Dez notas** (6, 10, 14–22, 71) localizam Hegel por número de
  parágrafo "da edição em hipertexto do Marxists Internet Archive" — numeração
  que não existe em edição impressa. Trocar pela paginação de Miller ou di
  Giovanni exige a mesma fonte (Hegel em inglês) que 4.6 — mesmo bloqueio.

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
