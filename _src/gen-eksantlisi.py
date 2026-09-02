# Παράγει το preview εξάντλησης με ΤΑ ΑΛΗΘΙΝΑ δεδομένα του POS.
# Διαβάζει menu.json + ing.json (dumps από defaults.js / ingredients.js) και
# αντικαθιστά το /*__DATA__*/ μέσα στο template.
import json, io, os, sys

SP = sys.argv[1]
TPL = sys.argv[2]
OUT = sys.argv[3]

menu = json.load(io.open(os.path.join(SP, 'menu.json'), encoding='utf-8'))
ingd = json.load(io.open(os.path.join(SP, 'ing.json'), encoding='utf-8'))

EM = {'orek':'🍟','aloifes':'🥫','temaxia':'🍢','pita':'🌯','aravik':'🫓','lavas':'🌮',
      'xxl':'🥙','merida':'🍽','club':'🥪','box':'🥡','burger':'🍔','vegan':'🌱',
      'salates':'🥗','drinks':'🥤','byres':'🍺'}
SUF = [' Πίτα',' Αραβική',' Λαβάς',' XXL',' Μερίδα',' Μερίδες',' Club',' Box',' Burger']

cats = [{'id':c['id'],'lb':c['name'],'em':EM.get(c['id'],'🍽')} for c in menu['cats']]

def disp(nm, cat):
    for s in SUF:
        if nm.endswith(s) and len(nm) > len(s) + 2:
            return nm[:-len(s)]
    return nm

items = []
for it in menu['items']:
    items.append({'id':it['id'],'nm':it['nm'],'dn':disp(it['nm'],it['cat']),
                  'cat':it['cat'],'pr':it['pr']})

prot  = [{'id':g['id'],'lb':g['label'],'ids':g['ids']} for g in menu['PROTEIN_GROUPS']]
bread = [{'id':g['id'],'lb':g['label'],'ic':g.get('icon','🫓'),'ids':g['ids']} for g in menu['BREAD_GROUPS']]
pot   = {'id':menu['POTATO_GROUP']['id'],'lb':menu['POTATO_GROUP']['label'],
         'ic':menu['POTATO_GROUP'].get('icon','🥔'),'ids':menu['POTATO_GROUP']['ids']}

links = {}
for lp in menu['LINKED_PAIRS']:
    links[lp['ingredient']] = {'ids':lp['ids'],'on':bool(lp.get('on'))}

ing = [{'k':x['k'],'g':x['g']} for x in ingd['ing'] if x['closable']]
glabels = ingd['labels']

# ── έλεγχοι ακεραιότητας: κάθε id ομάδας πρέπει να υπάρχει στο μενού ──
known = {i['id'] for i in items}
missing = []
for g in prot:  missing += [(g['id'],i) for i in g['ids'] if i not in known]
for g in bread: missing += [(g['id'],i) for i in g['ids'] if i not in known]
missing += [(pot['id'],i) for i in pot['ids'] if i not in known]
for k,v in links.items(): missing += [(k,i) for i in v['ids'] if i not in known]

data = {'CATS':cats,'P':items,'PROT':prot,'BREAD':bread,'POT':pot,
        'LINKS':links,'ING':ing,'GLB':glabels}

js = 'const D = ' + json.dumps(data, ensure_ascii=False, separators=(',',':')) + ';'
tpl = io.open(TPL, encoding='utf-8').read()
assert tpl.count('/*__DATA__*/') == 1, 'placeholder not found'
io.open(OUT,'w',encoding='utf-8').write(tpl.replace('/*__DATA__*/', js))

print('προϊόντα:', len(items), '| κατηγορίες:', len(cats))
print('οικογένειες κρέατος:', len(prot), '| ομάδες ψωμιού:', len(bread), '| πατάτα:', len(pot['ids']))
print('υλικά:', len(ing), '| υλικά που κλείνουν και πιάτο:', len(links))
print('ΑΓΝΩΣΤΑ ids σε ομάδες:', missing if missing else 'NONE')
print('γράφτηκε:', OUT, os.path.getsize(OUT), 'bytes')
