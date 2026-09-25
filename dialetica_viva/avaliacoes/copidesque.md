# Copidesque (26/09/2026)

Passada de revisão mecânica sobre `docx_src/word/document.xml` (592
parágrafos de corpo) e `footnotes.xml` (216 notas), usando um script de
varredura por regex (`espaço duplo`, `espaço antes/depois de pontuação`,
`palavra repetida`, `pontuação duplicada`, `parênteses/aspas desbalanceados`,
`espaço sobrando no início/fim de parágrafo`) mais uma checagem de
consistência de itálico para os termos estrangeiros recorrentes (via
`ferramentas/scan.py`). Não foi uma segunda leitura integral de prosa
(reservada para quem for ler o PDF final) — é o que dá para pegar de forma
sistemática e sem risco de alterar sentido.

## Corrigido

**9 aspas de fechamento soltas em citações em bloco** — o padrão de citação
em bloco do livro é sem aspas (a indentação já marca a citação); nove blocos
(parágrafos do corpo em torno das notas de Hegel/Pinkard/Irigaray/Jung)
carregavam uma aspa de fechamento perdida no fim, sem abertura em lugar
nenhum — sobra de quando essas citações provavelmente eram inline. Removida
em todos os 9; a que também estava sem o ponto final (a tradução da citação
de Irigaray) recebeu o ponto.

**8 espaços sobrando no fim de parágrafo + 2 no início** — todos em
parágrafos que terminam em dois-pontos, introduzindo uma citação em bloco na
sequência, ou que começam com "[tradução nossa]." Invisíveis no PDF
renderizado, mas sujeira no XML. Removidos.

**Itálico inconsistente em dois termos**:
- *Aufhebung*: 29 ocorrências em itálico, 2 em redondo (mesmo parágrafo,
  seção sobre Giegerich) — sem nenhuma razão gramatical para a exceção
  (diferente do caso já documentado de "anima" como verbo). Corrigidas para
  itálico.
- *telos*: 1 ocorrência em itálico contra 3 em redondo — a maioria manda,
  corrigida a única em itálico para redondo.
  Conferi também Notion, Bestimmung, Sittlichkeit, Erinnerung, Selbst,
  Begriff, Geist, devir-mulher, participation mystique, imago, unus mundus e
  mais uma dezena de termos — todos já consistentes, sem ação.

## Verificado e descartado (falso positivo)

- 3 "palavras repetidas" (`exige-o o`, `encontra encontra`, `pensa-a a`) —
  todas gramaticalmente corretas em português (clítico + preposição/verbo
  coincidindo na forma), não são erro.
- 7 "pontuação duplicada" no corpo e ~40 nas notas — todas são reticências
  `[...]` ou `...` marcando omissão em citação, convenção correta.
- 1 "minúscula após ponto" no corpo (`vs.`) e ~55 nas notas (`op. cit.`,
  `pp.`, DOIs) — abreviações, não erro de maiúscula.
- Aspas em número ímpar por parágrafo, parênteses desbalanceados: zero
  ocorrências reais depois da correção das 9 aspas soltas acima.
- "a priori" (1 ocorrência, redondo) e "devir-mulher" (25 ocorrências,
  redondo) — sem outra ocorrência para comparar ou já 100% consistentes;
  tratados como escolha de estilo, não mexi.

## Não coberto por esta passada

Concordância verbal, escolhas lexicais, ambiguidade de referência
pronominal e fluência de parágrafo — isso exige leitura corrida, não
varredura por padrão, e não foi refeito aqui (a Estação de cada capítulo já
passou por isso em rodadas anteriores, incluindo a de 4.3/4.4). Se quiser
uma segunda leitura de prosa corrida, é outro trabalho, maior.
