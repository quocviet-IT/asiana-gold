import zipfile, json, os, sys
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
BS = chr(92)


def rels(z, path):
    d = os.path.dirname(path)
    b = os.path.basename(path)
    rp = d + '/_rels/' + b + '.rels'
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


def scan(xlsx, tag):
    z = zipfile.ZipFile(xlsx)
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wbrels = rels(z, 'xl/workbook.xml')
    sheets = []
    for s in wb.findall('m:sheets/m:sheet', NS):
        rid = s.get('{%s}id' % NS['r'])
        tgt = wbrels.get(rid, (None, None))[0]
        if tgt:
            sheets.append((s.get('name'), norm('xl/workbook.xml', tgt)))

    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
            sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))

    records = []
    for name, spath in sheets:
        srels = rels(z, spath)
        drawing = None
        for rid, (tgt, typ) in srels.items():
            if typ == 'drawing':
                drawing = norm(spath, tgt)
        if not drawing or drawing not in z.namelist():
            continue

        cells = {}
        try:
            root = ET.fromstring(z.read(spath))
            for c in root.iter('{%s}c' % NS['m']):
                ref = c.get('r')
                t = c.get('t')
                v = c.find('m:v', NS)
                isx = c.find('m:is', NS)
                val = None
                if t == 's' and v is not None and v.text is not None:
                    i = int(v.text)
                    val = sst[i] if i < len(sst) else None
                elif isx is not None:
                    val = ''.join(x.text or '' for x in isx.iter('{%s}t' % NS['m']))
                elif v is not None:
                    val = v.text
                if val and str(val).strip():
                    cells[ref] = ' '.join(str(val).split())
        except Exception:
            pass

        drels = rels(z, drawing)
        droot = ET.fromstring(z.read(drawing))
        for anch in list(droot):
            frm = anch.find('xdr:from', NS)
            if frm is None:
                continue
            fc = int(frm.find('xdr:col', NS).text)
            fr = int(frm.find('xdr:row', NS).text)
            to = anch.find('xdr:to', NS)
            tc = int(to.find('xdr:col', NS).text) if to is not None else fc
            tr = int(to.find('xdr:row', NS).text) if to is not None else fr
            blip = anch.find('.//a:blip', NS)
            if blip is None:
                continue
            rid = blip.get('{%s}embed' % NS['r'])
            tgt = drels.get(rid, (None, None))[0]
            if not tgt:
                continue
            media = norm(drawing, tgt)
            near = []
            for rr in range(fr + 1, tr + 6):
                for cc in range(max(0, fc - 1), tc + 2):
                    ref = col_letters(cc) + str(rr)
                    if ref in cells and cells[ref] not in near:
                        near.append(cells[ref])
            above = []
            for rr in range(max(1, fr - 3), fr + 1):
                for cc in range(max(0, fc - 1), tc + 2):
                    ref = col_letters(cc) + str(rr)
                    if ref in cells and cells[ref] not in above:
                        above.append(cells[ref])
            records.append(dict(file=tag, sheet=name, row=fr + 1, col=fc + 1,
                                media=media, above=above[-4:], near=near[:6]))
    return records


out = []
for path, tag in [(sys.argv[1], 'M2_1.0'), (sys.argv[2], 'AG_2.0')]:
    recs = scan(path, tag)
    out.extend(recs)
    sys.stderr.write(tag + ': ' + str(len(recs)) + ' anchored images\n')
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sys.stderr.write('TOTAL ' + str(len(out)) + '\n')
