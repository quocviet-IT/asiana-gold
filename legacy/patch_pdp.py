import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n = 0


def rep(old, new):
    global s, n
    if old not in s:
        sys.stderr.write('!! MISS: ' + old[:90].replace('\n', ' ') + '\n')
        return
    s = s.replace(old, new, 1)
    n += 1


# ---------------- CSS ----------------
CSS = '''
/* ---------- product detail, editorial layout ---------- */
.pdp{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(28px,4.5vw,64px);align-items:start}
@media(max-width:920px){.pdp{grid-template-columns:1fr}}
.gal{display:grid;grid-template-columns:78px 1fr;gap:14px;align-items:start}
@media(max-width:520px){.gal{grid-template-columns:1fr}}
.gal-thumbs{display:flex;flex-direction:column;gap:10px}
@media(max-width:520px){.gal-thumbs{flex-direction:row;order:2}}
.gal-thumbs button{background:var(--plate);border:1px solid var(--rule);border-radius:8px;
  aspect-ratio:1/1;padding:6px;display:grid;place-items:center;transition:border-color .16s}
.gal-thumbs button img{width:100%;height:100%;object-fit:contain}
.gal-thumbs button[aria-current="true"]{border-color:var(--g500);box-shadow:0 0 0 1px var(--g500)}
.gal-thumbs button:hover{border-color:var(--g400)}
.gal-main{position:relative;background:var(--plate);border:1px solid var(--rule);border-radius:12px;
  aspect-ratio:1/1;display:grid;place-items:center;padding:28px;overflow:hidden;cursor:zoom-in}
.gal-main img{width:100%;height:100%;object-fit:contain;transition:transform .28s}
.gal-main.zoom img{transform:scale(2.3)}
.gal-count{position:absolute;right:14px;bottom:12px;font-family:"Cormorant Garamond",Georgia,serif;
  font-size:.85rem;letter-spacing:.14em;color:var(--plate-ink,#3B2C1A);opacity:.5;pointer-events:none}

.pdp-eyebrow{margin-bottom:14px}
.pdp h1{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;text-transform:uppercase;
  letter-spacing:.03em;font-size:clamp(2rem,3.6vw,3rem);line-height:1.06;margin:0 0 8px}
.pdp .sub{font-style:italic;color:var(--ink-3);font-size:1.05rem}
.pdp hr{border:0;border-top:1px solid var(--rule);margin:22px 0}
.pdp .desc{color:var(--ink-2);font-size:1.02rem;max-width:56ch}
.spec-list{list-style:none;margin:20px 0 0;padding:0;display:flex;flex-direction:column;gap:9px}
.spec-list li{font-size:.98rem;padding-left:16px;position:relative}
.spec-list li::before{content:"";position:absolute;left:0;top:.68em;width:6px;height:1px;background:var(--g400)}
.spec-list b{font-weight:600;color:var(--ink)}
.spec-list span{color:var(--ink-2)}
.pdp-actions{display:flex;gap:11px;flex-wrap:wrap;margin-top:26px}
.back-link{display:inline-flex;align-items:center;gap:8px;margin-top:20px;
  font-family:"Cormorant Garamond",Georgia,serif;font-size:.9rem;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;color:var(--g600)}
.back-link:hover{color:var(--g700)}

/* three points, roman-numbered */
.romans{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(22px,3.5vw,48px)}
@media(max-width:840px){.romans{grid-template-columns:1fr}}
.roman .rn{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.15rem;font-weight:600;
  letter-spacing:.2em;color:var(--g500);display:block;margin-bottom:10px}
.roman h3{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.5rem;font-weight:500;margin-bottom:9px}
.roman p{color:var(--ink-2);font-size:.96rem}

/* related, quiet grid */
.rels{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
@media(max-width:900px){.rels{grid-template-columns:repeat(2,1fr)}}
.rel{text-align:left;display:flex;flex-direction:column;gap:11px}
.rel .plate{background:var(--plate);border:1px solid var(--rule);border-radius:10px;aspect-ratio:1/1;
  display:grid;place-items:center;padding:18px;overflow:hidden;transition:border-color .16s}
.rel:hover .plate{border-color:var(--g400)}
.rel .plate img{width:100%;height:100%;object-fit:contain;transition:transform .3s}
.rel:hover .plate img{transform:scale(1.05)}
.rel b{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.2rem;font-weight:600;line-height:1.2}
.rel span{font-family:"Cormorant Garamond",Georgia,serif;font-size:.82rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-3);font-weight:600}
'''
rep('.hidden{display:none!important}\n</style>', CSS + '.hidden{display:none!important}\n</style>')

# ---------------- productHTML ----------------
old = re.search(r'/\* ================= PRODUCT ================= \*/\nfunction productHTML\(code\)\{.*?\n\}\n', s, re.S)
if not old:
    sys.stderr.write('!! productHTML not found\n')
    sys.exit(1)

NEW = r'''/* ================= PRODUCT ================= */
let pdPhoto = 0;

/* a description assembled from the sheet, never invented */
function blurb(p){
  const g = p.dia.length ? p.dia.map(d=>d.toFixed(1)).join(" · ") + " mm" : null;
  const cols = p.colors.map(c=>t({Y:"vàng",W:"trắng",R:"hồng"}[c],{Y:"yellow",W:"white",R:"rose"}[c])).join(t(", "," / "));
  const kind = p.kind==="bracelet" ? t("Lắc tay","A bracelet") : t("Dây chuyền","A chain");
  const bits = [];
  bits.push(t(
    kind+" "+p.vi.toLowerCase().replace(/^(dây|lắc)\s+/,"")+(g?", đường kính "+g:"")+".",
    (p.en||p.vi)+(g?", "+g+" gauge":"")+"."));
  bits.push(t(
    "Đúc và đan tại xưởng Asiana Gold, làm được ở vàng 750 và 610, màu "+cols+".",
    "Drawn and woven at the Asiana Gold factory in 750 and 610 gold, "+cols+"."));
  if(p.spec){
    const L = p.spec.rows.map(r=>r.length).filter(Boolean);
    const lo = L.length?L[0].split("-")[0]:null, hi = L.length?L[L.length-1].split("-").pop():null;
    bits.push(t(
      "Bảng quy cách có "+p.spec.rows.length+" cỡ tiêu chuẩn"+(lo?", chiều dài "+lo+" đến "+hi:"")+", trọng lượng ghi sẵn cả chỉ lẫn gram.",
      p.spec.rows.length+" standard sizes"+(lo?", lengths "+lo+" to "+hi:"")+", weights listed in both chỉ and grams."));
  } else {
    bits.push(t("Mẫu này báo quy cách theo từng đơn hàng.","Specifications for this model are quoted per order."));
  }
  return bits.join(" ");
}

function productHTML(code){
  const p = prod(code); if(!p) return catalogueHTML();
  const fam = FAMS.find(f=>f.vi===p.secVi) || {};
  const kin = P.filter(x=>x.secVi===p.secVi && x.ag!==p.ag).slice(0,4);
  const spec = p.spec;
  const sizes = spec ? spec.rows.map(r=>r.y) : [];
  if(pdSize && sizes.indexOf(pdSize)<0) pdSize = null;
  const chosen = pdSize || (sizes[0]||null);
  const inRfq = rfq.some(x=>x.ag===p.ag && x.size===chosen);
  const row = spec ? spec.rows.find(r=>r.y===chosen) : null;
  const shots = p.gallery && p.gallery.length ? p.gallery : [p.img];
  if(pdPhoto >= shots.length) pdPhoto = 0;

  const specItems = [
    [t("Mã AG","AG code"), p.ag],
    p.ksc ? [t("Mã nội bộ","Internal reference"), p.ksc] : null,
    [t("Kiểu đan","Construction"), t(p.secVi,p.secEn||p.secVi)],
    p.dia.length ? [t("Đường kính","Gauge"), p.dia.map(d=>d.toFixed(1)).join(" · ")+" mm"] : null,
    [t("Tuổi vàng","Purity"), "750 · 610"],
    [t("Màu vàng","Gold colour"), p.colors.map(c=>t({Y:"Vàng",W:"Trắng",R:"Hồng"}[c],{Y:"Yellow",W:"White",R:"Rose"}[c])).join(" · ")],
    row ? [t("Trọng lượng","Weight"), num(row.c750)+" "+t("chỉ","chỉ")+" · "+num(row.g750)+" g (750)"] : null,
    row ? [t("Chiều dài","Length"), row.length||"—"] : null,
    [t("Sản xuất","Made"), t("Tại xưởng, từ kéo sợi đến đánh bóng","In-house, wire drawing to polish")]
  ].filter(Boolean);

  const romans = [
    ["I", t("Xem đủ mọi góc","See every angle"),
        t("Dùng thư viện ảnh để so sánh từng góc chụp, từ toàn sợi đến vân bề mặt phóng to, mà không rời khỏi trang.",
          "Use the gallery to compare each shot, from the full chain to the magnified weave, without leaving the page.")],
    ["II", t("Đọc được từ mã","Read from the code"),
        t("Mã "+p.ag+" tự nói loại dây, màu vàng và đường kính. Khách sỉ quen mã rồi thì đặt hàng chỉ mất một dòng.",
          "The code "+p.ag+" states chain type, gold colour and gauge on its own. Once a buyer knows it, an order takes one line.")],
    ["III", t("Làm theo mẫu riêng","Made to your pattern"),
        t("Gửi mẫu vật lý hoặc bản vẽ, xưởng dựng khuôn riêng và làm mẫu đầu để duyệt trước khi vào chuyền.",
          "Send a sample or drawing; we cut a bespoke die and run a first-off for approval before the line starts.")]
  ];

  return `<section><div class="wrap">
    <div class="crumb"><button data-nav="home">${t("Trang chủ","Home")}</button> /
      <button data-nav="catalogue">Catalogue</button> /
      <button data-fam="${esc(p.secVi)}">${esc(t(p.secVi,p.secEn||p.secVi))}</button> /
      <span class="mono" style="color:var(--g700)">${esc(p.ag)}</span></div>

    <div class="pdp">
      <div class="gal">
        <div class="gal-thumbs">${shots.map((src,i)=>`
          <button data-photo="${i}" aria-current="${i===pdPhoto}" aria-label="${t("Ảnh","Photo")} ${i+1}">
            <img src="${src}" alt=""></button>`).join("")}</div>
        <div class="gal-main" id="gal-main">
          <img src="${shots[pdPhoto]}" alt="${esc(p.vi)}">
          <span class="gal-count">${pdPhoto+1} / ${shots.length}</span>
        </div>
      </div>

      <div>
        <span class="eyebrow pdp-eyebrow">${esc(t(p.secVi,p.secEn||p.secVi))}</span>
        <h1>${esc(t(p.vi,p.en||p.vi))}</h1>
        <p class="sub">${esc(t(p.en||p.vi,p.vi))}</p>
        <hr>
        <p class="desc">${esc(blurb(p))}</p>
        <ul class="spec-list">${specItems.map(x=>`<li><b>${esc(x[0])}:</b> <span>${esc(x[1])}</span></li>`).join("")}</ul>
        ${sizes.length?`<div style="margin-top:22px">
          <span class="eyebrow" style="margin-bottom:9px">${t("Chọn cỡ","Choose a size")}</span>
          <div class="sizepick">${sizes.map(sz=>`<button data-size="${esc(sz)}" aria-pressed="${sz===chosen}">${esc(sz)}</button>`).join("")}</div>
        </div>`:`<p style="margin-top:18px;color:var(--ink-3);font-size:.92rem">${t("Số lượng tối thiểu theo thoả thuận","Minimum order by agreement")}<span class="ph">${t("cần số liệu","needs figure")}</span></p>`}
        <div class="pdp-actions">
          <button class="btn ${inRfq?"btn-line":"btn-gold"}" data-add="${esc(p.ag)}" data-addsize="${esc(chosen||"")}">
            ${inRfq?t("✓ Đã có trong yêu cầu","✓ In your quote"):t("Thêm vào yêu cầu báo giá","Add to quote request")}</button>
          <a class="btn btn-line" href="https://zalo.me/0909858326" target="_blank" rel="noopener">${t("Hỏi qua Zalo","Ask on Zalo")}</a>
        </div>
        <button class="back-link" data-fam="${esc(p.secVi)}">← ${t("Về dòng","Back to")} ${esc(t(p.secVi,p.secEn||p.secVi))}</button>
      </div>
    </div>
  </div></section>

  ${spec?`<section class="band-tint" style="padding-block:clamp(38px,5vw,64px)"><div class="wrap">
    <div class="sec-head"><div><span class="eyebrow">${t("Bảng quy cách","Size table")}</span>
      <h2 style="font-size:1.9rem">${t("Trọng lượng theo tuổi vàng và chiều dài","Weight by purity and length")}</h2>
      <p>${t("Bấm một dòng để chọn cỡ đó.","Click a row to select that size.")}</p></div></div>
    <div class="tablewrap"><table>
      <thead><tr><th>${t("Mã 18K vàng","18K yellow")}</th><th>${t("18K trắng","18K white")}</th>
        <th class="num">${t("Chỉ 750","Chỉ 750")}</th><th class="num">${t("Gram 750","Gram 750")}</th>
        <th class="num">${t("Chỉ 610","Chỉ 610")}</th><th class="num">${t("Gram 610","Gram 610")}</th>
        <th>${t("Chiều dài","Length")}</th></tr></thead>
      <tbody>${spec.rows.map(r=>`<tr class="pick${r.y===chosen?" on":""}" data-size="${esc(r.y)}">
        <td class="code">${esc(r.y)}</td><td class="code" style="color:var(--ink-3)">${esc(r.w||"—")}</td>
        <td class="num">${num(r.c750)}</td><td class="num">${num(r.g750)}</td>
        <td class="num">${num(r.c610)}</td><td class="num">${num(r.g610)}</td>
        <td class="mono" style="font-size:.81rem">${esc(r.length||"—")}</td></tr>`).join("")}</tbody>
    </table></div>
  </div></section>`:""}

  <section><div class="wrap">
    <div class="romans stagger">${romans.map(r=>`
      <div class="roman"><span class="rn">${r[0]}</span><h3>${r[1]}</h3><p>${r[2]}</p></div>`).join("")}</div>
  </div></section>

  ${kin.length?`<section class="band-tint"><div class="wrap">
    <div class="sec-head"><div><span class="eyebrow">${t("Cùng dòng","Same family")}</span>
      <h2>${t("Mẫu khác trong "+p.secVi.toLowerCase(),"Other models in "+(p.secEn||p.secVi).toLowerCase())}</h2></div>
      <button class="btn btn-line btn-sm" data-fam="${esc(p.secVi)}">${t("Xem cả dòng","See the family")} →</button></div>
    <div class="rels stagger">${kin.map(k=>`
      <button class="rel" data-go="${esc(k.ag)}">
        <span class="plate"><img src="${k.img}" alt="${esc(k.vi)}" loading="lazy"></span>
        <b>${esc(t(k.vi,k.en||k.vi))}</b>
        <span>${esc(k.ag)}</span>
      </button>`).join("")}</div>
  </div></section>`:""}

  <section style="padding-top:0"><div class="wrap" style="text-align:center;padding-block:clamp(34px,5vw,60px)">
    <div class="orn">${LINKMARK}</div>
    <span class="eyebrow" style="margin-top:18px">${t("Khi anh chị sẵn sàng","When you are ready")}</span>
    <h2 style="margin:12px 0 12px">${t("Cần báo giá cho "+p.ag+"?","Need a quote for "+p.ag+"?")}</h2>
    <p class="lede" style="margin-inline:auto;text-align:center">${t(
      "Thêm mã vào yêu cầu rồi gửi kèm số lượng dự kiến, hoặc nhắn thẳng Zalo phòng kinh doanh.",
      "Add the code to your request with an intended volume, or message the sales desk on Zalo.")}</p>
    <div style="display:flex;gap:11px;justify-content:center;flex-wrap:wrap;margin-top:24px">
      <button class="btn btn-gold" data-add="${esc(p.ag)}" data-addsize="${esc(chosen||"")}">${t("Thêm vào yêu cầu","Add to quote")}</button>
      <button class="btn btn-line" data-nav="contact">${t("Liên hệ phòng kinh doanh","Contact the sales desk")}</button>
    </div>
  </div></section>`;
}
'''
s = s[:old.start()] + NEW + s[old.end():]
n += 1

# gallery + zoom wiring replaces the old single-plate zoom
rep('''  const plate=$("#pd-plate");
  if(plate){
    plate.addEventListener("mousemove",e=>{
      const r=plate.getBoundingClientRect();
      const img=plate.querySelector("img");
      img.style.transformOrigin=((e.clientX-r.left)/r.width*100)+"% "+((e.clientY-r.top)/r.height*100)+"%";
    });
    plate.addEventListener("mouseenter",()=>plate.classList.add("zoom"));
    plate.addEventListener("mouseleave",()=>plate.classList.remove("zoom"));
  }''',
'''  const plate=$("#gal-main");
  if(plate){
    plate.addEventListener("mousemove",e=>{
      const r=plate.getBoundingClientRect(), img=plate.querySelector("img");
      img.style.transformOrigin=((e.clientX-r.left)/r.width*100)+"% "+((e.clientY-r.top)/r.height*100)+"%";
    });
    plate.addEventListener("mouseenter",()=>plate.classList.add("zoom"));
    plate.addEventListener("mouseleave",()=>plate.classList.remove("zoom"));
  }''')

# thumbnail clicks
rep('''  const size=e.target.closest("[data-size]");
  if(size){ pdSize=size.dataset.size; render(); return; }''',
'''  const photo=e.target.closest("[data-photo]");
  if(photo){ pdPhoto=+photo.dataset.photo; render(); return; }
  const size=e.target.closest("[data-size]");
  if(size){ pdSize=size.dataset.size; render(); return; }''')

# reset the chosen photo when the product changes
rep('function go(name,extra){ view=Object.assign({name:name},extra||{}); if(name!=="product") pdSize=null; render(); }',
    'function go(name,extra){\n'
    '  if(name!=="product" || (extra&&extra.code!==view.code)){ pdSize=null; pdPhoto=0; }\n'
    '  view=Object.assign({name:name},extra||{}); render();\n}')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('applied %d edits\n' % n)
