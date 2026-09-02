import { PROTEIN_GROUPS, BREAD_GROUPS, POTATO_GROUP, LINKED_PAIRS, SAUCE_PRODUCT_LINKS, createMenu } from './src/core/defaults.js';
const menu = createMenu();
const cats = menu.map(c => ({ id: c.id, name: c.name, n: (c.items || []).length }));
const items = [];
for (const c of menu) for (const it of (c.items || [])) items.push({ id: it.id, nm: it.name, cat: c.id, pr: it.price });
console.log(JSON.stringify({ cats, PROTEIN_GROUPS, BREAD_GROUPS, POTATO_GROUP, LINKED_PAIRS, SAUCE_PRODUCT_LINKS, items }));
