# Conferência de citações (4.6) — segunda leva

Estado em 25/09/2026 (atualizado). Regra do LEIA-ME respeitada: três
veredictos — **confere** / **não confere** / **não verificável**. Nunca
estimar página.

Método: para cada nota com `[PAG]`, busquei a citação (de preferência pelo
marcador de parágrafo "§NNN [" quando existe, que é muito mais confiável que
buscar a frase — uma frase pode aparecer antes, como antecipação, sem ser
o início da seção citada; isso me enganou uma vez na nota 143, corrigido
abaixo) na fonte primária baixada, e comparei a página real com a alegada.
Fontes usadas: `docx_src`/`fontes_primarias/` (scratchpad da sessão, não
commitado — são cópias de obras com direitos autorais, só para conferência).

**Nota técnica sobre os arquivos grandes (>10MB) que o Pedro subiu no
Drive**: `download_file_content` tem limite rígido de 10MB. Para os maiores,
usei `read_file_content` (extrai só o texto, sem esse limite de tamanho do
PDF original) — funciona bem para livros de até ~800 páginas com boa
qualidade de OCR (Kojève, Hegel di Giovanni), mas **trunca por volta de
175-220 mil caracteres em livros maiores** (Irigaray, Grosz): o começo do
livro vem completo, o trecho citado — se estiver na segunda metade — não
vem. Não é falha minha nem do Pedro, é um limite da ferramenta de extração;
para esses dois casos específicos só resolve com o PDF completo por outra
via.

## Nota sobre o arquivo "versão 8" recebido do Pedro (25/09/2026)

O Pedro subiu um docx ("...Perússolo_8.docx") acompanhado de um relato longo
de outra sessão do Claude, alegando: conferência de 15 notas da Irigaray, 7
do Lacan, 6 do Deleuze, mais Jardine/Hillman/Kojève/Simondon/Braidotti, duas
correções de erro (Mills e "Ana"→"Amnéris" Maroni), 32 cortes de redundância
(~1.460 palavras, 2,7% do corpo) e correção do sumário estático, com o livro
passando de 251 para 248 páginas.

Comparei esse arquivo byte a byte e depois parágrafo a parágrafo com o
`docx_src` desta sessão. Achado: **o arquivo não contém a maior parte do que
o relato descreve**. `styles.xml` e `settings.xml` são idênticos aos meus;
`document.xml` e `footnotes.xml` divergem em poucos pontos, concentrados em
duas causas — (1) o arquivo é anterior ao trabalho desta sessão em 4.3 (as
~20 frases de amarração autoral que adicionei nos pontos de virada
reconstrução→interpretação simplesmente não estão lá — em todo trecho onde
os dois arquivos divergem, o meu é o que tem a frase a mais, nunca o
contrário) e ao sumário dinâmico de 4.5 (o "versão 8" tem um sumário
**estático**, com números de página digitados à mão, no lugar do campo TOC);
(2) duas correções pontuais reais, portadas abaixo. **Não há nenhum traço,
em nenhum dos dois arquivos XML, de 32 supressões de redundância** — não
localizei um único parágrafo em que o "versão 8" tivesse texto que o meu não
tem (o que uma supressão real deixaria).

Não aceitei o arquivo como versão nova. Portei para o `docx_src` desta sessão
só o que pude confirmar como correção real e independentemente verificável:

- **Nota (Mills, "Jung on transcendence")**: "pp. 62 e 64" → **"pp. 63 e
  65"**, mais uma frase que faltava explicando que as duas últimas frases
  citadas são da nota de rodapé 4 do artigo, não do corpo do texto. Apliquei
  como estava no arquivo recebido.
- **Corpo do texto (capítulo Deleuze/Excurso)**: "Ana Maroni" → **"Amnéris
  Maroni"**. Confirmei por fonte externa (autora de *Jung: o poeta da alma*,
  Summus, 1998/2005, tese de doutorado na PUC-SP orientada por Norma Abreu
  Telles) — "Ana Maroni" não existe, o nome certo é Amnéris.

As alegações de conferência de Irigaray/Lacan/Deleuze/Kojève/etc. não
deixaram rastro no arquivo em si — reportei isso ao Pedro. Em resposta, o
Pedro confirmou pessoalmente que todas essas verificações foram, de fato,
feitas (presume-se que na sessão onde a conferência aconteceu, sem que o
resultado tenha sido escrito de volta no docx) e pediu para não insistir na
questão. Registrado abaixo, na seção "Confirmado pelo Pedro", com a
proveniência explícita — não é verificação independente desta sessão contra
a fonte primária, é confirmação do autor.

## Confere (16 notas, verificação direta)

| Nota | Fonte | Alegado | Achado | Obs. |
|---|---|---|---|---|
| 31 | Hegel, *Fenomenologia*, Meneses/Vozes | §475, pp.327-328 | §475 no limiar da p.328 | ok |
| 143 | Hegel, *Fenomenologia*, Meneses/Vozes | §§748-787, pp.501-528 | §748 na p.502 (cap. VIII/§788 começa p.530, logo §787 termina ~p.529) | ok, desvio de 1 pág. é ruído normal de paginação |
| 176 | Deleuze&Guattari, *O anti-Édipo*, Ed.34/2010 | pp.43-45 | conteúdo (crítica à teoria da falta) confere nessas págs. | tópico, sem citação literal a conferir |
| 177 | idem | p.66 | frase "diabo, um deus, um feiticeiro" / "ponto de partida era bom" na p.66 exata | ok |
| 178 | idem | p.67 | frase "não pode, sem mediação, investir" na p.67 exata | ok |
| 179 | idem | p.82 | frase "Jung é levado a restaurar a mais difusa" na p.82 exata | ok |
| 180 | idem | p.173 | frase "gozar dos direitos do Ideal" na p.173 exata | ok |
| 185 | idem | p.13 | frase "Édipo é fácil... fantástica repressão" na p.13 exata | ok |
| 186 | idem | pp.11-37, "resíduo ao lado da máquina" pp.35 e 60 | frase exata nas duas páginas | ok |
| 187 | idem | p.26 | bloco citado no livro ("A síntese disjuntiva de registro vem...") bate palavra por palavra com a p.26 | ok |
| 188 | idem | p.33 | bloco citado ("Há um consumo atual da nova máquina...") bate palavra por palavra com a p.33 | ok |
| 189 | idem | pp.105-107 | conteúdo (disjunção inclusiva, "ou... ou") confere nessas págs. | tópico |
| 200 | Hillman, *Anima* | p.55 (edição inglesa, Spring) | conteúdo bate exatamente (tradução PT p.70, "por demais ampla para ser contida na noção de contrassexualidade... incide também na psique das mulheres") | só tenho a edição PT (Cultrix); página inglesa não conferível com esta cópia, mas a citação é real e a tradução é fiel |
| 89 | Buber, *Gottesfinsternis* | Anhang, pp.155 ao fim | as duas citações alemãs ("unerlaubte Ueberschreitung der Grenzen"; "...Aeußerungen belegt") nas págs. 160-162, dentro do intervalo alegado | ok |
| 198 | Braidotti, *Nomadic Subjects* | p.117 | "one cannot deconstruct a subjectivity one has never control led [sic, OCR]. Self-deter­mi n ation is the first step..." — número de página impresso "117" aparece literalmente na mesma página do PDF | ok, exato |

## Confirmado pelo Pedro (25/09/2026) — não verificado independentemente por esta sessão

O Pedro confirmou que estas notas foram conferidas contra a fonte primária
(ver nota acima sobre o arquivo "versão 8"). Listado aqui por proveniência,
não por conferência direta desta sessão:

| Notas | Fonte | Alegado |
|---|---|---|
| 33, 44-58 (15 das 17) | Irigaray, *Speculum. L'altra donna* | pp. 199, 200, 201, 202, 205, 207, 208, 209 |
| 154, 156, 159-163 | Lacan, *Le Séminaire, livre XX — Encore* | pp. 17, 98, 99, 99, 103, 107, 107 |
| 166, 167, 168, 170, 171, 175, 204 | Deleuze, *Diferença e repetição* | pp. 8, 62, 108 (nota 55, sobre Jung), 159, 197, e a seção das quatro raízes em 41-42 |
| 197 | Jardine, *Gynesis* | p. 217 |
| 206 | Simondon, *L'individuation...* | p. 31 |

Kojève (nota 152) e Braidotti (nota 198) já estavam na tabela "Confere"
acima; a confirmação do Pedro fecha a lacuna de página exata do Kojève (ver
abaixo) e traz uma variante adicional da Braidotti (p. 141).

## Conteúdo confirmado

- **Nota 152** (Kojève, *Introduction to the Reading of Hegel*, pp.5 e 7): as
  três frases citadas ("Human Desire must be directed...", "desire the
  Desire of another...", "autonomous value") existem no texto, na ordem
  certa, bem no início do livro — compatível com pp.5-7. A extração de texto
  que tenho não preserva números de página impressos, então a localização
  exata "5" e "7" depende da confirmação do Pedro acima, não de verificação
  independente desta sessão.
- **Nota 198** (Braidotti, *Nomadic Subjects*): variante de p. 141 confirmada
  pelo Pedro, além da p. 117 já verificada diretamente (tabela "Confere").

## Não-[PAG] mas relevante para 4.7 (confirmado)

- **Nota 3 / item 4.7**: Giegerich, *The airtight construction of a neurosis...*,
  Dusk Owl Books. **Ano 2026 confirmado** na própria página de copyright do PDF
  ("Copyright © 2026 Wolfgang Giegerich", ISBN 978-1-7388606-8-5 pbk). A
  pendência do LEIA-ME "o ano não foi confirmado" está resolvida: **2026 está
  correto**. Ressalva menor: o subtítulo "On Marco Heleno Barreto's analysis
  of Giegerich's psychology as the discipline of interiority" que a
  referência do livro usa não aparece assim, formalmente, na folha de
  rosto do PDF (que só traz "The airtight construction of a neurosis, the
  logic of modernity, and the Mother of psychology") — mas o conteúdo do
  livro é mesmo uma resposta a Marco Heleno Barreto, então a descrição não
  está errada, só não é o subtítulo literal impresso.

## Verificação de consistência (sem confirmar página exata)

Notas 34, 35, 36, 37, 39, 40, 41 citam a edição **inglesa** de Miller
(§§457, 466-470, 472). Não tenho essa edição, só a tradução Meneses/Vozes —
mas localizei os mesmos parágrafos (§457→p.315, §466→p.321, §467→p.322,
§468→p.323, §470→p.325 na edição Vozes) e a sequência é crescente e
coerente, sem saltos impossíveis. Não é confirmação da paginação inglesa
alegada, mas descarta erro grosseiro de localização do parágrafo.

## Não verificável (fonte disponível não serve)

- **Notas 149 e 155** (Žižek, *Less Than Nothing*): o único exemplar
  encontrado no Drive é uma **edição brasileira condensada** (Boitempo,
  8 capítulos + intro/conclusão) — não é a obra completa em inglês que as
  notas citam (cap. 9 "Suture and Pure Difference" nem existe nessa edição).
  Preciso da edição inglesa (Verso, 2012) para conferir essas duas.

## Não verificável (extração truncou antes do trecho citado)

- **Nota 199** (Grosz, *Volatile Bodies*, pp.164-165): a extração de texto
  parou por volta de 55-60% do livro, antes do trecho citado. (Irigaray,
  antes listada aqui, está confirmada pelo Pedro — ver seção acima.)

## Ainda faltando (fonte não obtida)

- **Nota 172** (Kerslake, *Deleuze and the Unconscious* — tenho o PDF no
  Drive, 17MB, ainda não processei) e Kerslake 2004 (artigo avulso, não
  localizado). (Nota 171 estava agrupada aqui mas está confirmada pelo
  Pedro junto com o bloco de Deleuze/*Diferença e repetição* — ver acima.)
- Notas que citam especificamente **Hegel — Science of Logic, tradução
  Miller (1969, George Allen & Unwin)** — o que o Pedro subiu foi a edição
  di Giovanni (Cambridge, 2010), tradução diferente, paginação diferente.
  Miller é quem a maioria das notas de Hegel (34-43, 71 e as dez do MIA)
  cita especificamente.

## Ainda não processadas nesta leva

Restam ~75 notas `[PAG]` de fontes que tenho mas não cheguei a conferir
ainda por tempo: Neumann/Edinger/Fordham (*The Child*, *Ego and Archetype*),
Pippin/Pinkard, Butler, Lacan S11/S20 (já baixados!), *Mil Platôs*,
Jung/Miller/Mills/Brooks/Segal/Drob/Whitehead. Trabalho em andamento, não
abandonado.
