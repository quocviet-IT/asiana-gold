"""List every sheet in a workbook with how much it holds, so an updated tab
is visible without opening Excel."""
import zipfile, os, sys, re
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
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


z = zipfile.ZipFile(sys.argv[1])
sizes = {i.filename: i.file_size for i in z.infolist()}
wb = ET.fromstring(z.read('xl/workbook.xml'))
wbrels = rels(z, 'xl/workbook.xml')
rows = []
for sh in wb.findall('m:sheets/m:sheet', NS):
    tgt = wbrels.get(sh.get('{%s}id' % NS['r']), (None,))[0]
    if not tgt:
        continue
    spath = norm('xl/workbook.xml', tgt)
    if spath not in z.namelist():
        continue
    xml = z.read(spath)
    ncells = xml.count(b'<c ')
    drawing, nimg = None, 0
    for _, (t2, typ) in rels(z, spath).items():
        if typ == 'drawing':
            drawing = norm(spath, t2)
    if drawing and drawing in z.namelist():
        nimg = z.read(drawing).count(b'<a:blip')
    rows.append((sh.get('name'), sizes.get(spath, 0), ncells, nimg))

print('%-34s %10s %8s %6s' % ('SHEET', 'BYTES', 'CELLS', 'IMGS'))
for name, b, c, i in rows:
    print('%-34s %10d %8d %6d' % (name[:34], b, c, i))
print('total sheets:', len(rows))
