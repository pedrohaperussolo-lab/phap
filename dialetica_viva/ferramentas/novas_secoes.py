# -*- coding: utf-8 -*-
"""Insere a §10.5 (dois regimes de objetividade), a §11.7 (crítica feminista de dentro),
o parágrafo da §13.6 e as referências novas. Rodar uma vez, a partir da raiz do pacote."""
import dx, notas, re, unicodedata

I = True
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def S(*partes):
    """S('texto', ('itálico',), 'texto') -> [(texto, it)]"""
    out = []
    for p in partes:
        if isinstance(p, tuple): out.append((esc(p[0]), True))
        else: out.append((esc(p), False))
    return out

PPR_BODY = '<w:pPr><w:spacing w:line="360" w:lineRule="auto"/><w:ind w:firstLine="720"/><w:jc w:val="both"/><w:rPr/></w:pPr>'
HEAD_PPR = '<w:pPr><w:pStyle w:val="Heading2"/><w:keepNext w:val="1"/><w:spacing w:after="180" w:before="360" w:lineRule="auto"/><w:jc w:val="left"/><w:rPr/></w:pPr>'
def head(segs):
    rs = ''
    for t, it in segs:
        rs += ('<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>'
               '<w:b w:val="1"/><w:bCs w:val="1"/><w:color w:val="000000"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rtl w:val="0"/>'
               + ('<w:i w:val="1"/><w:iCs w:val="1"/>' if it else '') + '</w:rPr><w:t xml:space="preserve">' + t + '</w:t></w:r>')
    return '<w:p>' + HEAD_PPR + rs + '</w:p>'
def body(segs): return dx.bodypara(segs, PPR_BODY)

def find(ps, prefix, start=0):
    for i in range(start, len(ps)):
        if dx.ptext(ps[i]).startswith(prefix): return i
    raise AssertionError('não achei: ' + prefix)

def renum_heading(p, velho, novo):
    assert ('>' + velho) in p, velho
    return p.replace('>' + velho, '>' + novo, 1)

# --------------------------------------------------------------------------------------
# TEXTO — §10.5
# --------------------------------------------------------------------------------------
H105 = S('10.5 Dois regimes de objetividade')
P105 = [
 S('Das três coisas que a seção anterior declarou por demonstrar, a segunda é a que mais pesa. Se a objetividade que Deleuze reivindica para o problema fosse de outro tipo que a objetividade que Jung reivindica para o arquétipo em si, "campo problemático" e "arquétipo" só poderiam dividir uma palavra, e a leitura proposta seria uma metáfora de que se gostou. Examino aqui a premissa em três passos: o que Deleuze quer dizer quando atribui objetividade ao problema, e por qual via chega a ela; o que Jung quer dizer quando a atribui ao arquétipo, e por qual via; e o que resta da premissa depois do confronto. Adianto o resultado, para que não se espere mais do que ele entrega: tal como foi enunciada, a premissa é falsa. Os dois autores não reivindicam a mesma objetividade. O que sobrevive é uma homologia mais estreita, que basta para o uso que o livro faz dela e não basta para nenhum outro.'),
 S('Comece-se por Deleuze, cuja posição é a menos intuitiva. A objetividade do problema não é a de uma coisa encontrada, nem a de um fato observado: é herdada de Kant e corrigida contra ele. O capítulo IV de ', ('Diferença e repetição',), ' abre lembrando que, para Kant, as Ideias são essencialmente "problemáticas" e que, inversamente, "os problemas são as próprias Ideias".',
   ' Deleuze lê aí que os verdadeiros problemas são Ideias e que estas "não são suprimidas por \'suas\' soluções, pois são a condição indispensável sem a qual nenhuma solução jamais existiria".',
   ' Daí a frase que a §10.4 já citou e que convém agora ler devagar: "Os problemas têm um valor objetivo, as Ideias têm de algum modo um objeto". O que ela afirma não é que o problema exista independentemente do pensamento, como um objeto existiria independentemente de quem o conhece. É que o indeterminado, nele, não mede a nossa ignorância: "não é uma simples imperfeição em nosso conhecimento, nem uma falta no objeto; é uma estrutura objetiva, perfeitamente positiva, agindo já na percepção como horizonte ou foco".',
   ' Objetivo, aqui, quer dizer positivo e estrutural: aquilo que determina os casos sem se confundir com nenhum deles.'),
 S('A via por que Deleuze chega a essa objetividade é transcendental, mas de um transcendental que recusa o formato kantiano. As categorias, diz ele, são condições da experiência possível e, por isso, "muito gerais, muito amplas para o real"; o que se procura são as condições da experiência real. "A condição deve ser condição da experiência real e não da experiência possível. Ela forma uma gênese intrínseca, não um condicionamento extrínseco." A cautela de método que acompanha o programa é igualmente explícita: o empirismo transcendental é, na sua fórmula, "o único meio de não decalcar o transcendental sobre as figuras do empirismo". A estrutura problemática não é, portanto, induzida dos casos, e tampouco postulada contra eles: é exigida por eles, como aquilo sem o que a sua gênese não se explicaria. A objetividade do problema tem a forma de uma exigência de gênese. Dado que há soluções, há de haver o problema que elas resolvem e que nelas persiste.'),
 S('Jung reivindica uma objetividade e a chama de empírica. Acusado com frequência de misticismo, insiste em que o inconsciente coletivo "não é uma questão especulativa nem filosófica, mas sim empírica. A pergunta seria simplesmente saber se tais formas universais existem ou não". A evidência que admite é a recorrência: descartadas a educação e a criptomnésia, "restam casos individuais em número suficiente, mostrando o ressurgimento autóctone de motivos mitológicos que desafiam toda dúvida racional".',
   ' A estrutura do argumento é indutiva. O arquétipo é aquilo que é preciso supor para que os motivos voltem onde nenhuma transmissão os explica; a objetividade reivindicada é a de um fator que precede as imagens e as forma, e a prova de que existe é o que as imagens fazem quando se acumulam.'),
 S('Mas o empirismo de Jung não é ingênuo, e os textos em que ele o refina são os que mais aproximam as duas posições. Em "Considerações teóricas sobre a natureza do psíquico", o arquétipo em si é um "fator psicoide", "irrepresentável", do qual a consciência só recebe "visualizações e concretizações". A operação que o postula é descrita sem rodeios: "Quando a Psicologia admite a existência de certos fatores psicoides irrepresentáveis, com base em suas observações, em princípio ela está fazendo a mesma coisa que a Física, quando constrói um modelo atômico".',
   ' A via é a mesma de antes, a observação, mas o que ela produz já não é um achado: é um modelo, e Jung o diz. Já no ensaio sobre a ', ('anima',), ', de 1936, ele o dizia em termos ainda mais curtos: o empirista "deve contentar-se, portanto, com um \'como se\' teórico".',
   ' E é o mesmo Jung que, ao definir o arquétipo, escreve na linguagem da filosofia crítica: "uma possibilidade dada ', ('a priori',), ' da forma da sua representação".',
   ' O vocabulário oscila entre o empírico e o ', ('a priori',), ', e é difícil ver nessa oscilação um descuido. Ela marca o ponto em que a via de Jung, sem deixar de ser empírica na origem, passa a depender de uma operação que já não é observação.'),
 S('Postos lado a lado, os dois regimes diferem pelo que sustenta a reivindicação e pelo que poderia desmenti-la. Em Jung, o arquétipo é inferido da recorrência e permanece exposto a ela: um motivo que se mostrasse explicável por educação ou criptomnésia perderia o valor probatório, e o próprio Jung nomeia essas hipóteses como as que cumpre descartar. Em Deleuze, o problema é exigido pela gênese e, por isso, não está exposto a casos no mesmo sentido; o que o atingiria não seria um motivo que deixa de recorrer, mas a demonstração de que a gênese das soluções pode dispensar a condição. O teste do achado que falta, que a §13.2 proporá — diga, antes de olhar o material, qual observação o faria abandonar o conceito —, separa os dois regimes sem esforço. Jung sabe responder. Para Deleuze, a pergunta não tem o mesmo sentido, e ele diria que isso não é fraqueza, mas a diferença entre um conceito empírico e uma condição transcendental. A premissa cai, portanto: a objetividade do problema e a do arquétipo em si não são do mesmo tipo, e transpor uma para a outra sem dizê-lo seria passar do empírico ao transcendental por baixo da mesa.'),
 S('O que sobrevive é uma homologia de estatuto, não de fundamento. Nos dois casos, o que se chama de objetivo é uma estrutura ainda não determinada, que só se determina nas suas respostas. Em Deleuze, o primeiro momento da Ideia é o indeterminado como "estrutura objetiva, perfeitamente positiva"; em Jung, "um arquétipo em estado de repouso, não projetado, não possui forma determinável, mas constitui uma estrutura formalmente indefinida, mas com a possibilidade de manifestar-se em formas determinadas, através da projeção".',
   ' Que um e outro escrevam "estrutura" para designar o que não é coisa nem representação não é coincidência verbal. Mas a homologia vale para o primeiro momento da Ideia e tropeça no terceiro: Deleuze insiste em que, "em vez de ser indeterminado, o virtual é completamente determinado",',
   ' em relações diferenciais e pontos singulares, ainda que não em existência atual, ao passo que o arquétipo de Jung, em repouso, nem sequer possui forma determinável. Há aqui uma diferença que a leitura da §10.4 não pode absorver: o problema deleuziano é rico em estrutura antes de qualquer solução, e o arquétipo junguiano, tal como o §142 do ensaio sobre a anima o descreve, só adquire estrutura determinada ao ser projetado.'),
 S('De passagem, e sem pretender com isso demonstrar a terceira premissa, uma observação. Jung escreve, na mesma passagem de 1947, que o arquétipo, ao ser representado, "difere, de maneira que não é possível determinar, daquilo que deu origem a essa representação".',
   ' A frase não afirma a não semelhança de que Deleuze precisa, mas também não afirma a semelhança: afirma uma diferença cuja medida é indeterminável, o que fica a meio caminho entre as duas. Fica registrado, e fica por demonstrar, porque o outro texto de Jung à mão, a analogia do sistema axial do cristal, que "determina apenas a estrutura estereométrica, não porém a forma concreta do cristal particular",',
   ' devolve à relação entre arquétipo e imagem uma semelhança estrutural que a não semelhança deleuziana recusa.'),
 S('A conclusão corrige a §10.4 sem desmanchá-la. O arquétipo não pode ser dito um problema virtual no sentido técnico de Deleuze, porque a objetividade que Jung lhe atribui é de outra espécie, e porque a estrutura que Jung lhe reconhece é menos do que o virtual exige. O que se pode dizer é que o arquétipo, tal como Jung o descreve nos seus textos mais cuidadosos, ocupa na teoria o mesmo lugar que o problema ocupa na de Deleuze: o de uma estrutura objetiva que não é coisa nem representação, que só se determina nas respostas e que persiste nelas. E cada autor fornece ao outro o que lhe falta. Jung fornece a exposição ao material, que o transcendental deleuziano dispensa; Deleuze fornece a explicação da persistência, que a indução de Jung não alcança, porque a recorrência mostra que algo volta, não por que volta como volta. Isto é menos do que a §10.4 podia parecer prometer. É, em compensação, algo que pode ser mantido sob o regime em que Jung dizia sustentar a sua própria teoria. A leitura do arquétipo como problema passa a valer como um "como se" teórico, e fica sujeita, portanto, ao teste do achado que falta: quem a adotar deve poder dizer qual observação clínica o faria abandoná-la.'),
]

def deleuze(resto):
    return S('Deleuze, G. (2006). ', ('Diferença e repetição',), ', ' + resto)
JUNG_CONC = S('Jung, C. G. (2016b). O conceito de inconsciente coletivo. In ', ('Os arquétipos e o inconsciente coletivo',), ' (Obras completas, Vol. IX/1, §92, ambas as citações). Vozes. (Trabalho original publicado em 1936).')
def jung_anima(par):
    return S('Jung, C. G. (2016b). O arquétipo com referência especial ao conceito de ', ('anima',), '. In ', ('Os arquétipos e o inconsciente coletivo',), ' (Obras completas, Vol. IX/1, §%s). Vozes. (Trabalho original publicado em 1936/1954).' % par)
def jung_psiq(par):
    return S('Jung, C. G. (2014b). Considerações teóricas sobre a natureza do psíquico. In ', ('A natureza da psique',), ' (Obras completas, Vol. VIII/2, §%s). Vozes. (Trabalho original publicado em 1947/1954).' % par)
JUNG_MAE = S('Jung, C. G. (2016b). Aspectos psicológicos do arquétipo materno. In ', ('Os arquétipos e o inconsciente coletivo',), ' (Obras completas, Vol. IX/1, §155). Vozes. (Trabalho original publicado em 1938/1954).')

# (índice do parágrafo dentro do bloco, âncora, nota)
NOTAS105 = [
 (1, 'as próprias Ideias".', deleuze('cap. IV, "Síntese ideal da diferença", seção "A Ideia como instância problemática", p. 162.')),
 (1, 'jamais existiria".', deleuze('cap. IV, p. 162. A formulação é a leitura que Deleuze faz de Kant, e é a que ele adota.')),
 (1, 'horizonte ou foco".', deleuze('cap. IV, p. 163, onde se encontram as duas passagens.')),
 (2, 'para o real";', deleuze('cap. I, p. 73.')),
 (2, 'extrínseco."', deleuze('cap. III, seção "Sentido e proposição", p. 150.')),
 (2, 'do empirismo".', deleuze('cap. III, seção "Pensar: sua gênese no pensamento", p. 142.')),
 (3, 'dúvida racional".', JUNG_CONC),
 (4, 'modelo atômico".', jung_psiq('417')),
 (4, 'como se\' teórico".', jung_anima('143')),
 (4, 'da sua representação".', JUNG_MAE),
 (6, 'através da projeção".', jung_anima('142')),
 (6, 'completamente determinado",', deleuze('cap. IV, seção "A realidade do virtual: ens omni modo...", p. 197.')),
 (7, 'a essa representação".', jung_psiq('417')),
 (7, 'cristal particular",', JUNG_MAE),
]

# --------------------------------------------------------------------------------------
# TEXTO — §11.7
# --------------------------------------------------------------------------------------
H117 = S('11.7 A crítica feminista de dentro da psicologia analítica')
P117 = [
 S('As interlocutoras que o livro convocou para testar as dialéticas pelo lugar que dão ao feminino — Irigaray, Butler, Jardine, Braidotti, Grosz — falam todas de fora da psicologia analítica. Seria uma lacuna séria se a tradição junguiana não tivesse produzido, por conta própria, uma crítica da ', ('anima',), ', e mais séria ainda se tivesse produzido uma que antecipasse a objeção que a §11.6 acaba de fazer. A primeira coisa existe, e é considerável. Resta saber se existe a segunda. A pergunta que guia esta seção é precisa: alguma dessas autoras formula a ', ('anima',), ' como o termo a subsumir — o feminino, em Jung, como complemento de uma totalidade previamente concebida, o ', ('Selbst',), ', ocupando posição estruturalmente análoga à que a ', ('Aufhebung',), ' reserva ao feminino em Hegel? Declaro o resultado de saída. Nas obras que consultei, nenhuma a formula nesses termos, e nenhuma recorre a Hegel para fazê-lo. Várias formulam, em vocabulário próprio, o núcleo do que está em jogo: que a complementaridade entre os sexos opera na teoria como pressuposto, e não como achado.'),
 S('A formulação mais próxima é a de Demaris Wehr. Em ', ('Jung and Feminism',), ', ela identifica no centro do paradigma junguiano uma dialética de conflito e resolução que é, a um só tempo, dualista e não dualista, com uma oscilação de Jung entre o dualismo e um ir além do dualismo que "nunca se resolve".',
   ' O diagnóstico toca num ponto que o livro examinou na §6.2: a hesitação entre uma tensão que se sustenta e uma totalidade que a resolve. E é quando Wehr passa da forma à matéria que a objeção se aproxima da §1.3. As ideias de oposição, compensação e equilíbrio, escreve, tornaram-se paradigmas governantes, com os quais Jung e os junguianos "tenderam a minimizar o necessário desequilíbrio entre anima e animus numa cultura que desvaloriza as mulheres".',
   ' E vai além: "construir uma teoria sobre a ilusão de equilíbrio funciona para mascarar o desequilíbrio de gênero que existe no patriarcado".',
   ' Mais adiante, a propósito da primeira projeção infantil, aponta o mesmo princípio em ação: a insistência de Jung no modelo da complementaridade sexual "o leva a errar".'),
 S('A origem desse paradigma já havia sido apontada por Naomi Goldenberg, a quem Wehr reconhece o mérito de ter chamado a atenção para o caráter derivado do animus. A passagem em que Jung o deduz é transparente quanto à lógica: "uma vez que a anima é um arquétipo encontrado nos homens, é razoável supor que um arquétipo equivalente deva estar presente nas mulheres; pois, assim como o homem é compensado por um elemento feminino, a mulher é compensada por um elemento masculino".',
   ' A psique da mulher, nesse raciocínio, é o inverso lógico da do homem, e o animus existe porque a simetria o exige. É a estrutura do termo a subsumir vista pelo avesso: a anima completa o homem, e o animus é postulado para que a simetria da teoria se feche. Polly Young-Eisendrath chega à mesma estrutura por outra porta, que é a do vocabulário lacaniano percorrido na Estação 9. Fazer uma divisão "forte e complementar" entre esses opostos, escreve, "quase elimina a sua utilidade psicológica";',
   ' e cita, para dizer o que se perde, a observação de Jacqueline Rose sobre Lacan: é quando as categorias "masculino" e "feminino" passam a representar "uma divisão absoluta e complementar" — cada sexo vindo a ocupar o lugar "daquilo que poderia satisfazer e completar o outro" — que elas "caem presas de uma mistificação em que a dificuldade da sexualidade desaparece instantaneamente". Ver os dois sexos como "complementos inerentes um do outro", acrescenta Young-Eisendrath, elimina a curiosidade pelos Outros, isto é, pelos aspectos desconhecidos de nós mesmos que supomos existir no sexo oposto.',
   ' Não é por acaso que o argumento chegue a ela por Lacan: a complementaridade de que fala Rose é justamente a que a Estação 9 mostrou desfeita pela inexistência da relação sexual.'),
 S('A defesa de Jung que a tradição oferece é, ela própria, uma resposta de dentro. Susan Rowland, que reconstitui o debate com mais generosidade do que Wehr, lembra que Jung "tem a tendência de colapsar e condensar o gênero e o sexo corporal", mas que não pode ser descrito como "um essencialista de gênero franco, dada a prioridade conferida por ele à pluralidade e androginia do inconsciente".',
   ' O argumento merece ser tomado a sério e, aplicado à questão deste livro, tem dois gumes. De um lado, afrouxa o essencialismo: se os arquétipos são andróginos e plurais, a ', ('anima',), ' não é "o" feminino. De outro, é o impulso compensatório, o mesmo que Wehr acusa, que Rowland invoca como freio: ele "não o permite ser essencialista como ele parece ter desejado ser".',
   ' O que para Wehr é o problema é, para Rowland, a salvaguarda, o que mostra que a disputa não é sobre se a ', ('anima',), ' complementa, e sim sobre se a complementação é a última palavra da teoria. Rowland registra, de passagem, onde a disputa se torna mais aguda: ao resumir a revisão feita por Irene Claremont de Castillejo, nota que ela é "mais conservadora" quando considera as mulheres "aquelas que possibilitam a individuação masculina pela encarnação da anima".',
   ' A frase descreve uma autora, e não uma tese de Rowland, mas é a mais próxima que encontrei da formulação procurada: o feminino como meio de que a totalidade masculina se serve para se completar. É, ainda assim, uma formulação indireta, a respeito de uma interlocutora que a própria Rowland classifica como conservadora, e não uma crítica.'),
 S('A saída mais interessante, porém, não vem das críticas: está no texto de Jung. No ensaio de 1936 sobre a ', ('anima',), ', ele escreve que "a sizígia masculino-feminino é apenas um dos possíveis pares de opostos", que ela tem "muitas relações com outros pares (de opostos) que não apresentam diferenças sexuais" e que "um arquétipo em estado de repouso, não projetado, não possui forma determinável".',
   ' Se isso é tomado a sério, a ', ('anima',), ' como figura feminina é um fenômeno da projeção, e não do arquétipo em si, e a complementaridade entre os sexos deixa de ser a forma da totalidade para ser uma das formas em que ela se dá a ver. É a leitura que Hillman fez de Jung e que a §11.6 já registrou; é também a passagem que a §10.5 usou para aproximar o arquétipo em repouso do virtual de Deleuze. A crítica feminista de dentro não precisa sair de Jung para encontrar o ponto em que a teoria se contradiz: ele está na distância entre o que Jung diz do arquétipo e o que faz da ', ('anima',), '.'),
 S('O resultado da busca pode ser resumido em três pontos. Primeiro: a crítica feminista junguiana confirma, por caminho independente, que a complementaridade funciona na teoria como pressuposto. É o que Wehr chama de ilusão de equilíbrio e Young-Eisendrath de divisão complementar. Segundo: essa crítica é feita em termos de ideologia de gênero e de epistemologia, e não de forma lógica; nenhuma das autoras afirma que a ', ('anima',), ' ocupe, na estrutura da psicologia complexa, o lugar que a ', ('Aufhebung',), ' reserva ao termo a subsumir. Terceiro: a conexão entre a ', ('anima',), ' e a lógica hegeliana da totalidade, tal como a propus na §1.3 e na §11.6, é, nas fontes consultadas, original deste livro, com a reserva de que a busca não foi exaustiva. Goldenberg só é citada aqui através de Wehr, e as autoras brasileiras ficaram de fora. Uma crítica formulada em termos que não procurei pode ter me escapado. O que posso afirmar é o que não encontrei, e onde procurei.'),
]
WEHR = lambda pag, ing, extra='': S('Wehr, D. S. (1987). ', ('Jung and feminism: Liberating archetypes',), '. Beacon Press, ' + pag + ': ' + ing + ' Tradução nossa.' + extra)
YE = lambda pag, ing: S('Young-Eisendrath, P. (1997). ', ('Gender and desire: Uncursing Pandora',), '. Texas A&M University Press, ' + pag + ': ' + ing + ' Tradução nossa.')
NOTAS117 = [
 (1, 'nunca se resolve".', WEHR('pp. 29-30', '"This dialectic is both dualistic and nondualistic. In fact, there is a kind of wavering on Jung\'s part between dualism and a reaching-beyond dualism that is never resolved."')),
 (1, 'desvaloriza as mulheres".', WEHR('p. 67', '"With the ideas of opposition, compensation, and balance as governing paradigms, Jung and Jungians have tended to downplay the necessary imbalance between the anima and animus in a culture that devalues women."')),
 (1, 'existe no patriarcado".', WEHR('p. 68', '"In fact we can go further, and consider that to construct a theory on the illusion of balance functions to mask the gender imbalance that exists in patriarchy." Na mesma página: "to pursue the illusion of balance as the goal of life is to avoid and thereby legitimate the social problem of inequality between the sexes".')),
 (1, 'leva a errar".', WEHR('p. 132', '"Here Jung\'s insistence on the model of sexual complementarity leads him astray."')),
 (2, 'elemento masculino".', WEHR('p. 64', '"Since the anima is an archetype that is found in men, it is reasonable to suppose that an equivalent archetype must be present in women; for just as the man is compensated by a feminine element, so woman is compensated by a masculine one." Wehr transcreve a passagem de Jung e a atribui à leitura de Goldenberg; a nota de Wehr que daria a fonte em Jung não é legível no exemplar digital consultado, e a localização da passagem na Obra completa deve ser conferida. Sobre o caráter derivado do animus, ver ainda Wehr, p. 132: "Naomi Goldenberg\'s critique of the animus as derivative is on target". Os textos de Goldenberg que Wehr arrola (entre eles "Archetypal theory after Jung", Spring, 1975, pp. 199-220, e Changing of the gods, Beacon Press, 1979, cap. 5) não foram consultados diretamente.')),
 (2, 'utilidade psicológica";', YE('p. 33', '"Making a strong and complementary division between these opposites almost eliminates their psychological usefulness."')),
 (2, 'no sexo oposto.', YE('p. 33', 'a passagem de Rose é citada por Young-Eisendrath a partir da introdução de Rose à edição inglesa de Feminine sexuality, de Lacan (a referência completa consta nas notas do capítulo 2 de Young-Eisendrath e deve ser conferida): "Sexuality belongs in this area of instability played out in the register of demand and desire, each sex coming to stand... for that which could satisfy and complete the other. It is when the categories \'male\' and \'female\' are seen to represent an absolute and complementary division that they fall prey to a mystification in which the difficulty of sexuality instantly disappears." E, a seguir: "Seeing the two sexes as inherent complements of each other, with specific roles assigned to each, eliminates our curiosity and interest in, and sometimes even our desire to know about, the Others — those unknown aspects of ourselves that we believe exist in the opposite sex."')),
 (3, 'androginia do inconsciente".', S('Rowland, S. (2024). ', ('Jung: uma revisão feminista',), ' (V. C. H. Richardson, Trad.). Vozes, cap. 2, "Sumário conclusivo". (Trabalho original publicado em 2002). A edição eletrônica consultada não traz a paginação impressa; as passagens de Rowland são, por isso, localizadas por capítulo e seção.')),
 (3, 'ter desejado ser".', S('Rowland, S. (2024). ', ('Jung: uma revisão feminista',), ', cap. 2, seção "Conceitos básicos da psicologia junguiana".')),
 (3, 'pela encarnação da anima".', S('Rowland, S. (2024). ', ('Jung: uma revisão feminista',), ', cap. 3, seção "Extensão e revisão: anima e animus", subseção "Principais autoras".')),
 (4, 'não possui forma determinável".', jung_anima('142')),
]

# --------------------------------------------------------------------------------------
# TEXTO — §13.6 (parágrafo novo)
# --------------------------------------------------------------------------------------
P136 = S('O fio do feminino foi seguido também, na §11.7, no interior da própria psicologia analítica. A busca ali não encontrou quem formulasse a ', ('anima',), ' como o termo a subsumir, mas encontrou, em Wehr e em Young-Eisendrath, o núcleo da objeção em vocabulário próprio — a complementaridade entre os sexos como pressuposto, e não como achado — e, no próprio Jung, a frase que permite sustentá-lo: a sizígia masculino-feminino é apenas um dos possíveis pares de opostos. Se a conexão com a ', ('Aufhebung',), ' é original deste livro, é original com essa reserva, porque repousa numa busca que declarei não exaustiva.')

# --------------------------------------------------------------------------------------
# REFERÊNCIAS
# --------------------------------------------------------------------------------------
R_JUNG2014B = S('Jung, C. G. (2014b). ', ('A natureza da psique',), ' (Obras completas, Vol. VIII/2). Vozes. (Trabalho original publicado em 1947/1954)')
R_JUNG2016B = S('Jung, C. G. (2016b). ', ('Os arquétipos e o inconsciente coletivo',), ' (Obras completas, Vol. IX/1). Vozes. (Trabalhos originais publicados entre 1934 e 1954)')
R_ROWLAND = S('Rowland, S. (2024). ', ('Jung: uma revisão feminista',), ' (V. C. H. Richardson, Trad.). Vozes. (Trabalho original publicado em 2002)')
R_WEHR = S('Wehr, D. S. (1987). ', ('Jung and feminism: Liberating archetypes',), '. Beacon Press.')
R_YE = S('Young-Eisendrath, P. (1997). ', ('Gender and desire: Uncursing Pandora',), '. Texas A&M University Press.')

def sk(t):
    t = t.replace('&amp;', '&')
    return unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode().lower()

def inserir_ref(ps, ini, fim, novo_segs):
    """Insere entrada em ordem alfabética (por texto normalizado) no intervalo [ini, fim) de ps."""
    novo = dx.bibpara(novo_segs)
    k = sk(''.join(t for t, _ in novo_segs))
    for i in range(ini, fim):
        if sk(dx.ptext(ps[i])) > k:
            ps.insert(i, novo); return i
    ps.insert(fim, novo); return fim

# --------------------------------------------------------------------------------------
# EXECUÇÃO
# --------------------------------------------------------------------------------------
def main():
    h, pre, ps, tail = dx.split()

    # --- §13.6: parágrafo novo depois de "O teste, porém, não devolveu..."
    i136 = find(ps, '13.6 O feminino, uma última vez')
    j = find(ps, 'O teste, porém, não devolveu', i136)
    ps.insert(j + 1, body(P136))

    # --- §11.7 -> inserir antes do antigo 11.7; antigo vira 11.8
    i117 = find(ps, '11.7 O que o devir não resolve')
    ps[i117] = renum_heading(ps[i117], '11.7 ', '11.8 ')
    bloco117 = [head(H117)] + [body(p) for p in P117]
    for k, p in enumerate(bloco117): ps.insert(i117 + k, p)
    base117 = i117 + 1   # índice do 1º parágrafo de corpo

    # --- §10.5 -> inserir antes do antigo 10.5; antigos 10.5..10.8 viram 10.6..10.9
    for velho, novo in [('10.8 ', '10.9 '), ('10.7 ', '10.8 '), ('10.6 ', '10.7 '), ('10.5 ', '10.6 ')]:
        i = find(ps, velho)
        ps[i] = renum_heading(ps[i], velho, novo)
    i105 = find(ps, '10.6 Intensidade e energia psíquica')
    bloco105 = [head(H105)] + [body(p) for p in P105]
    for k, p in enumerate(bloco105): ps.insert(i105 + k, p)
    base105 = i105 + 1

    # --- §10.4: ajustar a declaração das três premissas
    i104 = find(ps, 'Dessa convergência, proponho extrair')
    velho = 'Nenhuma das três está demonstrada neste livro.'
    assert ps[i104].count(velho) == 1
    ps[i104] = ps[i104].replace(velho, 'A segunda é examinada na §10.5, que a rejeita na forma em que foi enunciada; as outras duas continuam sem demonstração neste livro.')

    # --- referências
    # capítulo 10
    r10 = find(ps, 'Referências do capítulo', find(ps, '10.9 Uma psicologia sem opostos?'))
    k = find(ps, 'Jung, C. G. (2014a)', r10)
    ps.insert(k + 1, dx.bibpara(R_JUNG2014B)); ps.insert(k + 2, dx.bibpara(R_JUNG2016B))
    # capítulo 11
    r11 = find(ps, 'Referências do capítulo', find(ps, '11.8 O que o devir não resolve'))
    k = find(ps, 'Jardine, A. (1985)', r11)
    ps.insert(k + 1, dx.bibpara(R_JUNG2016B)); ps.insert(k + 2, dx.bibpara(R_ROWLAND))
    ps.insert(k + 3, dx.bibpara(R_WEHR)); ps.insert(k + 4, dx.bibpara(R_YE))
    # lista geral
    g = next(i for i in range(find(ps, '13.7 Por que permanecer aberta'), len(ps)) if dx.ptext(ps[i]).strip() == 'Referências')
    gend = find(ps, 'Índice onomástico', g)
    for segs in (R_ROWLAND, R_WEHR, R_YE):
        gend = find(ps, 'Índice onomástico', g)
        inserir_ref(ps, g + 1, gend, segs)
    # XVI/1: faixa de datas, verificada no exemplar (Vozes, 2013)
    n = 0
    for i, p in enumerate(ps):
        if dx.ptext(p).startswith('Jung, C. G. (2013a). A prática da psicoterapia') and '1929' not in dx.ptext(p):
            assert p.count(' (Obras completas, Vol. XVI/1). Vozes.') == 1
            ps[i] = p.replace(' (Obras completas, Vol. XVI/1). Vozes.', ' (Obras completas, Vol. XVI/1). Vozes. (Trabalhos originais publicados entre 1929 e 1951)'); n += 1
    assert n == 2, n

    dx.write(h, pre, ps, tail)

    # --- notas (depois de gravar; os índices de parágrafo já estão estáveis)
    h, pre, ps, tail = dx.split()
    i105 = find(ps, '10.5 Dois regimes de objetividade'); base105 = i105 + 1
    i117 = find(ps, '11.7 A crítica feminista de dentro da psicologia analítica'); base117 = i117 + 1
    for bloco, base in ((NOTAS105, base105), (NOTAS117, base117)):
        for pi, ancora, segs in reversed(bloco):
            notas.add_note(base + pi, esc_anchor(ancora), segs)
    print('notas:', notas.renumber())

def esc_anchor(a): return a.replace('&', '&amp;')

if __name__ == '__main__':
    main()
