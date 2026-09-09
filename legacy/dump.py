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
want = sys.argv[2]
first, last = int(sys.argv[3]), int(sys.argv[4])
sst = []
if 'xl/sharedStrings.xml' in z.namelist():
    for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
        sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
wb = ET.fromstring(z.read('xl/workbook.xml'))
wbrels = rels(z, 'xl/workbook.xml')
for sh in wb.findall('m:sheets/m:sheet', NS):
    if want not in sh.get('name'):
        continue
    spath = norm('xl/workbook.xml', wbrels[sh.get('{%s}id' % NS['r'])][0])
    sys.stderr.write('SHEET: ' + sh.get('name') + '\n')
    for row in ET.fromstring(z.read(spath)).iter('{%s}row' % NS['m']):
        rn = int(row.get('r'))
        if rn < first or rn > last:
            continue
        cells = []
        for c in row.findall('m:c', NS):
            ref, t = c.get('r'), c.get('t')
            col = re.match(r'([A-Z]+)', ref).group(1)
            v, isx = c.find('m:v', NS), c.find('m:is', NS)
            val = None
            if t == 's' and v is not None and v.text is not None:
                i = int(v.text)
                val = sst[i] if i < len(sst) else None
            elif isx is not None:
                val = ''.join(x.text or '' for x in isx.iter('{%s}t' % NS['m']))
            elif v is not None:
                val = v.text
            if val is not None and str(val).strip():
                s = ' '.join(str(val).split())
                cells.append(col + '=' + (s[:26]))
        if cells:
            print('%4d  %s' % (rn, '  '.join(cells)))
    break
