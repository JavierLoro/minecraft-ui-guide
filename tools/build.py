from pathlib import Path
from html import escape
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
source = (ROOT / 'GUIA-INTERFACES-MINECRAFT.md').read_text(encoding='utf-8')
template = (ROOT / 'source/template.html').read_text(encoding='utf-8')
md = MarkdownIt('commonmark', {'html': False}).enable('table')
parts = source.split('\n## ')
chapters = []
for i, part in enumerate(parts[1:], 1):
    title, _, body = part.partition('\n')
    chapters.append(f'<details class="chapter" id="cap-{i}"><summary>{escape(title)}</summary><div class="chapter-body">{md.render(body)}</div></details>')
html = template.replace('<!--REFERENCE-->', '\n'.join(chapters))
html = html.replace('<!--SOURCE_INTRO-->', md.render(parts[0].partition('\n')[2]))
html = html.replace('29 capítulos', f'{len(chapters)} capítulos')
installation = (ROOT / 'demo/INSTALACION.md').read_text(encoding='utf-8')
assert '<!--SERVER_INSTALL-->' in html, 'Falta el bloque de instalación'
html = html.replace('<!--SERVER_INSTALL-->', md.render(installation.partition('\n')[2]))
(ROOT / 'index.html').write_text(html, encoding='utf-8')
(ROOT / 'llms-full.txt').write_text(source, encoding='utf-8')
print(f'Generados index.html y llms-full.txt: {len(chapters)} capítulos.')
