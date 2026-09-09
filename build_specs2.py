"""Rebuild the size table from '2.1A) AG 2.0-OFFICIAL' (the fuller sheet) and
join production availability + MOQ from '2B) AG 2.0-AVAILABLE' by 18KY code.

OFFICIAL columns : A group | B 18KY | C 18KW | D silver-gilt | E silver
                   F chỉ750 | G g750 | H chỉ610 | I g610
                   L actual-750 | M actual-610 | N length | P marketing note
AVAILABLE columns: B 18KY | J can-make 0/1 | K MOQ (unit named in its header)
"""
import zipfile, json, os, sys, re
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
BS = chr(92)
SP = os.path.dirname(os.path.abspath(__file__))


def rels(z, p):
    rp = os.path.dirname(p) + '/_rels/' + os.path.basename(p) + '.rels'
    o = {}
    if rp in z.namelist():
        for r in ET.fromstring(z.read(rp)).findall('pr:Relationship', NS):
            o[r.get('Id')] = (r.get('Target'), r.get('Type').rsplit('/', 1)[-1])
    return o


def norm(b, t):
    if t.startswith('/'):
        return t.lstrip('/')
    return os.path.normpath(os.path.join(os.path.dirname(b), t)).replace(BS, '/')


def load(path):
    z = zipfile.ZipFile(path)
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
            sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wr = rels(z, 'xl/workbook.xml')
    return z, sst, wb, wr


def rows_of(z, sst, wb, wr, want):
    for sh in wb.findall('m:sheets/m:sheet', NS):
        if want not in sh.get('name'):
            continue
        sp = norm('xl/workbook.xml', wr[sh.get('{%s}id' % NS['r'])][0])
        out = {}
        for row in ET.fromstring(z.read(sp)).iter('{%s}row' % NS['m']):
            d = {}
            for c in row.findall('m:c', NS):
                col = re.match(r'([A-Z]+)', c.get('r')).group(1)
                t = c.get('t')
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
                    d[col] = ' '.join(str(val).split())
            if d:
                out[int(row.get('r'))] = d
        return sh.get('name'), out
    return None, {}


def num(x):
    try:
        return round(float(x), 3)
    except Exception:
        return None


src = sys.argv[1]
z, sst, wb, wr = load(src)

# ---- availability + MOQ, keyed by 18KY code ---------------------------------
_, av = rows_of(z, sst, wb, wr, 'AG 2.0-AVAILABLE')
avail, unit = {}, 'sợi'
for rn in sorted(av):
    d = av[rn]
    k = d.get('K', '')
    m = re.search(r'ĐVT:\s*([^)]+)\)', k)
    if m:
        unit = m.group(1).strip()
        continue
    code = d.get('B', '')
    if re.match(r'^[A-Z]{2}[A-Z0-9.\-]+$', code):
        avail[code.upper()] = {
            'can': d.get('J') == '1',
            'moq': num(d.get('K')),
            'unit': unit,
        }

# ---- the fuller size table ---------------------------------------------------
_, off = rows_of(z, sst, wb, wr, 'AG 2.0-OFFICIAL')
groups, cur = [], None
for rn in sorted(off):
    d = off[rn]
    a = d.get('A', '')
    if a and re.match(r'^\d+[.)]', a):
        cur = {'title': re.sub(r'^\d+[.)]\s*', '', a).strip(), 'rows': []}
        groups.append(cur)
        continue
    b = d.get('B', '')
    if cur is None or not re.match(r'^[A-Z]{2}\d', b):
        continue
    key = b.upper()
    a_ = avail.get(key, {})
    cur['rows'].append({
        'y': b, 'w': d.get('C', ''),
        'sv': d.get('D', ''), 'svw': d.get('E', ''),
        'c750': num(d.get('F')), 'g750': num(d.get('G')),
        'c610': num(d.get('H')), 'g610': num(d.get('I')),
        'real750': num(d.get('L')), 'real610': num(d.get('M')),
        'length': d.get('N', ''),
        'note': d.get('P', ''),
        'can': a_.get('can'), 'moq': a_.get('moq'), 'unit': a_.get('unit'),
    })

groups = [g for g in groups if g['rows']]
json.dump(groups, open(os.path.join(SP, 'specs.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
json.dump(avail, open(os.path.join(SP, 'avail.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

total = sum(len(g['rows']) for g in groups)
known = sum(1 for g in groups for r in g['rows'] if r['can'] is not None)
canmake = sum(1 for g in groups for r in g['rows'] if r['can'])
withmoq = sum(1 for g in groups for r in g['rows'] if r['moq'])
silver = sum(1 for g in groups for r in g['rows'] if r['sv'])
sys.stderr.write('groups %d   rows %d\n' % (len(groups), total))
sys.stderr.write('  availability known %d, of which can-make %d\n' % (known, canmake))
sys.stderr.write('  rows with MOQ %d, rows with a silver code %d\n' % (withmoq, silver))
for g in groups[:16]:
    r = g['rows'][0]
    sys.stderr.write('  %-40s %2d cỡ  %-9s %s\n' % (g['title'][:40], len(g['rows']), r['y'], r['length']))
