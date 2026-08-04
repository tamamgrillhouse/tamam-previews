/* Opa POS — product icons.
   One 64x64 grid, 3px strokes, round caps, drawn as line art with a soft fill layer.
   Everything uses currentColor, so a single icon works on every palette. */

const ICONS = {

souvlaki: `<line x1="9" y1="55" x2="55" y2="9"/>
  <g class="f"><rect x="15" y="30" width="16" height="16" rx="3" transform="rotate(-45 23 38)"/>
  <rect x="24" y="21" width="16" height="16" rx="3" transform="rotate(-45 32 29)"/>
  <rect x="33" y="12" width="16" height="16" rx="3" transform="rotate(-45 41 20)"/></g>
  <rect x="15" y="30" width="16" height="16" rx="3" transform="rotate(-45 23 38)"/>
  <rect x="24" y="21" width="16" height="16" rx="3" transform="rotate(-45 32 29)"/>
  <rect x="33" y="12" width="16" height="16" rx="3" transform="rotate(-45 41 20)"/>`,

kontosouvli: `<line x1="32" y1="5" x2="32" y2="59"/>
  <path class="f" d="M32 13c11 0 17 7 17 19s-6 19-17 19-17-7-17-19 6-19 17-19z"/>
  <path d="M32 13c11 0 17 7 17 19s-6 19-17 19-17-7-17-19 6-19 17-19z"/>
  <path d="M17 26c5 3 25 3 30 0M17 38c5 3 25 3 30 0"/>`,

loukaniko: `<path class="f" d="M44 14a17 17 0 1 0 6 20 8 8 0 1 1-6-20z"/>
  <path d="M44 14a17 17 0 1 0 6 20 8 8 0 1 1-6-20z"/>
  <path d="M44 14l4-5M50 34l6 2"/>`,

kokoretsi: `<line x1="32" y1="5" x2="32" y2="59"/>
  <path class="f" d="M32 14c9 0 15 8 15 18s-6 18-15 18-15-8-15-18 6-18 15-18z"/>
  <path d="M32 14c9 0 15 8 15 18s-6 18-15 18-15-8-15-18 6-18 15-18z"/>
  <path d="M18 24l27 8M18 33l27 8M20 42l24 7"/>`,

brizola: `<path class="f" d="M22 12c14-4 28 4 30 17s-8 24-21 23-22-9-22-20c0-7 5-18 13-20z"/>
  <path d="M22 12c14-4 28 4 30 17s-8 24-21 23-22-9-22-20c0-7 5-18 13-20z"/>
  <circle cx="21" cy="19" r="6"/>
  <path d="M28 34c6-3 12-1 15 4"/>`,

paidakia: `<g class="f"><circle cx="20" cy="20" r="10"/><circle cx="44" cy="20" r="10"/></g>
  <circle cx="20" cy="20" r="10"/><circle cx="44" cy="20" r="10"/>
  <path d="M23 29l10 26M41 29L31 55"/>`,

gyros: `<path class="f" d="M32 6l16 40H16z"/>
  <path d="M32 6l16 40H16z"/>
  <path d="M22 26h20M19 36h26"/>
  <path d="M12 46h40a4 4 0 0 1 0 10H12a4 4 0 0 1 0-10z"/>`,

beer: `<path class="f" d="M16 22h26v30a6 6 0 0 1-6 6H22a6 6 0 0 1-6-6z"/>
  <path d="M16 22h26v30a6 6 0 0 1-6 6H22a6 6 0 0 1-6-6z"/>
  <path d="M42 28h6a7 7 0 0 1 0 14h-6"/>
  <path d="M16 22a6 6 0 0 1 6-6 7 7 0 0 1 10-4 7 7 0 0 1 10 10z"/>
  <path d="M24 32v16M34 32v16"/>`,

krasi: `<path class="f" d="M17 10h30l-3 14a12 12 0 0 1-24 0z"/>
  <path d="M17 10h30l-3 14a12 12 0 0 1-24 0z"/>
  <path d="M32 36v16M22 54h20"/>`,

karafa: `<path d="M26 6h12v10"/>
  <path class="f" d="M38 16l8 12v22a8 8 0 0 1-8 8H26a8 8 0 0 1-8-8V28l8-12z"/>
  <path d="M38 16l8 12v22a8 8 0 0 1-8 8H26a8 8 0 0 1-8-8V28l8-12z"/>
  <path d="M18 36c6 3 22 3 28 0"/>`,

ouzo: `<path class="f" d="M19 18h26l-3 30a6 6 0 0 1-6 5h-8a6 6 0 0 1-6-5z"/>
  <path d="M19 18h26l-3 30a6 6 0 0 1-6 5h-8a6 6 0 0 1-6-5z"/>
  <path d="M21 33c4 3 8-3 11 0s7 3 11 0"/>
  <path d="M28 8v5M36 6v7"/>`,

tsipouro: `<path d="M28 5h8v9"/>
  <path class="f" d="M36 14c0 6 8 8 8 16v20a6 6 0 0 1-6 6H26a6 6 0 0 1-6-6V30c0-8 8-10 8-16z"/>
  <path d="M36 14c0 6 8 8 8 16v20a6 6 0 0 1-6 6H26a6 6 0 0 1-6-6V30c0-8 8-10 8-16z"/>
  <path d="M20 38h24"/>`,

anapsiktiko: `<path class="f" d="M20 14h24v38a6 6 0 0 1-6 6H26a6 6 0 0 1-6-6z"/>
  <path d="M20 14h24v38a6 6 0 0 1-6 6H26a6 6 0 0 1-6-6z"/>
  <path d="M20 14c0-4 24-4 24 0M24 8h10a3 3 0 0 1 0 6"/>
  <path d="M20 26h24"/>`,

nero: `<path d="M27 5h10v7h-10z"/>
  <path class="f" d="M37 12c0 5 7 7 7 15v25a6 6 0 0 1-6 6H26a6 6 0 0 1-6-6V27c0-8 7-10 7-15z"/>
  <path d="M37 12c0 5 7 7 7 15v25a6 6 0 0 1-6 6H26a6 6 0 0 1-6-6V27c0-8 7-10 7-15z"/>
  <path d="M20 34c4 3 8-3 12 0s8 3 12 0"/>`,

kafes: `<path class="f" d="M14 22h30v18a14 14 0 0 1-28 0z"/>
  <path d="M14 22h30v18a14 14 0 0 1-28 0z"/>
  <path d="M44 26h5a7 7 0 0 1 0 14h-5"/>
  <path d="M10 56h40"/>
  <path d="M23 8c-3 4 3 6 0 10M34 8c-3 4 3 6 0 10"/>`,

patates: `<path class="f" d="M17 26h30l-4 28a5 5 0 0 1-5 4H26a5 5 0 0 1-5-4z"/>
  <path d="M17 26h30l-4 28a5 5 0 0 1-5 4H26a5 5 0 0 1-5-4z"/>
  <path d="M17 34h30"/>
  <path d="M24 26V9l6 2M32 26V6l6 3M40 26V12l6 3"/>`,

psomi: `<path class="f" d="M12 30c0-11 9-18 20-18s20 7 20 18v18a4 4 0 0 1-4 4H16a4 4 0 0 1-4-4z"/>
  <path d="M12 30c0-11 9-18 20-18s20 7 20 18v18a4 4 0 0 1-4 4H16a4 4 0 0 1-4-4z"/>
  <path d="M22 20l-4 8M32 18l-4 9M42 20l-4 8"/>`,

tzatziki: `<path class="f" d="M10 30h44c0 14-10 24-22 24S10 44 10 30z"/>
  <path d="M10 30h44c0 14-10 24-22 24S10 44 10 30z"/>
  <path d="M26 30c0-5 4-8 4-12s-5-4-5-8"/>
  <circle cx="38" cy="20" r="5"/>`,

salata: `<path class="f" d="M8 28h48c0 15-11 26-24 26S8 43 8 28z"/>
  <path d="M8 28h48c0 15-11 26-24 26S8 43 8 28z"/>
  <circle cx="22" cy="18" r="7"/>
  <path d="M34 28c0-8 6-13 13-13-1 8-5 12-13 13z"/>
  <path d="M40 22l6-6"/>`,

eisitirio: `<path class="f" d="M8 18h48v10a6 6 0 0 0 0 12v10H8V40a6 6 0 0 0 0-12z"/>
  <path d="M8 18h48v10a6 6 0 0 0 0 12v10H8V40a6 6 0 0 0 0-12z"/>
  <path d="M32 18v4M32 30v4M32 42v4" stroke-dasharray="4 4"/>
  <path d="M16 32h8M16 40h12"/>`
};
