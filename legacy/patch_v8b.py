import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new, count=1):
    global s, n
    if old not in s:
        miss.append(old[:88].replace('\n', ' '))
        return
    s = s.replace(old, new, count)
    n += 1


# ---------------------------------------------------------------- slides
rep('''  {code:"CY30CU",
   eyeVi:"Sáu cỡ · 2,0 đến 8,0 mm", eyeEn:"Six gauges · 2.0 to 8.0 mm",
   hVi:"Đủ cỡ, đủ tuổi vàng,<br><em>đủ chiều dài.</em>", hEn:"Every gauge, purity<br><em>and length.</em>",
   pVi:"Từ 2,0 đến 8,0 mm, vàng 750 và 610, ba màu vàng — trắng — hồng, chiều dài 42 đến 50 cm. Trọng lượng ghi sẵn cả chỉ lẫn gram cho từng cỡ.",
   pEn:"From 2.0 to 8.0 mm, 750 and 610 gold, yellow — white — rose, lengths 42 to 50 cm. Weights listed in both chỉ and grams for every size."},
  {code:"CY25HE",''',
    '''  {code:"CY30CA1",
   eyeVi:"Bốn tuổi vàng · sáu cỡ", eyeEn:"Four purities · six gauges",
   hVi:"Đủ cỡ, đủ tuổi vàng,<br><em>đủ chiều dài.</em>", hEn:"Every gauge, purity<br><em>and length.</em>",
   pVi:"Từ 2,0 đến 8,0 mm, tuổi vàng 750 · 680 · 610 · 416, ba màu vàng — trắng — hồng, chiều dài 42 đến 50 cm.",
   pEn:"From 2.0 to 8.0 mm, in 750 · 680 · 610 · 416 gold, yellow — white — rose, lengths 42 to 50 cm."},
  {code:"CBY3",''')

# ---------------------------------------------------------------- hero art
rep('''        <div class="hero-art">
          <div class="hero-plate"><img src="${p.img}" alt="${esc(p.vi)}"></div>
          <div class="hero-badge"><b>${esc(p.ag)}</b><span>${esc(t(p.vi,p.en||p.vi))}</span></div>
        </div>''',
    '''        <div class="hero-art">
          <img class="hero-cut" src="${(DATA.heroCuts&&DATA.heroCuts[s.code])||p.img}" alt="${esc(p.vi)}">
          <div class="hero-tag"><b>${esc(p.ag)}</b><span>${esc(t(p.vi,p.en||p.vi))}</span></div>
        </div>''')

# ---------------------------------------------------------------- rail -> numbers
rep('''  <div class="wrap rail"><div class="inner">
    <div><b>${P.length}</b><span>${t("mẫu trong catalogue","models in catalogue")}</span></div>
    <div><b>${FAMS.length}</b><span>${t("dòng sản phẩm","product families")}</span></div>
    <div><b>${mm(2)}–${mm(8)} mm</b><span>${t("đường kính","gauge range")}</span></div>
    <div><b>750 · 610</b><span>${t("tuổi vàng","gold purity")}</span></div>
    <div><b>42–50 cm</b><span>${t("chiều dài chuẩn","standard lengths")}</span></div>
  </div></div>''',
    '''  <div class="wrap numbers"><div class="card-in">
    <div class="head">
      <span class="eyebrow">${t("Asiana Gold bằng con số","Asiana Gold by the numbers")}</span>
      <h2>${t("Một catalogue đã chuẩn hoá đến từng cỡ","A catalogue standardised down to the gauge")}</h2>
      <p>${t("Không phải album ảnh. Mỗi mẫu có mã đọc được, mỗi cỡ có trọng lượng ghi sẵn theo cả chỉ lẫn gram.","Not a photo album. Every model carries a readable code, and every size carries a weight in both chỉ and grams.")}</p>
    </div>
    <div class="ngrid">
      ${[[P.length, t("mẫu trong catalogue","models in catalogue")],
         [FAMS.length, t("dòng sản phẩm","product families")],
         [SPECS.length, t("nhóm quy cách","spec groups")],
         [SPECS.reduce((a,g)=>a+g.rows.length,0), t("dòng size chuẩn","standard size rows")],
         [DIAS.length, t("cỡ đường kính","gauge sizes")],
         [PURITIES.length, t("tuổi vàng","gold purities")]]
        .map(x=>`<div class="ncell"><b data-count="${x[0]}">${x[0]}</b><span>${x[1]}</span></div>`).join("")}
    </div>
    <div class="pending">
      <span>${t("Bốn con số còn chờ bộ phận sản phẩm cấp:","Four figures still awaiting the product team:")}</span>
      <ul>${[t("Năng lực / tháng","Monthly output"),t("MOQ","MOQ"),
             t("Thời gian sản xuất","Lead time"),t("Thị trường xuất khẩu","Export markets")]
            .map(x=>`<li>${x}</li>`).join("")}</ul>
    </div>
  </div></div>''')

# ---------------------------------------------------------------- feats -> who we work for
old_feats = re.search(r'  <section class="band-tint"><div class="wrap">\n    <div class="sec-head center">\n      <span class="eyebrow">\$\{t\("Vì sao chọn Asiana Gold".*?</div></section>\n', s, re.S)
if not old_feats:
    miss.append('feats section')
else:
    NEW = '''  <section class="band-tint"><div class="wrap who">
    <div>
      <span class="eyebrow">${t("Chúng tôi làm cho ai","Who we work for")}</span>
      <h2 style="margin:12px 0 16px">${t("Asiana Gold chỉ làm hàng sỉ<br><em>và hàng gia công.</em>","Asiana Gold works wholesale<br><em>and contract only.</em>")}</h2>
      <p class="lede">${t(
        "Không bán lẻ từng sợi. Khách của xưởng là những nơi mua theo lô, đọc bảng quy cách trước khi hỏi giá, và cần cùng một mẫu giao đi giao lại giống hệt nhau.",
        "We do not sell single pieces. Our customers buy by the batch, read the spec sheet before asking a price, and need the same model to arrive identical every time.")}</p>
      <div class="clients">${[t("Tiệm vàng","Jewellers"),t("Nhà nhập khẩu","Importers"),
        t("Thương hiệu trang sức","Jewellery brands"),t("Chuỗi bán lẻ","Retail chains"),
        t("Xưởng gia công","Contract workshops")].map(x=>`<span>${x}</span>`).join("")}</div>
    </div>
    <div class="pillars">
      ${[["factory", t("Các công đoạn chính làm tại xưởng","The main stages happen here"),
          t("Kéo sợi, đan máy, khắc, xoắn, bện, hàn khoá và đánh bóng — cùng một nơi, nên một mã đặt lại lần sau vẫn ra đúng sợi đó.",
            "Wire drawing, machine weaving, cutting, twisting, braiding, clasping and polishing under one roof — so re-ordering a code returns the same chain.")],
         ["scale", t("Cân và kiểm trước khi niêm phong","Weighed and checked before sealing"),
          t("Mỗi lô kiểm trọng lượng và tuổi vàng đối chiếu với bảng quy cách. Sai số nằm ngoài bảng thì không xuất xưởng.",
            "Every batch is weighed and assayed against the spec table. Anything outside the table does not leave the floor.")],
         ["ship", t("Đóng gói cho hàng đi xa","Packed for the journey"),
          t("Niêm phong theo lô kèm chứng từ tuổi vàng, sẵn sàng cho khách nội địa lẫn khách nhập khẩu.",
            "Sealed per batch with purity documentation, ready for domestic and importing customers.")]
        ].map(x=>`<div class="pillar"><span class="pi">${ICONS[x[0]]}</span>
          <div><h3>${x[1]}</h3><p>${x[2]}</p></div></div>`).join("")}
      <div class="pillar"><span class="pi">${ICONS.code}</span>
        <div><h3>${t("Chứng nhận","Certifications")}</h3>
        <p style="color:var(--ink-3);font-style:italic">${t("Chưa có thông tin — cần bộ phận sản phẩm xác nhận xưởng đang có chứng nhận nào.","Not yet supplied — the product team needs to confirm which certifications the factory holds.")}<span class="ph">${t("cần thông tin","needs input")}</span></p></div></div>
    </div>
  </div></section>
'''
    s = s[:old_feats.start()] + NEW + s[old_feats.end():]
    n += 1

# ---------------------------------------------------------------- purity table -> alloy cards
rep('''      <div class="tablewrap" style="margin-top:22px"><table style="min-width:400px">
        <thead><tr><th>${t("Tuổi vàng","Purity")}</th><th class="num">${t("Hàm lượng","Fineness")}</th>
          <th>${t("Tương đương","Karat")}</th><th>${t("Màu","Colours")}</th></tr></thead>
        <tbody>
          <tr><td class="code">750</td><td class="num">75,0% Au</td><td>18K</td>
            <td><span class="dot Y" style="display:inline-block;vertical-align:-2px"></span>
                <span class="dot W" style="display:inline-block;vertical-align:-2px"></span>
                <span class="dot R" style="display:inline-block;vertical-align:-2px"></span></td></tr>
          <tr><td class="code">610</td><td class="num">61,0% Au</td><td>≈ 14,6K</td>
            <td><span class="dot Y" style="display:inline-block;vertical-align:-2px"></span>
                <span class="dot W" style="display:inline-block;vertical-align:-2px"></span></td></tr>
        </tbody></table></div>''',
    '''      <div class="alloys" style="margin-top:22px">${PURITIES.map(x=>`
        <div class="alloy">
          <span class="k">${x.k}</span>
          <span class="au">${t(x.au,x.auEn)}% Au</span>
          <span class="kt">${t(x.kt,x.ktEn)}</span>
          <span class="note">${x.spec
            ? t("Có cột trọng lượng trong bảng quy cách","Weight column in the size table")
            : t("Trọng lượng báo theo đơn hàng","Weight quoted per order")}</span>
        </div>`).join("")}</div>''')

rep('${t("Khách trong nước cân theo chỉ, khách xuất khẩu cân theo gram. Mọi bảng ghi song song hai đơn vị nên không bên nào phải quy đổi.","Domestic buyers weigh in chỉ, export buyers in grams. Every table carries both, so neither side has to convert.")}',
    '${t("Xưởng làm bốn tuổi vàng. Bảng size chuẩn hiện có cột trọng lượng cho 750 và 610; tuổi 680 và 416 báo theo từng đơn.","The factory works four purities. The standard size table carries weight columns for 750 and 610; 680 and 416 are quoted per order.")}')

rep('<p>${t("Trích từ catalogue nội bộ. Cột chỉ và gram tính cho vàng 750 và 610.","From the internal catalogue. Chỉ and gram columns for 750 and 610 gold.")}</p></div></div>',
    '<p>${t("Trích từ catalogue nội bộ. Cột chỉ và gram tính cho vàng 750 và 610; tuổi 680 và 416 báo theo đơn.","From the internal catalogue. Chỉ and gram columns for 750 and 610 gold; 680 and 416 quoted per order.")}</p></div></div>')

rep('["scale",t("Quy cách sẵn theo cỡ","Specs ready per gauge"),t("Trọng lượng ghi sẵn cả chỉ và gram cho vàng 750 và 610, kèm chiều dài tiêu chuẩn từng cỡ.","Weights in both chỉ and grams for 750 and 610 gold, with standard lengths per gauge.")],',
    '["scale",t("Quy cách sẵn theo cỡ","Specs ready per gauge"),t("Trọng lượng ghi sẵn cả chỉ và gram, kèm chiều dài tiêu chuẩn từng cỡ.","Weights in both chỉ and grams, with standard lengths per gauge.")],')

# ---------------------------------------------------------------- counters
rep('''function wireExtras(){''',
    '''function animateCounts(root){
  const els = root.querySelectorAll("[data-count]");
  if(!els.length) return;
  if(!("IntersectionObserver" in window) ||
     window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const io = new IntersectionObserver(entries=>{
    entries.forEach(en=>{
      if(!en.isIntersecting) return;
      const el = en.target; io.unobserve(el);
      const end = +el.dataset.count; if(!isFinite(end)) return;
      const t0 = performance.now(), dur = 950;
      const step = now => {
        const k = Math.min(1,(now-t0)/dur);
        el.textContent = Math.round(end * (1 - Math.pow(1-k,3)));
        if(k < 1) requestAnimationFrame(step); else el.textContent = end;
      };
      requestAnimationFrame(step);
    });
  },{threshold:.45});
  els.forEach(el=>io.observe(el));
}

function wireExtras(){''')
rep('  wireDecoder(app);\n  wireExtras();', '  wireDecoder(app);\n  wireExtras();\n  animateCounts(app);')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('stage 2: %d edits\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
