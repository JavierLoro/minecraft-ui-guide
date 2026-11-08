from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parent.parent

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('script', 'img') and 'src' in attrs:
            self.links.append(attrs['src'])

html = (ROOT / 'index.html').read_text(encoding='utf-8')
parser = Inspector()
parser.feed(html)
assert len(parser.ids) == len(set(parser.ids)), 'IDs duplicados'
for link in parser.links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        continue
    assert not url.path.startswith('/'), f'Enlace incompatible con un subdirectorio: {link}'
    if url.path:
        assert (ROOT / unquote(url.path)).is_file(), f'Archivo no encontrado: {link}'
    elif url.fragment:
        assert unquote(url.fragment) in parser.ids, f'Ancla no encontrada: {link}'
guide = (ROOT / 'GUIA-INTERFACES-MINECRAFT.md').read_text(encoding='utf-8')
assert (ROOT / 'llms-full.txt').read_text(encoding='utf-8') == guide, 'Texto de agentes desactualizado'
assert html.count('class="chapter"') == len(re.findall(r'^## ', guide, re.M))
assert (ROOT / '.nojekyll').is_file()
for name in ('index.html', 'AGENTS.md', 'llms.txt', 'llms-full.txt', 'GUIA-INTERFACES-MINECRAFT.md'):
    text = (ROOT / name).read_text(encoding='utf-8')
    assert 'C:\\Users\\' not in text and 'C:/Users/' not in text, f'Ruta personal en {name}'
    assert 'IndustrialMC' not in text, f'Referencia a servidor concreto en {name}'
print(f'Correcto: {len(parser.links)} enlaces HTML, Markdown sincronizado y paquete independiente.')
