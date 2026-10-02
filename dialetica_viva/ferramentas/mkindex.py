# -*- coding: utf-8 -*-
import json,re,unicodedata
b=json.load(open('bodypages.json'))
NAMES = [
 ("Antígona (personagem)", r"Antígona"),
 ("Astor, James", r"Astor"),
 ("Baillie, J. B.", r"Baillie"),
 ("Braidotti, Rosi", r"Braidotti"),
 ("Brooke, Roger", r"Brooke"),
 ("Brooks, Robin McCoy", r"Brooks"),
 ("Buber, Martin", r"Buber"),
 ("Butler, Judith", r"Butler"),
 ("Carus, Carl Gustav", r"Carus"),
 ("Creonte", r"Creonte"),
 ("Cristo", r"Cristo"),
 ("Deleuze, Gilles", r"Deleuze"),
 ("Drob, Sanford", r"Drob"),
 ("Édipo", r"Édipo"),
 ("Edinger, Edward F.", r"Edinger"),
 ("Espinosa, Benedictus de", r"Espinosa|Spinoza"),
 ("Fordham, Michael", r"Fordham"),
 ("Freeman, John", r"Freeman"),
 ("Freud, Sigmund", r"Freud"),
 ("Giegerich, Wolfgang", r"Giegerich"),
 ("Guattari, Félix", r"Guattari"),
 ("Hegel, G. W. F.", r"Hegel"),
 ("Heidegger, Martin", r"Heidegger"),
 ("Hillman, James", r"Hillman"),
 ("Hull, R. F. C.", r"Hull"),
 ("Hyppolite, Jean", r"Hyppolite"),
 ("Irigaray, Luce", r"Irigaray"),
 ("Jones, Raya", r"Jones"),
 ("Jung, C. G.", r"Jung"),
 ("Kant, Immanuel", r"Kant\b"),
 ("Kelly, Sean M.", r"Kelly"),
 ("Klein, Melanie", r"Klein"),
 ("Kojève, Alexandre", r"Kojève"),
 ("Lacan, Jacques", r"Lacan"),
 ("Malabou, Catherine", r"Malabou"),

 ("Mills, Jon", r"Mills"),
 ("Mogenson, Greg", r"Mogenson"),
 ("Neumann, Erich", r"Neumann"),
 ("Nietzsche, Friedrich", r"Nietzsche"),
 ("Otto, Rudolf", r"Otto\b"),
 ("Pinkard, Terry", r"Pinkard"),
 ("Pippin, Robert B.", r"Pippin"),
 ("Platão", r"Platão"),
 ("Polinices", r"Polinices"),
 ("Samuels, Andrew", r"Samuels"),
 ("Schleiermacher, Friedrich", r"Schleiermacher"),
 ("Schopenhauer, Arthur", r"Schopenhauer"),
 ("Segal, Robert A.", r"Segal"),
 ("Shamdasani, Sonu", r"Shamdasani"),
 ("Silveira, Nise da", r"Nise da Silveira"),
 ("Simondon, Gilbert", r"Simondon"),
 ("Sófocles", r"Sófocles"),
 ("Urban, Elizabeth", r"Urban"),
 ("Whitehead, Alfred North", r"Whitehead"),
 ("Winborn, Mark", r"Winborn"),
 ("Žižek, Slavoj", r"Žižek"),
]

OVERRIDE = {
 "Miller, A. V.": [11],
 "Miller, Jeffrey C.": [73],
 "Miller, David L.": [144],
}
EXTRA = [
 ("Dosse, François", r"Dosse"),
 ("Grosz, Elizabeth", r"Grosz"),
 ("Jardine, Alice", r"Jardine"),
 ("Kerslake, Christian", r"Kerslake"),
 ("Maroni, Amnéris", r"Maroni"),
]
NAMES = NAMES + EXTRA

def norm(t):  # join hyphenated line breaks
    return t.replace('-\n','').replace('\n',' ')
res={}
for disp,pat in NAMES:
    rx=re.compile(pat)
    pgs=[i+1 for i,t in enumerate(b) if 6<=i+1<=249 and rx.search(norm(t))]
    res[disp]=pgs
res.update(OVERRIDE)

if __name__=='__main__':
    for d,p in res.items(): print(f'{len(p):4d}  {d}: {p[:14]}{"..." if len(p)>14 else ""}')
