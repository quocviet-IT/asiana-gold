import os, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new):
    global s, n
    if old not in s:
        miss.append(old[:80].replace('\n', ' '))
        return
    s = s.replace(old, new, 1)
    n += 1


# 1. the spec list must describe the size the visitor actually picked
rep('''  const specItems = [
    [t("Mã AG","AG code"), p.ag],
    p.ksc ? [t("Mã nội bộ","Internal reference"), p.ksc] : null,
    [t("Kiểu đan","Construction"), t(p.secVi,p.secEn||p.secVi)],
    p.dia.length ? [t("Đường kính","Gauge"), p.dia.map(mm).join(" · ")+" mm"] : null,
    [t("Tuổi vàng","Purity"), PURITY_LINE],
    [t("Màu vàng","Gold colour"), p.colors.map(c=>t({Y:"Vàng",W:"Trắng",R:"Hồng"}[c],{Y:"Yellow",W:"White",R:"Rose"}[c])).join(" · ")],
    row ? [t("Trọng lượng","Weight"), num(row.c750)+" "+t("chỉ","chỉ")+" · "+num(row.g750)+" g (750)"] : null,
    row ? [t("Chiều dài","Length"), row.length||"—"] : null,
    [t("Sản xuất","Made"), t("Tại xưởng, từ kéo sợi đến đánh bóng","In-house, wire drawing to polish")]
  ].filter(Boolean);''',
    '''  // everything below follows the selected size, not the family the page opened on
  const shownCode = chosen || p.ag;
  const selDia    = gaugeOf(shownCode);
  const diaText   = selDia != null ? mm(selDia)+" mm"
                  : (p.dia.length ? p.dia.map(mm).join(" · ")+" mm" : null);
  const specItems = [
    [t("Mã AG","AG code"), shownCode],
    (row && row.w) ? [t("Mã vàng trắng","White gold code"), row.w] : null,
    p.ksc ? [t("Mã nội bộ","Internal reference"), p.ksc] : null,
    [t("Kiểu đan","Construction"), t(p.secVi,p.secEn||p.secVi)],
    diaText ? [t("Đường kính","Gauge"), diaText] : null,
    [t("Tuổi vàng","Purity"), PURITY_LINE],
    [t("Màu vàng","Gold colour"), p.colors.map(c=>t({Y:"Vàng",W:"Trắng",R:"Hồng"}[c],{Y:"Yellow",W:"White",R:"Rose"}[c])).join(" · ")],
    row ? [t("Trọng lượng","Weight"), num(row.c750)+" "+t("chỉ","chỉ")+" · "+num(row.g750)+" g (750)"] : null,
    row ? [t("Chiều dài","Length"), len(row.length)] : null,
    [t("Sản xuất","Made"), t("Tại xưởng, từ kéo sợi đến đánh bóng","In-house, wire drawing to polish")]
  ].filter(Boolean);''')

# 2. a tidy length formatter, used everywhere a length is printed
rep('const mm  = d => lang==="vi" ? Number(d).toFixed(1).replace(".",",") : Number(d).toFixed(1);',
    'const mm  = d => lang==="vi" ? Number(d).toFixed(1).replace(".",",") : Number(d).toFixed(1);\n'
    'const len = x => String(x||"—").replace(/\\s*cm\\s*$/i," cm").replace(/\\s*-\\s*/,"–").trim();')
rep('<td class="mono" style="font-size:.81rem">${esc(r.length||"—")}</td></tr>`).join("")}</tbody></table></div>`\n    : `<div class="note">',
    '<td class="mono" style="font-size:.81rem">${esc(len(r.length))}</td></tr>`).join("")}</tbody></table></div>`\n    : `<div class="note">')

# 3. the breadcrumb names the size on screen
rep('<span class="mono" style="color:var(--g700)">${esc(p.ag)}</span></div>\n\n    <div class="pdp">',
    '<span class="mono" style="color:var(--g700)">${esc(chosen || p.ag)}</span></div>\n\n    <div class="pdp">')

# 4. the size lives in the address, so a picked size is a shareable link
rep('''  if(view.name === "product")                     path = "/product/" + encodeURIComponent(view.code);''',
    '''  if(view.name === "product")                     path = "/product/" + encodeURIComponent(view.code);''')
rep('''  if(lang === "en") q.set("lang", "en");
  if(view.name === "catalogue"){''',
    '''  if(lang === "en") q.set("lang", "en");
  if(view.name === "product" && pdSize) q.set("size", pdSize);
  if(view.name === "catalogue"){''')
rep('''    view = prod(code) ? {name:"product", code:code} : {name:"catalogue"};''',
    '''    view = prod(code) ? {name:"product", code:code} : {name:"catalogue"};
    const sz = q.get("size");
    if(sz){
      const pr = prod(code);
      if(pr && pr.spec && pr.spec.rows.some(r => r.y === sz)) pdSize = sz;
    }''')

# 5. picking a size updates the address without stacking history
rep('''  const size=e.target.closest("[data-size]");
  if(size){ pdSize=size.dataset.size; render(); return; }''',
    '''  const size=e.target.closest("[data-size]");
  if(size){ pdSize=size.dataset.size; reflow(); return; }''')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('edits %d\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
