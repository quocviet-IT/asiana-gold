import zipfile, json, os, sys
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
BS = chr(92)


def rels(z, path):
    rp = os.path.dirname(path) + '/_rels/' + os.path.basename(path) + '.rels'
    out = {}
    if rp in z.namelist():
        for rel in ET.fromstring(z.read(rp)).findall('pr:Relationship', NS):
            out[rel.get('Id')] = (rel.get('Target'), rel.get('Type').rsplit('/', 1)[-1])
    return out


def norm(base, target):
    if target.startswith('/'):
        return target.lstrip('/')
    return os.path.normpath(os.path.join(os.path.dirname(base), target)).replace(BS, '/')


def col_letters(n):
    s = ''
    while n >= 0:
        s = chr(n % 26 + 65) + s
        n = n // 26 - 1
    return s


def load(xlsx, want):
    z = zipfile.ZipFile(xlsx)
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wbrels = rels(z, 'xl/workbook.xml')
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
            sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    for s in wb.findall('m:sheets/m:sheet', NS):
        name = s.get('name')
        if want not in name:
            continue
        spath = norm('xl/workbook.xml', wbrels[s.get('{%s}id' % NS['r'])][0])
        cells = {}
        root = ET.fromstring(z.read(spath))
        for c in root.iter('{%s}c' % NS['m']):
            ref, t = c.get('r'), c.get('t')
            v, isx = c.find('m:v', NS), c.find('m:is', NS)
            val = None
            if t == 's' and v is not None and v.text is not None:
                i = int(v.text)
                val = sst[i] if i < len(sst) else None
            elif isx is not None:
                val = ''.join(x.text or '' for x in isx.iter('{%s}t' % NS['m']))
            elif v is not None:
                val = v.text
            if val and str(val).strip():
                cells[ref] = str(val).strip()
        drawing = None
        for rid, (tgt, typ) in rels(z, spath).items():
            if typ == 'drawing':
                drawing = norm(spath, tgt)
        imgs = []
        if drawing and drawing in z.namelist():
            drels = rels(z, drawing)
            for anch in list(ET.fromstring(z.read(drawing))):
                frm = anch.find('xdr:from', NS)
                blip = anch.find('.//a:blip', NS)
                if frm is None or blip is None:
                    continue
                tgt = drels.get(blip.get('{%s}embed' % NS['r']), (None,))[0]
                if not tgt:
                    continue
                imgs.append(dict(row=int(frm.find('xdr:row', NS).text) + 1,
                                 col=int(frm.find('xdr:col', NS).text) + 1,
                                 media=norm(drawing, tgt)))
        return z, name, cells, imgs
    return None, None, {}, []


z, name, cells, imgs = load(sys.argv[1], sys.argv[2])
sys.stderr.write('SHEET: ' + str(name) + '  cells=' + str(len(cells)) + '  imgs=' + str(len(imgs)) + '\n')
imgs.sort(key=lambda x: (x['row'], x['col']))
for im in imgs[:14]:
    print('IMG r%d c%s %s' % (im['row'], col_letters(im['col'] - 1), im['media'].split('/')[-1]))
    for d in range(-4, 7):
        ref = col_letters(im['col'] - 1) + str(im['row'] + d)
        if ref in cells:
            print('    %+d %-5s %s' % (d, ref, ' | '.join(cells[ref].split(chr(10)))[:110]))
    print()
