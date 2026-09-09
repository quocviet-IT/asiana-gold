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


# ---- product page: the silver codes for the size on screen -------------------
rep('''    row && row.real750 ? [t("Trọng lượng thực tế","Actual weight"), num(row.real750)+" g (750)"] : null,''',
    '''    row && row.real750 ? [t("Trọng lượng thực tế","Actual weight"), num(row.real750)+" g (750)"] : null,
    (row && row.sv)  ? [t("Mã bạc xi vàng","Gold-plated silver code"), row.sv] : null,
    (row && row.svw) ? [t("Mã bạc","Silver code"), row.svw] : null,''')

# a note under the size table when the whole run is also made in silver
rep('''    </table></div>`:""}
  </div></section>`:""}''',
    '''    </table></div>
    ${spec.rows.some(r=>r.sv||r.svw) ? `<p class="note" style="margin-top:18px">${t(
      "Cả dải cỡ này còn làm bằng bạc và bạc xi vàng, mã bắt đầu bằng SV. Trọng lượng bạc khác trọng lượng vàng và báo riêng theo đơn.",
      "This whole run is also made in silver and gold-plated silver, coded with an SV prefix. Silver weights differ from gold and are quoted per order.")}</p>` : ""}
  </div></section>`:""}''')

# ---- catalogue: a material filter -------------------------------------------
rep("let filt={fam:null,kind:null,color:null,dia:null};",
    "let filt={fam:null,kind:null,color:null,dia:null,mat:null};")
rep('''    (!filt.color||p.colors.includes(filt.color)) && (!filt.dia||p.dia.includes(filt.dia)) &&''',
    '''    (!filt.color||p.colors.includes(filt.color)) && (!filt.dia||p.dia.includes(filt.dia)) &&
    (!filt.mat || (filt.mat==="silver" ? p.silver===true : true)) &&''')
rep('''        ${grp(t("Đường kính","Gauge"),"dia",DIAS.map(d=>({v:d,label:mm(d)+" mm",n:P.filter(p=>p.dia.includes(d)).length})))}''',
    '''        ${grp(t("Đường kính","Gauge"),"dia",DIAS.map(d=>({v:d,label:mm(d)+" mm",n:P.filter(p=>p.dia.includes(d)).length})))}
        ${grp(t("Chất liệu","Material"),"mat",[
          {v:"silver",label:t("Có làm bằng bạc","Also made in silver"),n:P.filter(p=>p.silver===true).length}])}''')
rep('if(e.target.closest("#clear")){ filt={fam:null,kind:null,color:null,dia:null}; catUI.q=""; reflow(); return; }',
    'if(e.target.closest("#clear")){ filt={fam:null,kind:null,color:null,dia:null,mat:null}; catUI.q=""; reflow(); return; }')
rep('  if(fam){ e.preventDefault(); closeLayer(); filt={fam:fam.dataset.fam,kind:null,color:null,dia:null}; catUI.q=""; go("catalogue"); return; }',
    '  if(fam){ e.preventDefault(); closeLayer(); filt={fam:fam.dataset.fam,kind:null,color:null,dia:null,mat:null}; catUI.q=""; go("catalogue"); return; }')
rep('''  filt  = {fam:null, kind:null, color:null, dia:null};
  catUI = {q:"", sort:"code", mode:"grid"};''',
    '''  filt  = {fam:null, kind:null, color:null, dia:null, mat:null};
  catUI = {q:"", sort:"code", mode:"grid"};''')
rep('''    filt.dia   = q.get("dia") ? parseFloat(q.get("dia")) : null;''',
    '''    filt.dia   = q.get("dia") ? parseFloat(q.get("dia")) : null;
    filt.mat   = q.get("mat") || null;''')
rep('''    if(filt.dia)           q.set("dia", filt.dia);''',
    '''    if(filt.dia)           q.set("dia", filt.dia);
    if(filt.mat)           q.set("mat", filt.mat);''')

# ---- home: silver stated next to the gold purities ---------------------------
rep('''      <div class="alloys" style="margin-top:22px">${PURITIES.map(x=>`''',
    '''      <div class="alloys" style="margin-top:22px">${PURITIES.map(x=>`''')
rep('''          <span class="note">${x.spec
            ? t("Có cột trọng lượng trong bảng quy cách","Weight column in the size table")
            : t("Trọng lượng báo theo đơn hàng","Weight quoted per order")}</span>
        </div>`).join("")}</div>''',
    '''          <span class="note">${x.spec
            ? t("Có cột trọng lượng trong bảng quy cách","Weight column in the size table")
            : t("Trọng lượng báo theo đơn hàng","Weight quoted per order")}</span>
        </div>`).join("")}</div>
      <div class="note" style="margin-top:24px">${t(
        "<b>Ngoài vàng, xưởng còn làm bạc và bạc xi vàng.</b> "+
        DATA.specs.reduce((a,g)=>a+g.rows.filter(r=>r.sv||r.svw).length,0)+
        " dòng trong bảng quy cách có mã bạc đi kèm, tiền tố SV. Tuổi bạc và trọng lượng bạc chưa có trong bảng, cần bộ phận sản phẩm bổ sung.",
        "<b>Beyond gold, the factory also works silver and gold-plated silver.</b> "+
        DATA.specs.reduce((a,g)=>a+g.rows.filter(r=>r.sv||r.svw).length,0)+
        " rows in the size table carry a silver code with an SV prefix. Silver grade and silver weights are not in the table yet.")}<span class="ph">${t("cần bổ sung","to supply")}</span></div>''')

# ---- hero slide 2 names the second material ---------------------------------
rep('''   pVi:"Đường kính 2,0 đến 8,0 mm. Tuổi vàng 750, 680, 610 và 416. Vàng, trắng và hồng. Chiều dài 42 đến 50 cm.",
   pEn:"Gauges from 2.0 to 8.0 mm. Purities 750, 680, 610 and 416. Yellow, white and rose. Lengths 42 to 50 cm."},''',
    '''   pVi:"Đường kính 2,0 đến 8,0 mm. Tuổi vàng 750, 680, 610 và 416. Vàng, trắng và hồng. Phần lớn kiểu dây còn làm bằng bạc và bạc xi vàng.",
   pEn:"Gauges from 2.0 to 8.0 mm. Purities 750, 680, 610 and 416. Yellow, white and rose. Most styles are also made in silver and gold-plated silver."},''')

# ---- capabilities: silver as a production line -------------------------------
rep('''        [t("Hàn khoá và hoàn thiện","Clasping and finishing"),t("Khoá lật, khoá ghép, đánh bóng và kiểm tuổi vàng trước khi niêm phong lô.","Lobster and integrated clasps, polishing, purity checks before the batch is sealed.")]''',
    '''        [t("Hàn khoá và hoàn thiện","Clasping and finishing"),t("Khoá lật, khoá ghép, đánh bóng và kiểm tuổi vàng trước khi niêm phong lô.","Lobster and integrated clasps, polishing, purity checks before the batch is sealed.")],
        [t("Dòng bạc và bạc xi vàng","Silver and gold-plated silver"),t("Phần lớn kiểu dây làm được bằng bạc, mã riêng bắt đầu bằng SV. Tuổi bạc và trọng lượng bạc chưa có trong bảng quy cách.","Most styles are also produced in silver under their own SV codes. Silver grade and weights are not in the size table yet.")]''')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('edits %d\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
