import { EFOOD_INGREDIENT_IDS } from './src/integrations/efood-ingredient-ids.js';
import { STOCK_GROUP_LABELS, stockEntry, isClosableIngredient } from './src/core/ingredients.js';
const keys = Object.keys(EFOOD_INGREDIENT_IDS);
const out = keys.map(k => ({ k, closable: isClosableIngredient(k), g: (stockEntry(k) || {}).group || 'other' }));
console.log(JSON.stringify({ labels: STOCK_GROUP_LABELS, ing: out }));
