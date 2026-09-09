import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new, count=1):
    global s, n
    if old not in s:
        miss.append(old[:78].replace('\n', ' '))
        return
    s = s.replace(old, new, count)
    n += 1


# ============ hero: plain statements, no italic accent ============
rep('''   eyeVi:"Xưởng sản xuất · TP. Hồ Chí Minh", eyeEn:"Manufacturing · Ho Chi Minh City",
   hVi:"Dây chuyền vàng 18K,<br><em>sản xuất theo mã.</em>", hEn:"18K gold chains,<br><em>made to code.</em>",
   pVi:"Xưởng dây chuyền vàng quy mô công nghiệp tại Việt Nam. Mọi mẫu đều có mã đọc được và bảng trọng lượng chuẩn — khách sỉ đặt hàng chỉ bằng một dòng mã.",
   pEn:"Industrial-scale gold chain manufacturing in Vietnam. Every model has a readable code and a standard weight table — wholesale buyers order with a single line."},''',
    '''   eyeVi:"TP. Hồ Chí Minh", eyeEn:"Ho Chi Minh City",
   hVi:"Xưởng dây chuyền vàng 18K", hEn:"18K gold chain factory",
   pVi:"Gia công dây chuyền và lắc tay vàng cho tiệm vàng trong nước và khách nhập khẩu. Catalogue 62 mẫu, mỗi mẫu có mã riêng và bảng trọng lượng theo từng cỡ.",
   pEn:"Gold chains and bracelets made for jewellers and importing customers. A catalogue of 62 models, each with its own code and a weight table for every size."},''')
rep('''   eyeVi:"Bốn tuổi vàng · sáu cỡ", eyeEn:"Four purities · six gauges",
   hVi:"Đủ cỡ, đủ tuổi vàng,<br><em>đủ chiều dài.</em>", hEn:"Every gauge, purity<br><em>and length.</em>",
   pVi:"Từ 2,0 đến 8,0 mm, tuổi vàng 750 · 680 · 610 · 416, ba màu vàng — trắng — hồng, chiều dài 42 đến 50 cm.",
   pEn:"From 2.0 to 8.0 mm, in 750 · 680 · 610 · 416 gold, yellow — white — rose, lengths 42 to 50 cm."},''',
    '''   eyeVi:"Quy cách", eyeEn:"Specifications",
   hVi:"Bốn tuổi vàng, sáu cỡ đường kính", hEn:"Four purities, six gauges",
   pVi:"Đường kính 2,0 đến 8,0 mm. Tuổi vàng 750, 680, 610 và 416. Vàng, trắng và hồng. Chiều dài 42 đến 50 cm.",
   pEn:"Gauges from 2.0 to 8.0 mm. Purities 750, 680, 610 and 416. Yellow, white and rose. Lengths 42 to 50 cm."},''')
rep('''   eyeVi:"Nhận OEM / ODM", eyeEn:"OEM / ODM welcome",
   hVi:"Gửi mẫu của bạn,<br><em>xưởng dựng khuôn riêng.</em>", hEn:"Send your sample,<br><em>we cut the die.</em>",''',
    '''   eyeVi:"Gia công", eyeEn:"Contract work",
   hVi:"Nhận gia công theo mẫu riêng", hEn:"Contract work to your pattern",''')

# ============ numbers ============
rep('''      <span class="eyebrow">${t("Asiana Gold bằng con số","Asiana Gold by the numbers")}</span>
      <h2>${t("Một catalogue đã chuẩn hoá đến từng cỡ","A catalogue standardised down to the gauge")}</h2>
      <p>${t("Không phải album ảnh. Mỗi mẫu có mã đọc được, mỗi cỡ có trọng lượng ghi sẵn theo cả chỉ lẫn gram.","Not a photo album. Every model carries a readable code, and every size carries a weight in both chỉ and grams.")}</p>''',
    '''      <h2>${t("Catalogue","The catalogue")}</h2>
      <p>${t("62 mẫu dây chuyền và lắc tay. Mỗi mẫu có mã riêng, mỗi cỡ có trọng lượng ghi theo chỉ và gram.","62 chain and bracelet models. Each has its own code, and each size has a weight in chỉ and grams.")}</p>''')
rep('<span>${t("Bốn con số còn chờ bộ phận sản phẩm cấp:","Four figures still awaiting the product team:")}</span>',
    '<span>${t("Chưa có số liệu:","Not yet supplied:")}</span>')

# ============ families ============
rep('''      <div><span class="eyebrow">${t("Dòng sản phẩm","Product families")}</span>
        <h2>${t("Tám dòng dây chuyền và lắc tay","Eight chain and bracelet families")}</h2>''',
    '''      <div>
        <h2>${t("Dòng sản phẩm","Product families")}</h2>''')
rep('<button class="btn btn-line" data-nav="catalogue">${t("Xem tất cả","See all")} →</button>',
    '<button class="btn btn-line" data-nav="catalogue">${t("Xem toàn bộ catalogue","See the whole catalogue")}</button>')
rep('<u>${t("Xem dòng này","View family")} →</u>', '<u>${t("Xem dòng này","View family")}</u>')

# ============ who we work for ============
rep('''      <span class="eyebrow">${t("Chúng tôi làm cho ai","Who we work for")}</span>
      <h2 style="margin:12px 0 16px">${t("Asiana Gold chỉ làm hàng sỉ<br><em>và hàng gia công.</em>","Asiana Gold works wholesale<br><em>and contract only.</em>")}</h2>
      <p class="lede">${t(
        "Không bán lẻ từng sợi. Khách của xưởng là những nơi mua theo lô, đọc bảng quy cách trước khi hỏi giá, và cần cùng một mẫu giao đi giao lại giống hệt nhau.",
        "We do not sell single pieces. Our customers buy by the batch, read the spec sheet before asking a price, and need the same model to arrive identical every time.")}</p>''',
    '''      <h2 style="margin:0 0 16px">${t("Khách hàng của xưởng","Who we supply")}</h2>
      <p class="lede">${t(
        "Xưởng bán sỉ và nhận gia công theo mẫu. Khách đặt theo lô và thường đặt lại cùng một mã nhiều lần, nên mỗi mã phải cho ra đúng một sợi như nhau.",
        "We sell wholesale and take contract work. Customers order by the batch and re-order the same code repeatedly, so a code has to produce the same chain every time.")}</p>''')
rep('t("Đóng gói cho hàng đi xa","Packed for the journey")', 't("Đóng gói và chứng từ","Packing and paperwork")')

# ============ decoder ============
rep('''      <span class="eyebrow on-dark">${t("Hệ mã sản phẩm","The code system")}</span>
      <h2 style="margin:12px 0 14px">${t("Đọc được cả sợi dây<br><em>chỉ từ tám ký tự</em>","Eight characters<br><em>describe the whole chain</em>")}</h2>
      <p class="lede">${t("Rê chuột lên từng ký tự để xem nó nói gì. Đây là hệ mã nội bộ Asiana Gold dùng cho toàn bộ catalogue — khách sỉ quen mã rồi thì đặt hàng chỉ mất một dòng.","Hover any character to see what it says. This is the internal code system behind the whole Asiana Gold catalogue — once a buyer knows it, an order takes one line.")}</p>
      <div class="note" style="margin-top:20px">${t("<b>Đường kính nằm ngay trong mã.</b> Hai chữ số sau màu vàng là phần mười milimét: <span class='mono'>CY<b>25</b>SR</span> là 2,5 mm.","<b>The gauge lives in the code.</b> The two digits after the gold colour are tenths of a millimetre: <span class='mono'>CY<b>25</b>SR</span> is 2.5 mm.")}</div>''',
    '''      <h2 style="margin:0 0 16px">${t("Cách đọc mã sản phẩm","Reading a product code")}</h2>
      <p class="lede">${t("Rê chuột lên từng ký tự để xem nó chỉ gì. Toàn bộ catalogue dùng chung hệ mã này.","Hover a character to see what it stands for. The whole catalogue uses this one system.")}</p>
      <div class="note" style="margin-top:24px">${t("Hai chữ số sau ký tự màu vàng là đường kính tính theo phần mười milimét, nên <span class='mono'>CY25SR</span> là 2,5 mm. Dây bi ghi thẳng cỡ bi: <span class='mono'>CBY2.5</span>.","The two digits after the gold-colour letter are the gauge in tenths of a millimetre, so <span class='mono'>CY25SR</span> is 2.5 mm. Bead chains carry the bead size directly: <span class='mono'>CBY2.5</span>.")}</div>''')

# ============ featured / finder / gauge / purity / process / faq / cta ============
rep('''      <div><span class="eyebrow">${t("Mẫu tiêu biểu","Selected models")}</span>
        <h2>${t("Tám mẫu chủ lực trong catalogue","Eight staples from the catalogue")}</h2></div>
      <button class="btn btn-line" data-nav="catalogue">${t("Toàn bộ","All")} ${P.length} →</button>''',
    '''      <div><h2>${t("Mẫu tiêu biểu","Selected models")}</h2></div>
      <button class="btn btn-line" data-nav="catalogue">${t("Xem toàn bộ "+P.length+" mẫu","See all "+P.length+" models")}</button>''')
rep('''      <span class="eyebrow">${t("Công cụ","Tool")}</span>
      <h2>${t("Tra cứu quy cách theo cỡ","Find the spec by gauge")}</h2>''',
    '''      <h2>${t("Tra cứu quy cách theo cỡ","Find the spec by gauge")}</h2>''')
rep('''      <span class="eyebrow">${t("Đường kính","Gauge")}</span>
      <h2 style="margin:12px 0 14px">${t("Sáu cỡ, vẽ đúng kích thước thật","Six gauges, drawn at true size")}</h2>
      <p class="lede">${t("Các thanh bên dưới dùng đơn vị milimét thật của trình duyệt, nên chúng rộng đúng bằng đường kính sợi dây. Đặt ngón tay lên màn hình là ước được cỡ cần đặt.","The bars below use real browser millimetres, so each is exactly as wide as the chain itself. Hold a finger to the screen and you have your gauge.")}</p>''',
    '''      <h2 style="margin:0 0 14px">${t("Đường kính theo tỉ lệ thật","Gauges at true size")}</h2>
      <p class="lede">${t("Các thanh dưới đây vẽ bằng đơn vị milimét của trình duyệt, nên rộng đúng bằng đường kính sợi dây.","The bars below are drawn in browser millimetres, so each is as wide as the chain itself.")}</p>''')
rep('''      <span class="eyebrow">${t("Tuổi vàng & đơn vị","Purity & units")}</span>
      <h2 style="margin:12px 0 14px">${t("Bảng quy cách ghi cả chỉ và gram","Specs carry both chỉ and grams")}</h2>''',
    '''      <h2 style="margin:0 0 14px">${t("Tuổi vàng","Gold purity")}</h2>''')
rep('''      <span class="eyebrow">${t("Quy trình OEM / ODM","OEM / ODM process")}</span>
      <h2>${t("Từ mã đến lô hàng, năm chặng","From code to shipment, five stages")}</h2>''',
    '''      <h2>${t("Quy trình sản xuất","How an order runs")}</h2>''')
rep('''      <span class="eyebrow">${t("Câu hỏi thường gặp","Frequently asked")}</span>
      <h2>${t("Khách sỉ hay hỏi gì trước","What wholesale buyers ask first")}</h2>''',
    '''      <h2>${t("Câu hỏi thường gặp","Common questions")}</h2>''')
rep('<div><h2>${t("Gửi danh sách mã, nhận báo giá.","Send the codes, get a quote.")}</h2>',
    '<div><h2>${t("Yêu cầu báo giá","Request a quote")}</h2>')

# ============ capabilities page ============
rep('''    <span class="eyebrow">${t("Năng lực xưởng","Factory capabilities")}</span>
    <h1 style="font-size:clamp(1.95rem,3.6vw,2.9rem);margin:12px 0 16px">${t("Một xưởng, một hệ mã, một bảng quy cách","One factory, one code system, one spec sheet")}</h1>''',
    '''    <h1 style="font-size:clamp(1.95rem,3.6vw,2.9rem);margin:0 0 16px">${t("Năng lực sản xuất","What the factory does")}</h1>''')
rep('''      <span class="eyebrow">${t("Trên chuyền","On the floor")}</span>
      <h2 style="margin:12px 0 18px">${t("Xưởng làm được gì","What we can make")}</h2>''',
    '''      <h2 style="margin:0 0 18px">${t("Công đoạn sản xuất","Production stages")}</h2>''')
rep('''      <span class="eyebrow">${t("Còn thiếu","Still missing")}</span>
      <h2 style="margin:12px 0 14px">${t("Bốn con số bộ phận sản phẩm phải cấp","Four figures the product team must supply")}</h2>
      <p class="lede" style="font-size:.93rem">${t("Đây là những con số khách sỉ tìm đầu tiên. Bản dựng này để trống có chủ ý — không bịa số cho một xưởng đang chào khách xuất khẩu.","These are the first things a wholesale buyer looks for. This study leaves them blank on purpose — no invented figures.")}</p>''',
    '''      <h2 style="margin:0 0 14px">${t("Số liệu chưa có","Figures still missing")}</h2>
      <p class="lede">${t("Bốn ô dưới đây để trống. Bộ phận sản phẩm cần cấp số thật trước khi trang lên sóng.","The four rows below are blank. The product team needs to supply real figures before this page goes live.")}</p>''')
rep('''    <div class="sec-head"><div><span class="eyebrow">${t("Bảng quy cách chuẩn","Standard spec groups")}</span>
      <h2>${t("Mười bốn nhóm, đủ cỡ và trọng lượng","Fourteen groups, every gauge and weight")}</h2>''',
    '''    <div class="sec-head"><div>
      <h2>${t("Bảng quy cách đầy đủ","The full size table")}</h2>''')

# ============ careers / contact ============
rep('''    <span class="eyebrow">${t("Tuyển dụng","Careers")}</span>
    <h1 style="font-size:clamp(1.95rem,3.6vw,2.9rem);margin:12px 0 16px">${t("Làm việc tại xưởng","Work on the floor")}</h1>''',
    '''    <h1 style="font-size:clamp(1.95rem,3.6vw,2.9rem);margin:0 0 16px">${t("Tuyển dụng","Careers")}</h1>''')
rep('''    <span class="eyebrow">${t("Liên hệ & báo giá","Contact & quotes")}</span>
    <h1''', '''    <h1''')

# ============ product page: drop the roman block and the arrows ============
m = re.search(r'\n  <section><div class="wrap">\n    <div class="romans stagger">.*?</div>\n  </div></section>\n', s, re.S)
if m:
    s = s[:m.start()] + '\n' + s[m.end():]
    n += 1
else:
    miss.append('romans block')
s = re.sub(r'\n  const romans = \[\n.*?\n  \];\n', '\n', s, count=1, flags=re.S)

rep('<button class="back-link" data-fam="${esc(p.secVi)}">← ${t("Về dòng","Back to")}',
    '<button class="back-link" data-fam="${esc(p.secVi)}">${t("Về dòng","Back to")}')
rep('<button class="btn btn-line btn-sm" data-fam="${esc(p.secVi)}">${t("Xem cả dòng","See the family")} →</button>',
    '<button class="btn btn-line btn-sm" data-fam="${esc(p.secVi)}">${t("Xem cả dòng","See the family")}</button>')
rep('''    <span class="eyebrow" style="margin-top:18px">${t("Khi anh chị sẵn sàng","When you are ready")}</span>
    <h2 style="margin:12px 0 12px">''',
    '''    <h2 style="margin:0 0 12px">''')
rep('<button class="back" data-nav="catalogue">← ${t("Quay lại catalogue","Back to catalogue")}</button>',
    '<button class="back" data-nav="catalogue">${t("Quay lại catalogue","Back to catalogue")}</button>')

# drop the ornament markup that CSS now hides
s = s.replace('<div class="orn">${LINKMARK}</div>\n', '')
s = s.replace('    <div class="orn">${LINKMARK}</div>\n', '')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('copy pass: %d edits\n' % n)
for mm in miss:
    sys.stderr.write('MISS: ' + mm + '\n')
sys.stderr.write('arrows left: %d\n' % (s.count('} →') + s.count('←')))
sys.stderr.write('<em> left: %d\n' % s.count('<em>'))
