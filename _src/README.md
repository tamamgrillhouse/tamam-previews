# _src — πηγή του `eksantlisi-rizikes.html`

Το preview της εξάντλησης **δεν γράφεται στο χέρι**: παράγεται από τα **πραγματικά δεδομένα
του POS**, ώστε να μη διαφωνεί ποτέ με το `defaults.js`.

## Πώς ξαναχτίζεται

Από τον φάκελο του POS (`tamam-pos-v2`):

```
node <εδώ>/dump-menu.mjs > <scratch>/menu.json
node <εδώ>/dump-ing.mjs  > <scratch>/ing.json
python <εδώ>/gen-eksantlisi.py <scratch> <εδώ>/eksantlisi-template.html ../eksantlisi-rizikes.html
```

Τα δύο `dump-*.mjs` **πρέπει να τρέξουν από τη ρίζα του POS** (κάνουν σχετικά import στο `src/`).

## Τι τραβάει

| Από | Τι |
|---|---|
| `src/core/defaults.js` | `createMenu()` (128 προϊόντα / 15 κατηγορίες) · `PROTEIN_GROUPS` (13) · `BREAD_GROUPS` (5) · `POTATO_GROUP` · `LINKED_PAIRS` (15) |
| `src/integrations/efood-ingredient-ids.js` | τα 23 κλειδιά υλικών |
| `src/core/ingredients.js` | ομάδα κάθε υλικού (`stockEntry`) + `isClosableIngredient` |

## Δικλείδα

Ο `gen-eksantlisi.py` ελέγχει ότι **κάθε id κάθε ομάδας υπάρχει στο μενού** και τυπώνει
`ΑΓΝΩΣΤΑ ids σε ομάδες: NONE`. Αν εμφανιστεί λίστα, μια ομάδα δείχνει σε προϊόν που δεν
υπάρχει πια — διόρθωσέ το στο POS, όχι εδώ.
