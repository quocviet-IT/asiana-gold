# -*- coding: utf-8 -*-
"""Inject the payload into the shell and lay the result down at every target.

The loose single-file copy has no img/ folder beside it, so its image paths are
rewritten to the deployed origin; the two site folders keep root-relative paths."""
import os, sys, io, json

SP = os.path.dirname(os.path.abspath(__file__))
TOKEN = '/*__PAYLOAD__*/{products:[],specs:[]}'
# asiana-gold-preview-site.vercel.app now 307s to asiana-gold.com, whose DNS still
# points at Google Sites, so images fetched through it would 404. Use the alias
# that actually serves the deployment.
CDN = 'https://asiana-gold-preview-site-ecru.vercel.app/img/'

shell = io.open(os.path.join(SP, 'shell.html'), encoding='utf-8').read()
payload = json.dumps(json.load(io.open(os.path.join(SP, 'payload.json'), encoding='utf-8')),
                     ensure_ascii=False, separators=(',', ':'))
assert TOKEN in shell, 'payload token missing'
html = shell.replace(TOKEN, payload, 1)

targets = [
    (os.path.join(SP, 'asiana-gold.html'), False),
    (r'C:\Users\pit010\asiana-gold-preview-site\index.html', False),
    (r'C:\Users\pit010\asiana-gold-preview\index.html', False),
    (r'C:\Users\pit010\asiana-gold-redesign.html', True),
]
for path, absolute in targets:
    out = html.replace('"/img/', '"' + CDN) if absolute else html
    io.open(path, 'w', encoding='utf-8', newline='').write(out)
    sys.stderr.write('%-52s %.0f KB\n' % (os.path.basename(path), os.path.getsize(path) / 1024))
sys.stderr.write('img paths root-relative: %d\n' % html.count('"/img/'))
