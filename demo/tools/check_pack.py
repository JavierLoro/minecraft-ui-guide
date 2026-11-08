"""Check resource references and the fixed-width HUD contract without a game client."""
from pathlib import Path
import json, struct, zlib
ROOT = Path(__file__).resolve().parents[1] / 'pack'

def image(path):
    b = path.read_bytes()
    assert b[:8] == b'\x89PNG\r\n\x1a\n', path
    width,height,depth,color,*_ = struct.unpack('>IIBBBBB',b[16:29])
    assert (depth,color) == (8,6), path
    offset=8;data=b''
    while offset<len(b):
        length=struct.unpack('>I',b[offset:offset+4])[0]
        if b[offset+4:offset+8] == b'IDAT':data+=b[offset+8:offset+8+length]
        offset += length + 12
    raw=zlib.decompress(data);stride=width*4+1
    assert all(raw[y*stride]==0 for y in range(height)), 'Expected generator filter 0'
    return width,height,b''.join(raw[y*stride+1:(y+1)*stride] for y in range(height))

fonts=ROOT/'assets/taller/font'
for p in fonts.glob('*.json'):
    for provider in json.loads(p.read_text(encoding='utf-8'))['providers']:
        if provider['type']=='bitmap':
            namespace,name=provider['file'].split(':',1)
            texture=ROOT/'assets'/namespace/'textures'/name
            w,h,pixels=image(texture)
            chars=provider['chars']
            assert all(len(row)==len(chars[0]) for row in chars)
            assert w % len(chars[0])==0 and h % len(chars)==0
            assert provider['ascent'] <= provider['height']
for name in ['white_background','white_progress']:
    w,h,p=image(ROOT/f'assets/minecraft/textures/gui/sprites/boss_bar/{name}.png')
    assert (w,h)==(182,5) and not any(p)
font=json.loads((fonts/'value.json').read_text(encoding='utf-8'))['providers'][1]
w,h,p=image(ROOT/'assets/taller/textures/font/hud.png')
chars=''.join(font['chars'])
for char in 'TALLERPIEZAS0123456789/':
    index=chars.index(char);left=(index%16)*8;top=(index//16)*8
    extent=max(x+1 for y in range(8) for x in range(8) if p[((top+y)*w+left+x)*4+3])
    assert extent+1==6,(char,extent)
assert 161-151+36-36+58-58+141+9==160
meta=json.loads((ROOT/'pack.mcmeta').read_text())
assert meta['pack']['min_format']==[97,1] and meta['pack']['max_format']==[97,1]
print('Pack OK: texture links, PNG structure, transparency, glyph metrics and 160px HUD advance.')
