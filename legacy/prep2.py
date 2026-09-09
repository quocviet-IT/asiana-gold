"""Swap the new OFFICIAL size table and the availability map into the payload,
keeping the products and their photo galleries untouched."""
import json, os, sys

SP = os.path.dirname(os.path.abspath(__file__))
pay = json.load(open(os.path.join(SP, 'payload.json'), encoding='utf-8'))
specs = json.load(open(os.path.join(SP, 'specs.json'), encoding='utf-8'))
avail = json.load(open(os.path.join(SP, 'avail.json'), encoding='utf-8'))
prods = pay['products']

old_rows = sum(len(g['rows']) for g in pay.get('specs', []))

by_code, by_title = {}, {}
for g in specs:
    by_title.setdefault(g['title'].strip().lower(), g)
    for r in g['rows']:
        by_code.setdefault(r['y'].strip().upper(), g)

lost, matched_code, matched_title, unmatched = [], 0, 0, []
for p in prods:
    g = by_code.get(p['ag'].upper())
    if g:
        matched_code += 1
    else:
        g = by_title.get(p['vi'].strip().lower())
        if g:
            matched_title += 1
    p['spec'] = g
    p['avail'] = avail.get(p['ag'].upper())
    if g and not any(r['y'].strip().upper() == p['ag'].upper() for r in g['rows']):
        lost.append((p['ag'], g['title'], g['rows'][0]['y']))
    if not g:
        unmatched.append(p['ag'])

pay['specs'] = specs
pay['avail'] = avail
json.dump(pay, open(os.path.join(SP, 'payload.json'), 'w', encoding='utf-8'), ensure_ascii=False)

canmake = sum(1 for p in prods if p.get('avail') and p['avail']['can'])
withav = sum(1 for p in prods if p.get('avail'))
sys.stderr.write('spec groups %d, rows %d (was %d)\n' % (len(specs), sum(len(g['rows']) for g in specs), old_rows))
sys.stderr.write('products with a spec group: %d (by code %d, by title %d)\n'
                 % (matched_code + matched_title, matched_code, matched_title))
sys.stderr.write('products with availability data: %d, of which orderable now: %d\n' % (withav, canmake))
sys.stderr.write('products whose own code is no longer a row in the new table: %d\n' % len(lost))
for a, t, first in lost[:12]:
    sys.stderr.write('   %-10s %-34s bảng bắt đầu từ %s\n' % (a, t[:34], first))
sys.stderr.write('products with no spec group at all: %d\n' % len(unmatched))
sys.stderr.write('payload %.2f MB\n' % (os.path.getsize(os.path.join(SP, 'payload.json')) / 1048576))
