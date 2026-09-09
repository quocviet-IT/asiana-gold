# -*- coding: utf-8 -*-
"""Wire the quote form to the sales inbox.

The site is a single static file, so there is no server to post to. Composing a
prefilled message in the visitor's own mail client is the one route that really
reaches pkd@asiana-gold.com without a form service or an email API key. A copy
button covers visitors whose browser has no mail client attached."""
import os, re, sys

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


NEW = r'''  if(e.target.id!=="rfq-form") return;
  e.preventDefault();

  const val = id => { const el = document.getElementById(id); return el ? el.value.trim() : ""; };
  const NL = String.fromCharCode(13) + String.fromCharCode(10);
  const co = val("f-co");
  const total = rfq.reduce((a,x)=>a+(+x.qty||0),0);

  const L = [];
  L.push(t("YÊU CẦU BÁO GIÁ","QUOTE REQUEST"));
  L.push("");
  L.push(t("Công ty","Company") + ": " + co);
  L.push(t("Người liên hệ","Contact") + ": " + val("f-name"));
  L.push("Email: " + val("f-mail"));
  L.push(t("Điện thoại / Zalo","Phone / Zalo") + ": " + val("f-tel"));
  L.push(t("Thị trường","Market") + ": " + val("f-country"));
  L.push(t("Tuổi vàng","Purity") + ": " + val("f-purity"));
  L.push(t("Số lượng dự kiến","Intended quantity") + ": " + val("f-qty"));
  L.push("");
  if(rfq.length){
    L.push(t("Mã quan tâm","Codes requested") + " (" + rfq.length + " " + t("mã","codes") + ", " + total + " " + t("sợi","pcs") + "):");
    rfq.forEach(it=>{
      const pr = prod(it.ag);
      L.push("  - " + (it.size || it.ag) + "   " + (pr ? t(pr.vi, pr.en || pr.vi) : "") + "   x" + it.qty);
    });
  } else {
    L.push(t("Chưa chọn mã cụ thể.","No specific codes selected."));
  }
  const note = val("f-note");
  if(note){ L.push(""); L.push(t("Ghi chú","Notes") + ": " + note); }
  L.push("");
  L.push(t("Gửi từ","Sent from") + " " + location.origin);

  const subject = t("Yêu cầu báo giá","Quote request") + (co ? " — " + co : "");
  const body = L.join(NL);
  lastQuoteText = subject + NL + NL + body;

  const href = "mailto:pkd@asiana-gold.com?subject=" + encodeURIComponent(subject) +
               "&body=" + encodeURIComponent(body);
  try { window.location.href = href; } catch(err){}

  $("#form-msg").innerHTML = t(
    "Đang mở thư gửi tới pkd@asiana-gold.com. Nếu máy không tự mở, bấm ",
    "Opening a message to pkd@asiana-gold.com. If nothing opens, use ") +
    '<button type="button" id="copy-quote" class="linkish">' +
    t("sao chép nội dung","copy the text") + '</button>' +
    t(" rồi dán vào email.", " and paste it into an email.");
});

/* the composed message, kept so it can be copied if no mail client answers */
let lastQuoteText = "";
document.addEventListener("click", e => {
  if(!e.target.closest("#copy-quote")) return;
  const done = ok => { const m=$("#form-msg"); if(m) m.textContent = ok
    ? t("Đã sao chép. Dán vào email gửi pkd@asiana-gold.com.","Copied. Paste it into an email to pkd@asiana-gold.com.")
    : t("Không sao chép được. Hãy chọn và chép thủ công.","Could not copy. Please select and copy manually."); };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(lastQuoteText).then(()=>done(true), ()=>done(false));
  } else {
    try{
      const ta=document.createElement("textarea"); ta.value=lastQuoteText;
      ta.style.cssText="position:fixed;left:-9999px"; document.body.appendChild(ta);
      ta.select(); const ok=document.execCommand("copy"); ta.remove(); done(ok);
    }catch(err){ done(false); }
  }
});'''

rep('''  if(e.target.id!=="rfq-form") return;
  e.preventDefault();
  const total=rfq.reduce((a,x)=>a+(+x.qty||0),0);
  $("#form-msg").textContent = t(
    "Bản dựng thiết kế — form chưa nối máy chủ. Sẽ gửi "+rfq.length+" mã, tổng "+total+" sợi.",
    "Design study — the form is not wired to a server. Would send "+rfq.length+" codes, "+total+" pieces.");
});''', NEW)

# a button that reads as a link inside running text
rep('.hidden{display:none!important}\n</style>',
    '''.linkish{font:inherit;color:var(--g700);text-decoration:underline;text-underline-offset:3px;
  padding:0;background:none;border:0;cursor:pointer}
.linkish:hover{color:var(--ink)}
.hidden{display:none!important}
</style>''')

# say where it goes, right above the send button
rep('''          <button class="btn btn-gold" type="submit">${t("Gửi yêu cầu","Send request")}</button>
          <span id="form-msg" class="count"></span>''',
    '''          <button class="btn btn-gold" type="submit">${t("Gửi yêu cầu","Send request")}</button>
          <span id="form-msg" class="count"></span>
          <p style="flex-basis:100%;margin-top:4px;font-size:.94rem;color:var(--ink-3);font-style:italic">${t(
            "Yêu cầu được gửi tới pkd@asiana-gold.com.",
            "Requests go to pkd@asiana-gold.com.")}</p>''')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('edits %d\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
