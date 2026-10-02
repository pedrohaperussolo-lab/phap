# -*- coding: utf-8 -*-
import notas, json, sys
d=json.load(open(sys.argv[1]))
for item in d:
    notas.add_note(item['par'], item['anchor'], [(t,bool(i)) for t,i in item['segs']])
print('renumeradas:', notas.renumber())
