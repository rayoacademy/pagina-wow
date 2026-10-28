// pagina-wow · medidor de contraste (WCAG 2.1). Se pega en la consola o se inyecta con el navegador.
// Devuelve los textos visibles que no llegan a 4.5:1 (o 3:1 si son grandes). Los textos sobre foto
// se reportan aparte porque su fondo real depende de la imagen.
(() => {
  document.documentElement.style.setProperty('scroll-behavior', 'auto', 'important');
  const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  const parse = s => {
    const m = (s.match(/[\d.]+(?:e-?\d+)?/g) || []).map(Number);
    if (!m.length) return [0, 0, 0, 0];
    // color(srgb r g b / a) viene en 0..1; rgb()/rgba() en 0..255
    if (/^color\(srgb/.test(s)) return [m[0] * 255, m[1] * 255, m[2] * 255, m[3] ?? 1];
    return m;
  };
  const mezcla = (a, b) => { const al = a[3] ?? 1; return [0, 1, 2].map(i => a[i] * al + b[i] * (1 - al)); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  function fondo(el) {
    const capas = []; let bgEl = null;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage !== 'none' && /url\(/.test(cs.backgroundImage)) return { foto: true };
      // degradado opaco: se toman todos sus colores y se mide contra el peor
      if (/gradient/.test(cs.backgroundImage)) {
        const stops = (cs.backgroundImage.match(/(rgba?|color)\([^)]*\)/g) || []).map(parse).map(c => (c.length === 3 ? [...c, 1] : c));
        if (stops.length && stops.every(c => c[3] >= 0.9)) return { varios: stops };
      }
      const c = parse(cs.backgroundColor); if (c.length === 3) c.push(1);
      if (c[3] > 0) { capas.push(c); if (c[3] >= 1) { bgEl = n; break; } }
    }
    // ¿hay una imagen o video entre el texto y su fondo opaco? Solo se sabe con el texto en pantalla.
    el.scrollIntoView({ block: 'center', behavior: 'instant' });
    const r = el.getBoundingClientRect();
    const pila = document.elementsFromPoint(r.left + Math.min(r.width / 2, 20), r.top + r.height / 2);
    const iFondo = bgEl ? pila.indexOf(bgEl) : pila.length;
    if (pila.some((d, i) => (d.tagName === 'IMG' || d.tagName === 'VIDEO' || d.tagName === 'CANVAS') && i < (iFondo < 0 ? pila.length : iFondo))) return { foto: true };
    let base = [255, 255, 255];
    for (let i = capas.length - 1; i >= 0; i--) base = mezcla(capas[i], base);
    return { color: base };
  }
  const malos = [], foto = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const vistos = new Set();
  while (w.nextNode()) {
    const t = w.currentNode, el = t.parentElement;
    if (!t.textContent.trim() || vistos.has(el)) continue; vistos.add(el);
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    if (el.closest('[aria-hidden="true"]')) continue;
    let tc = parse(cs.color); if (tc.length === 3) tc.push(1);
    if (tc[3] === 0) continue; // texto con degradado (background-clip: text): se revisa a ojo
    const f = fondo(el);
    const txt = t.textContent.trim().slice(0, 50);
    if (f.foto) { foto.push(txt); continue; }
    const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
    const grande = px >= 24 || (px >= 18.66 && bold);
    const min = grande ? 3 : 4.5;
    const rr = Math.min(...(f.varios || [f.color]).map(b => ratio(mezcla(tc, b), b)));
    if (rr < min) malos.push({ txt, ratio: +rr.toFixed(2), min, sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') });
  }
  return { textos: vistos.size, malos, sobre_foto: foto.length };
})()
