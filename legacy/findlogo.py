import zipfile, io, os, sys, hashlib
from PIL import Image

SP = os.path.dirname(os.path.abspath(__file__))
cands = []
for path, tag in [(sys.argv[1], 'A'), (sys.argv[2], 'B')]:
    z = zipfile.ZipFile(path)
    for n in z.namelist():
        if not n.startswith('xl/media/'):
            continue
        raw = z.read(n)
        try:
            im = Image.open(io.BytesIO(raw))
            w, h = im.size
        except Exception:
            continue
        ar = w / h if h else 0
        # a wordmark is wide and short; product shots here are square-ish or tall
        if ar >= 1.7 and w >= 300:
            cands.append((tag, n, w, h, round(ar, 2), len(raw), hashlib.md5(raw).hexdigest()[:8], raw))

seen = set()
uniq = []
for c in cands:
    if c[6] in seen:
        continue
    seen.add(c[6])
    uniq.append(c)
uniq.sort(key=lambda c: -c[4])
sys.stderr.write('wide candidates: %d unique of %d\n' % (len(uniq), len(cands)))
for i, c in enumerate(uniq[:14]):
    p = os.path.join(SP, 'cand%02d.png' % i)
    open(p, 'wb').write(c[7])
    sys.stderr.write('  cand%02d  %s %-22s %4dx%-4d ar=%.2f  %6d B\n' % (i, c[0], c[1].split('/')[-1], c[2], c[3], c[4], c[5]))
