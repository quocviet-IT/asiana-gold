# -*- coding: utf-8 -*-
"""Replace the placeholder careers page with the real openings the client sent.
Descriptions collapse behind the same <details> pattern the FAQ already uses."""
import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n = 0

CSS = '''.a ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:7px}
.a li{padding-left:2px}
.qa summary .role{font-family:"Cormorant Garamond",Georgia,serif}
.apply{border-top:1.5px solid var(--ink);padding-top:20px;margin-top:26px;
  display:grid;grid-template-columns:auto 1fr;gap:10px 26px;align-items:baseline;max-width:70ch}
.apply dt{font-family:"EB Garamond",Georgia,serif;font-style:italic;color:var(--ink-2)}
.apply dd{margin:0}
'''
if '.a ul{margin:0' not in s:
    s = s.replace('.hidden{display:none!important}\n</style>', CSS + '.hidden{display:none!important}\n</style>', 1)
    n += 1

JOBS = r'''const JOBS = [
  {vi:"Tư vấn viên — Kênh sỉ", en:"Wholesale sales consultant", d:[
   "Lập kế hoạch kinh doanh tại khu vực phụ trách. Chủ động đề xuất các chương trình nhằm thúc đẩy doanh số.",
   "Thực hiện mục tiêu kinh doanh gồm các chỉ tiêu KPI được giao như lợi nhuận, doanh số theo từng khách hàng hoặc từng giải pháp được phân công.",
   "Tư vấn bán hàng cho khách, tiếp nhận thông tin đặt hàng, phối hợp với Giám sát kinh doanh triển khai thực hiện đơn hàng.",
   "Quản lý tình hình bán hàng và sau bán hàng: sản lượng, doanh thu, hàng trả lại và công nợ khách hàng.",
   "Hỗ trợ chăm sóc khách hàng hiện có. Tìm kiếm, phát triển khách hàng mới theo nhóm thị trường phụ trách.",
   "Thực hiện các báo giá sản phẩm cho từng đối tượng khách hàng, lập hợp đồng thương mại theo quy định của Công ty.",
   "Làm việc với khách hàng, đối tác và các bộ phận liên quan trong Công ty để triển khai đúng hợp đồng và quản lý chi phí bán hàng theo phương án kinh doanh.",
   "Báo cáo theo định kỳ hoặc đột xuất theo yêu cầu.",
   "Thực hiện các công việc khác do cấp trên giao."]},

  {vi:"Kế toán nguyên vật liệu", en:"Materials accountant", d:[
   "Kiểm tra, giám sát nhập liệu chứng từ xuất kho và nhập kho nguyên vật liệu vào file báo cáo.",
   "Kiểm tra, giám sát luân chuyển nguyên vật liệu trong nội bộ Công ty: xuất từ kho cho thợ gia công và nhập ngược lại.",
   "Đảm bảo tính chính xác giá trị vốn (giá thành) để phục vụ cho các báo cáo nguyên vật liệu.",
   "Kiểm tra tình hình ghi chép chứng từ, ghi nhận xuất nhập tồn kho giữa phòng kế toán và các phòng ban liên quan; chủ động yêu cầu điều chỉnh bổ sung cho phù hợp.",
   "Theo dõi chặt chẽ chứng từ, đảm bảo tính chính xác và đồng nhất giữa số liệu thực tế, chứng từ gốc và số liệu trên file mềm.",
   "Thực hiện kiểm kê công cụ dụng cụ, nguyên vật liệu sản xuất; tham gia kiểm kho hàng hóa cuối tháng.",
   "Tính hao hụt nguyên vật liệu công thợ: phân bổ chính xác nguyên vật liệu đã tiêu hao vào đối tượng sử dụng để việc tính giá thành được chính xác.",
   "Báo cáo nguyên vật liệu tại công ty.",
   "Các công việc khác của quản lý và Ban Giám đốc điều phối.",
   "Xây dựng các quy trình, hướng dẫn công việc theo trách nhiệm.",
   "Tuân thủ 100% nội quy và tiêu chuẩn 5S của công ty: lịch làm việc, vệ sinh, dọn hàng, đi trễ."]},

  {vi:"Kế toán thuế", en:"Tax accountant", d:[
   "Tìm hiểu, hệ thống hóa cách thức nhập liệu, chốt sổ và khóa sổ các nội dung trên phần mềm Fast.",
   "Cập nhật đủ và đúng các nghiệp vụ mua vào bán ra, doanh thu, chi phí, tiền mặt, tiền gửi ngân hàng.",
   "Thực hiện việc xuất hóa đơn bán hàng theo quy định tài chính.",
   "Theo dõi, hạch toán đủ và đúng các nghiệp vụ đầu tư, mua sắm tài sản cố định và công cụ dụng cụ.",
   "Theo dõi, hạch toán, trích lập đầy đủ các khoản chi phí cần phân bổ và chi phí khấu hao tài sản cố định.",
   "Lập biên bản kiểm kê tài sản cố định và công cụ dụng cụ theo quy định tài chính, thực hiện cùng kế toán nguyên vật liệu.",
   "Theo dõi, hạch toán các nghiệp vụ liên quan trích lương và trích nộp BHXH, BHYT, BHTN, KPCĐ theo quy định tài chính.",
   "Theo dõi, hạch toán các nghiệp vụ liên quan các khoản phải thu, phải trả và công nợ.",
   "Theo dõi, hạch toán các nghiệp vụ liên quan đến mua vào, bán ra, hàng hóa tồn kho và công nợ.",
   "Đảm bảo công tác chốt sổ, khóa sổ kế toán hàng tháng đủ và đúng theo quy định hiện hành.",
   "Lập và nộp các báo cáo thuế, báo cáo Ngân hàng Nhà nước hàng quý theo quy định hiện hành.",
   "Lập và nộp các báo cáo thuế, báo cáo tài chính, báo cáo thống kê, báo cáo Ngân hàng Nhà nước hàng năm.",
   "Đảm bảo nộp các khoản thuế phát sinh hàng quý và hàng năm đúng quy định hiện hành.",
   "Chịu trách nhiệm về các giao dịch với cơ quan Thuế, Sở Kế hoạch và Đầu tư, Hải quan, kiểm toán, và các đối tác như ngân hàng, khách hàng, nhà cung cấp.",
   "Yêu cầu chung: số liệu chính xác, đầy đủ, chi tiết và gửi đúng thời hạn; không thất thoát, không thừa thiếu không rõ nguyên nhân."]},

  {vi:"Kế toán tổng hợp", en:"General accountant", d:[
   "Hạch toán doanh thu, chi phí, khấu hao tài sản cố định.",
   "Lập và làm các báo cáo thuế hàng tháng, hàng quý.",
   "Lên bảng cân đối phát sinh lỗ lãi, trích lương, đóng và làm việc với bảo hiểm xã hội.",
   "Chịu trách nhiệm về các giao dịch với cơ quan Thuế, Sở Kế hoạch và Đầu tư, Hải quan, và các đối tác như ngân hàng, khách hàng, nhà cung cấp.",
   "Trực tiếp báo cáo lên kế toán trưởng việc thực hiện các kế hoạch tài chính trong tháng, quý, năm.",
   "Xử lý các báo cáo của kế toán viên về nghiệp vụ và quản lý doanh thu, chi phí.",
   "Hợp tác cùng các cơ quan kiểm toán để thực hiện các báo cáo kết quả kinh doanh chính xác.",
   "Quản lý và kiểm soát các thanh toán trong và ngoài nước.",
   "Theo dõi, quản lý, giám sát số liệu bán hàng: giá vốn, giá bán, khách hàng, hàng tồn kho, công nợ.",
   "Giám sát và theo dõi kiểm kê cùng phòng kho và phòng vật tư; tham gia kiểm kho hàng hóa cuối tháng.",
   "Báo cáo nguyên vật liệu.",
   "Thực hiện các công việc khác theo điều phối của quản lý trực tiếp."]},

  {vi:"Trợ lý kỹ thuật", en:"Technical assistant", d:[
   "Chủ động theo dõi và đánh giá tình trạng máy móc, thiết bị sản xuất; phát hiện sớm rủi ro và thực hiện biện pháp phòng ngừa.",
   "Thực hiện các công việc vận hành, hiệu chỉnh và bảo trì thường xuyên; kiểm tra, bảo dưỡng định kỳ và xử lý sự cố máy móc, thiết bị sản xuất.",
   "Phối hợp với các bộ phận liên quan để giải quyết các vấn đề kỹ thuật phát sinh trong quá trình sản xuất.",
   "Đánh giá và phân tích hiệu suất máy móc, thiết bị; đề xuất các phương án cải tiến để nâng cao năng suất, chất lượng sản phẩm và giảm thiểu lãng phí.",
   "Lập báo cáo, cập nhật hồ sơ kỹ thuật và lịch trình bảo dưỡng máy móc định kỳ.",
   "Các công việc khác do cấp trên giao phó."]}
];

function careersHTML(){
  return `<section><div class="wrap">
    <div class="crumb"><button data-nav="home">${t("Trang chủ","Home")}</button> / <span>${t("Tuyển dụng","Careers")}</span></div>
    <h1 style="font-size:clamp(1.95rem,3.6vw,2.9rem);margin:0 0 16px">${t("Tuyển dụng","Careers")}</h1>
    <p class="lede">${t(
      "Cơ hội việc làm của bạn ở đây. Xưởng đặt tại TP. Hồ Chí Minh, đang tuyển "+JOBS.length+" vị trí.",
      "Your job is here. The factory is in Ho Chi Minh City and is hiring for "+JOBS.length+" positions.")}</p>

    <dl class="apply">
      <dt>${t("Cách ứng tuyển","How to apply")}</dt>
      <dd>${t("Gửi hồ sơ về","Send your application to")} <a class="mono" href="mailto:hr@asiana-gold.com">hr@asiana-gold.com</a></dd>
      <dt>${t("Tiêu đề email","Email subject")}</dt>
      <dd>${t("Họ tên + ứng tuyển + vị trí công việc","Full name + ứng tuyển + position")}</dd>
    </dl>

    <h2 style="margin:44px 0 0;font-size:1.6rem">${t("Vị trí đang tuyển","Open positions")}</h2>
    ${lang==="en"?`<p style="color:var(--ink-3);font-style:italic;margin-top:8px">Job descriptions are written in Vietnamese.</p>`:""}
    <div class="faq" style="margin-top:20px">${JOBS.map((j,i)=>`
      <details class="qa"${i===0?" open":""}>
        <summary>${esc(t(j.vi,j.en))}</summary>
        <div class="a"><ul>${j.d.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>
      </details>`).join("")}</div>
  </div></section>`;
}
'''

old = re.search(r'function careersHTML\(\)\{.*?\n\}\n', s, re.S)
if old:
    s = s[:old.start()] + JOBS + s[old.end():]
    n += 1
else:
    sys.stderr.write('!! careersHTML not found\n')
    sys.exit(1)

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('edits %d\n' % n)
