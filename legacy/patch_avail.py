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


# ---- CSS: a quiet status mark, not a badge ----------------------------------
rep('.hidden{display:none!important}\n</style>',
    '''.stat{display:inline-flex;align-items:baseline;gap:7px;white-space:nowrap}
.stat::before{content:"";width:7px;height:7px;border-radius:99px;background:var(--ink-3);flex-shrink:0;
  align-self:center}
.stat.yes::before{background:#3E7A4E}
.stat.no::before{background:#B0894A}
td .stat{font-size:.9rem}
.hidden{display:none!important}
</style>''')

# ---- availability helper -----------------------------------------------------
rep('const prod = code => P.find(x=>x.ag===code);',
    '''const prod = code => P.find(x=>x.ag===code);
const availOf = code => (DATA.avail && DATA.avail[String(code||"").toUpperCase()]) || null;
function statusHTML(a){
  if(!a) return `<span style="color:var(--ink-3)">${t("chưa có thông tin","not yet supplied")}</span>`
    + `<span class="ph">${t("cần thông tin","needs input")}</span>`;
  return a.can
    ? `<span class="stat yes">${t("Đặt được ngay","Available to order")}</span>`
    : `<span class="stat no">${t("Làm theo đơn — hỏi trước","Made to order — ask first")}</span>`;
}''')

# ---- product page: real MOQ, real status, and the dropped-gauge note ---------
rep('''    [t("Sản xuất","Made"), t("Tại xưởng, từ kéo sợi đến đánh bóng","In-house, wire drawing to polish")]
  ].filter(Boolean);''',
    '''    [t("Sản xuất","Made"), t("Tại xưởng, từ kéo sợi đến đánh bóng","In-house, wire drawing to polish")]
  ].filter(Boolean);
  const av = availOf(shownCode) || availOf(p.ag);
  const moqText = av && av.moq
    ? num(av.moq) + " " + (lang==="vi" ? (av.unit || "sợi")
        : ({"sợi":"pcs","vòng":"pcs","viên":"pcs"}[av.unit] || "pcs"))
    : null;
  // the official table dropped some gauges; say so instead of quietly showing another size
  const ownGone = spec && !spec.rows.some(r => r.y.toUpperCase() === p.ag.toUpperCase());''')

rep('''    row ? [t("Chiều dài","Length"), len(row.length)] : null,''',
    '''    row ? [t("Chiều dài","Length"), len(row.length)] : null,
    row && row.real750 ? [t("Trọng lượng thực tế","Actual weight"), num(row.real750)+" g (750)"] : null,''')

rep('''        <ul class="spec-list">${specItems.map(x=>`<li><b>${esc(x[0])}:</b> <span>${esc(x[1])}</span></li>`).join("")}</ul>''',
    '''        <ul class="spec-list">${specItems.map(x=>`<li><b>${esc(x[0])}:</b> <span>${esc(x[1])}</span></li>`).join("")}
          <li><b>${t("Tình trạng","Status")}:</b> ${statusHTML(av)}</li>
          <li><b>${t("Đặt hàng tối thiểu","Minimum order")}:</b> <span>${moqText ? esc(moqText)
            : t("theo thoả thuận","by agreement")+'<span class="ph">'+t("cần số liệu","needs figure")+'</span>'}</span></li>
        </ul>
        ${ownGone ? `<div class="note" style="margin-top:18px">${t(
          "Cỡ "+(gaugeOf(p.ag)!=null?mm(gaugeOf(p.ag))+" mm":p.ag)+" không còn trong bảng quy cách chính thức. Các cỡ đang làm bắt đầu từ "+
            (gaugeOf(spec.rows[0].y)!=null?mm(gaugeOf(spec.rows[0].y))+" mm":spec.rows[0].y)+".",
          "The "+(gaugeOf(p.ag)!=null?mm(gaugeOf(p.ag))+" mm":p.ag)+" gauge is no longer in the official size table. Current sizes start at "+
            (gaugeOf(spec.rows[0].y)!=null?mm(gaugeOf(spec.rows[0].y))+" mm":spec.rows[0].y)+".")}</div>` : ""}''')

# ---- product size table: actual weight + per-size status --------------------
rep('''        <th class="num">${t("Chỉ 610","Chỉ 610")}</th><th class="num">${t("Gram 610","Gram 610")}</th>
        <th>${t("Chiều dài","Length")}</th></tr></thead>
      <tbody>${spec.rows.map(r=>`<tr class="pick${r.y===chosen?" on":""}" data-size="${esc(r.y)}">
        <td class="code">${esc(r.y)}</td><td class="code" style="color:var(--ink-3)">${esc(r.w||"—")}</td>
        <td class="num">${num(r.c750)}</td><td class="num">${num(r.g750)}</td>
        <td class="num">${num(r.c610)}</td><td class="num">${num(r.g610)}</td>
        <td class="mono" style="font-size:.81rem">${esc(len(r.length))}</td></tr>`).join("")}</tbody>''',
    '''        <th class="num">${t("Chỉ 610","Chỉ 610")}</th><th class="num">${t("Gram 610","Gram 610")}</th>
        <th class="num">${t("Thực tế 750","Actual 750")}</th>
        <th>${t("Chiều dài","Length")}</th><th>${t("Tình trạng","Status")}</th></tr></thead>
      <tbody>${spec.rows.map(r=>`<tr class="pick${r.y===chosen?" on":""}" data-size="${esc(r.y)}">
        <td class="code">${esc(r.y)}</td><td class="code" style="color:var(--ink-3)">${esc(r.w||"—")}</td>
        <td class="num">${num(r.c750)}</td><td class="num">${num(r.g750)}</td>
        <td class="num">${num(r.c610)}</td><td class="num">${num(r.g610)}</td>
        <td class="num">${r.real750!=null?num(r.real750):"—"}</td>
        <td class="mono" style="font-size:.81rem">${esc(len(r.length))}</td>
        <td>${r.can==null?'<span style="color:var(--ink-3)">—</span>'
             :(r.can?`<span class="stat yes">${t("Sẵn","Ready")}</span>`
                    :`<span class="stat no">${t("Theo đơn","To order")}</span>`)}</td></tr>`).join("")}</tbody>''')

# ---- capabilities page: MOQ is no longer a blank -----------------------------
rep('''        <tbody>${[t("Năng lực sản xuất mỗi tháng","Monthly output"),t("Số lượng đặt tối thiểu (MOQ)","Minimum order quantity"),
          t("Thời gian sản xuất tiêu chuẩn","Standard lead time"),t("Thị trường xuất khẩu","Export markets served")]
          .map(r=>`<tr><td>${r}</td><td style="color:var(--ink-3)">—<span class="ph">${t("cần số liệu","needs figure")}</span></td></tr>`).join("")}</tbody>''',
    '''        <tbody>${[
          [t("Số lượng đặt tối thiểu (MOQ)","Minimum order quantity"),
           t("5 sợi mỗi mã","5 pieces per code"), true],
          [t("Mẫu đặt được ngay","Models orderable now"),
           Object.values(DATA.avail||{}).filter(x=>x.can).length + " / " + Object.keys(DATA.avail||{}).length, true],
          [t("Năng lực sản xuất mỗi tháng","Monthly output"), null, false],
          [t("Thời gian sản xuất tiêu chuẩn","Standard lead time"), null, false],
          [t("Thị trường xuất khẩu","Export markets served"), null, false]
        ].map(r=>`<tr><td>${r[0]}</td><td>${r[2]?esc(r[1])
            :'<span style="color:var(--ink-3)">—</span><span class="ph">'+t("cần số liệu","needs figure")+'</span>'}</td></tr>`).join("")}</tbody>''')

# ---- catalogue card: a quiet mark for what is orderable now -------------------
rep('''      <span class="foot">${p.colors.map(c=>`<span class="dot ${c}"></span>`).join("")}
        ${p.spec?`<span class="count" style="margin-left:auto">${p.spec.rows.length} ${t("cỡ","sizes")}</span>`:""}</span>''',
    '''      <span class="foot">${p.colors.map(c=>`<span class="dot ${c}"></span>`).join("")}
        ${p.avail && p.avail.can?`<span class="stat yes count" style="margin-left:6px">${t("Sẵn","Ready")}</span>`:""}
        ${p.spec?`<span class="count" style="margin-left:auto">${p.spec.rows.length} ${t("cỡ","sizes")}</span>`:""}</span>''')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('edits %d\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
