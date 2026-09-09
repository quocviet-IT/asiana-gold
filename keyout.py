"""Key the white studio background out of a chain shot so it can sit on a dark hero.
Gold is warm and saturated; the sweep background is bright and neutral. Combining a
luminance ramp with a saturation floor keeps thin, pale chain links that a plain
threshold would eat. PIL only — no numpy on this machine."""
import json, os, sys, io, base64
from PIL import Image, ImageChops, ImageFilter

SP = os.path.dirname(os.path.abspath(__file__))


def key_out(im, lo=188, hi=250, sat_floor=15, sat_gain=13.0):
    im = im.convert('RGB')
    r, g, b = im.split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mn = ImageChops.darker(ImageChops.darker(r, g), b)
    sat = ImageChops.subtract(mx, mn)                 # 0 on neutral background
    lum = im.convert('L')
    span = float(hi - lo)
    a_lum = lum.point(lambda v: 255 if v <= lo else (0 if v >= hi else int(255 * (hi - v) / span)))
    a_sat = sat.point(lambda v: 0 if v < sat_floor else min(255, int((v - sat_floor) * sat_gain)))
    alpha = ImageChops.lighter(a_lum, a_sat)
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.7))
    alpha = alpha.point(lambda v: 0 if v < 26 else v)  # kill specular haze off the sweep
    return Image.merge('RGBA', (r, g, b, alpha))


def cut_uri(uri, box=900):
    im = Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1])))
    im.thumbnail((box, box), Image.LANCZOS)
    return key_out(im)


if __name__ == '__main__':
    prods = json.load(open(os.path.join(SP, 'payload.json'), encoding='utf-8'))['products']
    codes = sys.argv[1:] or ['CY25SR']
    tiles = []
    for c in codes:
        p = next((x for x in prods if x['ag'] == c), None)
        if not p:
            sys.stderr.write('no ' + c + '\n')
            continue
        t = cut_uri(p['img'])
        t.thumbnail((400, 400), Image.LANCZOS)
        tiles.append((c, t))
    H = max(t.height for _, t in tiles) + 32
    W = sum(t.width for _, t in tiles) + 16 * (len(tiles) + 1)
    sheet = Image.new('RGB', (W, H), (26, 20, 9))      # the real hero ground
    x = 16
    for c, t in tiles:
        sheet.paste(t, (x, 16), t)
        x += t.width + 16
    sheet.save(os.path.join(SP, 'keyout-proof.jpg'), quality=92)
    print('proof:', ', '.join(c for c, _ in tiles))
