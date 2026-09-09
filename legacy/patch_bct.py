# -*- coding: utf-8 -*-
"""Add the Bộ Công Thương notification mark to the footer.

Drawn as vector: online.gov.vn now serves its assets through a JS app, so the
old static PNG path 404s, and an http-only image would be blocked as mixed
content on an https page anyway."""
import os, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new):
    global s, n
    if old not in s:
        miss.append(old[:90].replace('\n', ' '))
        return
    s = s.replace(old, new, 1)
    n += 1


BADGE = '''      <a class="bct" href="http://online.gov.vn/" target="_blank" rel="noopener"
         aria-label="Đã thông báo Bộ Công Thương">
        <svg viewBox="0 0 360 118" role="img" aria-hidden="true">
          <defs><path id="bctArc" d="M14 62a48 48 0 0 1 48-48" fill="none"/></defs>
          <circle cx="62" cy="62" r="48" fill="#1C6FB5"/>
          <path d="M40 63l16 16 30-33" fill="none" stroke="#FFFFFF" stroke-width="13"
                stroke-linecap="round" stroke-linejoin="round"/>
          <text font-family="Arial, Helvetica, sans-serif" font-size="11.5"
                font-weight="700" fill="#FFFFFF" letter-spacing="1.1">
            <textPath href="#bctArc" startOffset="4%">ONLINE.GOV.VN</textPath>
          </text>
          <rect x="120" y="12" width="236" height="96" rx="5" fill="#1C7FC4"/>
          <text x="238" y="55" text-anchor="middle" fill="#FFFFFF"
                font-family="Arial, Helvetica, sans-serif" font-weight="700"
                font-size="31" letter-spacing=".5">ĐÃ THÔNG BÁO</text>
          <text x="238" y="88" text-anchor="middle" fill="#FFFFFF"
                font-family="Arial, Helvetica, sans-serif" font-weight="700"
                font-size="21" letter-spacing=".5">BỘ CÔNG THƯƠNG</text>
        </svg>
      </a>
'''

rep('''    <div class="colophon">
      <span data-vi="© 2026 Asiana Gold. Bản dựng lại giao diện — chưa phải trang chính thức."
            data-en="© 2026 Asiana Gold. Interface redesign study — not the live site."></span>''',
    '''    <div class="colophon">
''' + BADGE + '''      <span data-vi="© 2026 Asiana Gold. Bản dựng lại giao diện — chưa phải trang chính thức."
            data-en="© 2026 Asiana Gold. Interface redesign study — not the live site."></span>''')

rep('.colophon{margin-top:38px;padding-top:20px;border-top:1px solid rgba(255,255,255,.1);font-size:.78rem;\n  display:flex;gap:18px;flex-wrap:wrap;justify-content:space-between;color:#8E7F66}',
    '.colophon{margin-top:38px;padding-top:20px;border-top:1px solid rgba(255,255,255,.1);font-size:.78rem;\n'
    '  display:flex;gap:18px 24px;flex-wrap:wrap;align-items:center;justify-content:space-between;color:#8E7F66}\n'
    '.bct{display:block;flex-shrink:0;width:168px;transition:opacity .18s}\n'
    '.bct:hover{opacity:.82}\n'
    '.bct svg{width:100%;height:auto;display:block}\n'
    '@media(max-width:640px){.bct{width:148px}}')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('edits %d\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
