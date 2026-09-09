import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n = 0


def rep(old, new):
    global s, n
    if old not in s:
        sys.stderr.write('!! NOT FOUND: ' + old[:100].replace('\n', ' ') + '\n')
        return
    s = s.replace(old, new, 1)
    n += 1


# ---- gradient stops as tokens, so the mark re-tunes itself per surface ----
rep('  --focus:#8C6A1E; --maxw:1240px;\n}',
    '  --focus:#8C6A1E; --maxw:1240px;\n'
    '  /* the mark\'s own gold ramp — pale at the left, bronze at the right */\n'
    '  --lg1:#EFDFB0; --lg2:#DCC176; --lg3:#C9A44A; --lg4:#AC8630; --lg5:#8B6A20; --lg6:#75581A;\n}')

for anchor in ['    --shadow-l:0 8px 22px rgba(0,0,0,.6), 0 44px 88px -40px rgba(0,0,0,1);\n    --focus:#E3C982;\n  }',
               '  --shadow-l:0 8px 22px rgba(0,0,0,.6), 0 44px 88px -40px rgba(0,0,0,1);\n  --focus:#E3C982;\n}']:
    bright = ('  --lg1:#F7EBC9; --lg2:#E9D294; --lg3:#DCBB6A; --lg4:#CBA750; --lg5:#B8913A; --lg6:#A57F2E;\n')
    if anchor.startswith('    '):
        rep(anchor, anchor[:-len('  }')] + bright.replace('  --lg', '    --lg') + '  }')
    else:
        rep(anchor, anchor[:-1] + bright + '}')

rep('.logo{display:block;height:auto;color:var(--ink)}\n'
    '.logo.on-dark{color:var(--onDark)}',
    '.logo{display:block;height:auto}\n'
    '/* on an espresso ground the ramp has to sit brighter to stay legible */\n'
    '.logo.on-dark{--lg1:#FBF3DC;--lg2:#F0DDA9;--lg3:#E3C87F;--lg4:#D5B463;--lg5:#C3A04C;--lg6:#B08C3C}')

# ---- the mark itself, redrawn to the artwork\'s proportions ----
old_logo = re.search(r'function logoSVG\(cls,w\)\{.*?\n\}\n', s, re.S)
if not old_logo:
    sys.stderr.write('!! logoSVG not found\n')
    sys.exit(1)

new_logo = '''function logoSVG(cls,w){
  const id = "ag-" + (logoSVG.k = (logoSVG.k||0)+1);
  return `<svg class="logo ${cls||""}" width="${w||180}" viewBox="0 0 600 220"
      role="img" aria-label="Asiana Gold — Pure Gold Chain">
    <defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="0.42">
      <stop offset="0" stop-color="var(--lg1)"/><stop offset=".2" stop-color="var(--lg2)"/>
      <stop offset=".42" stop-color="var(--lg3)"/><stop offset=".64" stop-color="var(--lg4)"/>
      <stop offset=".84" stop-color="var(--lg5)"/><stop offset="1" stop-color="var(--lg6)"/>
    </linearGradient></defs>
    <g stroke="url(#${id})" stroke-width="4.5" fill="none">
      <path d="M20 58H236"/><path d="M364 58H580"/>
      <path d="M20 58V185"/><path d="M580 58V185"/>
      <path d="M20 185H172"/><path d="M428 185H580"/>
    </g>
    <g fill="none" stroke="url(#${id})" stroke-width="11">
      <rect x="247" y="35.5" width="57" height="45" rx="11"/>
      <rect x="296" y="35.5" width="57" height="45" rx="11"/>
    </g>
    <text x="300" y="155" text-anchor="middle" fill="url(#${id})"
      font-family="Archivo, 'Arial Black', 'Helvetica Neue', sans-serif"
      font-weight="900" font-style="italic" font-size="80" letter-spacing="-1">Asiana Gold</text>
    <text x="300" y="192" text-anchor="middle" fill="url(#${id})"
      font-family="Arial, 'Helvetica Neue', Helvetica, sans-serif"
      font-weight="400" font-size="19" letter-spacing="4.2">PURE GOLD CHAIN</text>
  </svg>`;
}
'''
s = s[:old_logo.start()] + new_logo + s[old_logo.end():]
n += 1

# the ornament divider should carry the same ramp
rep('const LINKMARK = `<svg width="30" height="14" viewBox="0 0 160 60" fill="none" stroke="currentColor" stroke-width="11" aria-hidden="true">\n'
    '  <rect x="8" y="8" width="76" height="44" rx="12"/><rect x="76" y="8" width="76" height="44" rx="12"/></svg>`;',
    'const LINKMARK = `<svg width="34" height="15" viewBox="0 0 168 60" fill="none" stroke="currentColor" stroke-width="10" aria-hidden="true">\n'
    '  <rect x="7" y="8" width="78" height="44" rx="12"/><rect x="83" y="8" width="78" height="44" rx="12"/></svg>`;')

# footer sits on espresso in both themes
rep('$("#foot-logo").innerHTML = logoSVG("on-dark",190);',
    '$("#foot-logo").innerHTML = logoSVG("on-dark",200);')
rep('$("#hdr-logo").innerHTML = logoSVG("",170);',
    '$("#hdr-logo").innerHTML = logoSVG("",180);')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('applied %d edits\n' % n)
sys.stderr.write('currentColor left in logo: %d\n' % len(re.findall(r'logoSVG[\s\S]{0,900}?currentColor', s)))
