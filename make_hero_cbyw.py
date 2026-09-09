# -*- coding: utf-8 -*-
"""Turn the two-tone bead photo the customer supplied into the third hero cut.

The file already carries a clean alpha channel, so no keying is needed — only a
crop to the pixels that actually contain chain, and a WebP encode small enough
to stay inline in the payload."""
import io, base64, json, os, sys
from PIL import Image

SP = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(SP, 'pasted_cby3.png')).convert('RGBA')
box = im.split()[-1].getbbox()
im = im.crop(box)
sys.stderr.write('cropped to %s\n' % (im.size,))

for side, q in ((900, 82), (820, 80), (740, 78)):
    t = im.copy()
    t.thumbnail((side, side), Image.LANCZOS)
    buf = io.BytesIO()
    t.save(buf, 'WEBP', quality=q, method=6)
    raw = buf.getvalue()
    sys.stderr.write('  %dpx q%d -> %s  %.0f KB\n' % (side, q, t.size, len(raw) / 1024))
    if len(raw) < 92000:
        break

uri = 'data:image/webp;base64,' + base64.b64encode(raw).decode()
pj = os.path.join(SP, 'payload.json')
pay = json.load(open(pj, encoding='utf-8'))
pay['heroCuts'].pop('CBY3', None)
pay['heroCuts']['CBYW2.5'] = uri
json.dump(pay, open(pj, 'w', encoding='utf-8'), ensure_ascii=False)
sys.stderr.write('heroCuts: %s\n' % list(pay['heroCuts']))

# proof tile on the real hero ground
d = Image.new('RGB', t.size, (26, 20, 9))
d.paste(t, (0, 0), t)
d.save(os.path.join(SP, 'hero-cbyw-proof.jpg'), quality=90)
