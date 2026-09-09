import zipfile, json, os, sys, re
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
BS = chr(92)
SP = os.path.dirname(os.path.abspath(__file__))


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
sst = []
if 'xl/sharedStrings.xml' in z.namelist():
    for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
        sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))

wb = ET.fromstring(z.read('xl/workbook.xml'))
wbrels = rels(z, 'xl/workbook.xml')
want = sys.argv[2]
rows = {}
for s in wb.findall('m:sheets/m:sheet', NS):
    if want not in s.get('name'):
        continue
    spath = norm('xl/workbook.xml', wbrels[s.get('{%s}id' % NS['r'])][0])
    for row in ET.fromstring(z.read(spath)).iter('{%s}row' % NS['m']):
        rn = int(row.get('r'))
        vals = {}
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
                vals[col] = ' '.join(str(val).split())
        if vals:
            rows[rn] = vals
    break

groups = []
cur = None
for rn in sorted(rows):
    v = rows[rn]
    a = v.get('A', '')
    b = v.get('B', '')
    if a and re.match(r'^\d+[.)]', a):
        cur = dict(title=re.sub(r'^\d+[.)]\s*', '', a), rows=[])
        groups.append(cur)
        continue
    if cur is not None and b and re.match(r'^[A-Z]{2}\d', b):
        def num(x):
            try:
                return round(float(x), 3)
            except Exception:
                return None
        cur['rows'].append(dict(y=b, w=v.get('C', ''),
                                c750=num(v.get('D')), g750=num(v.get('E')),
                                c610=num(v.get('F')), g610=num(v.get('G')),
                                length=v.get('H', '')))

groups = [g for g in groups if g['rows']]
json.dump(groups, open(os.path.join(SP, 'specs.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sys.stderr.write('GROUPS %d\n' % len(groups))
for g in groups[:14]:
    sys.stderr.write('  %-46s %d sizes  e.g. %s %s g / %s cm\n' % (
        g['title'][:46], len(g['rows']), g['rows'][0]['y'], g['rows'][0]['g750'], g['rows'][0]['length']))
