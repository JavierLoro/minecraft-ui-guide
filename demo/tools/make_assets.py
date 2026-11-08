"""Build the demo's original, deterministic pixel assets using only Python's stdlib."""
from pathlib import Path
import json, struct, zlib
ROOT = Path(__file__).resolve().parents[1] / 'pack' / 'assets'

def png(path, width, height, pixels):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    raw = b''.join(b'\0' + bytes(pixels[y * width * 4:(y + 1) * width * 4]) for y in range(height))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
                    + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

def canvas(width, height): return bytearray(width * height * 4)
def rect(pixels, width, x, y, w, h, color):
    for py in range(y, y + h):
        for px in range(x, x + w):
            start = (py * width + px) * 4
            pixels[start:start + 4] = bytes(color)
def meta(name, data):
    path = ROOT / 'taller' / 'font' / (name + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
NAVY=(24,48,76,255); TEAL=(81,212,203,255); DARK=(12,27,44,255); WHITE=(255,255,255,255)
p = canvas(160,48)
rect(p,160,0,0,160,48,TEAL);rect(p,160,1,1,158,46,DARK);rect(p,160,2,2,156,44,NAVY)
rect(p,160,0,0,3,48,(236,174,72,255))
png(ROOT/'taller/textures/hud/panel.png',160,48,p)
providers=[{'type':'bitmap','file':'taller:hud/panel.png','height':48,'ascent':8,'chars':['\ue000']}]
for frame in range(6):
    p=canvas(140,6);rect(p,140,0,0,140,6,(74,103,127,255));rect(p,140,1,1,138,4,DARK)
    fill=frame*138//5
    if fill:rect(p,140,1,1,fill,4,TEAL)
    png(ROOT/f'taller/textures/hud/progress_{frame}.png',140,6,p)
    providers.append({'type':'bitmap','file':f'taller:hud/progress_{frame}.png','height':6,'ascent':-26,'chars':[chr(0xe010+frame)]})
meta('hud',{'providers':providers})
for on in [False,True]:
    p=canvas(24,12);rect(p,24,0,0,24,12,TEAL if on else (97,116,136,255))
    rect(p,24,1,1,22,10,NAVY);rect(p,24,13 if on else 2,2,9,8,TEAL if on else WHITE)
    png(ROOT/f'taller/textures/icons/toggle_{"on" if on else "off"}.png',24,12,p)
meta('icons',{'providers':[{'type':'space','advances':{' ':4}},
    {'type':'bitmap','file':'taller:icons/toggle_on.png','height':12,'ascent':10,'chars':['\ue101']},
    {'type':'bitmap','file':'taller:icons/toggle_off.png','height':12,'ascent':10,'chars':['\ue102']}]})
# Original 5x7 alphabet: all HUD glyphs intentionally have a 5px extent and a 6px advance.
patterns={
'A':'01110/10001/10001/11111/10001/10001/10001','B':'11110/10001/10001/11110/10001/10001/11110',
'C':'01111/10000/10000/10000/10000/10000/01111','D':'11110/10001/10001/10001/10001/10001/11110',
'E':'11111/10000/10000/11110/10000/10000/11111','F':'11111/10000/10000/11110/10000/10000/10000',
'G':'01111/10000/10000/10111/10001/10001/01111','H':'10001/10001/10001/11111/10001/10001/10001',
'I':'11111/00100/00100/00100/00100/00100/11111','J':'00111/00010/00010/00010/10010/10010/01100',
'K':'10001/10010/10100/11000/10100/10010/10001','L':'10000/10000/10000/10000/10000/10000/11111',
'M':'10001/11011/10101/10101/10001/10001/10001','N':'10001/11001/10101/10011/10001/10001/10001',
'O':'01110/10001/10001/10001/10001/10001/01110','P':'11110/10001/10001/11110/10000/10000/10000',
'Q':'01110/10001/10001/10001/10101/10010/01101','R':'11110/10001/10001/11110/10100/10010/10001',
'S':'01111/10000/10000/01110/00001/00001/11110','T':'11111/00100/00100/00100/00100/00100/00100',
'U':'10001/10001/10001/10001/10001/10001/01110','V':'10001/10001/10001/10001/10001/01010/00100',
'W':'10001/10001/10001/10101/10101/10101/01010','X':'10001/10001/01010/00100/01010/10001/10001',
'Y':'10001/10001/01010/00100/00100/00100/00100','Z':'11111/00001/00010/00100/01000/10000/11111',
'0':'01110/10001/10011/10101/11001/10001/01110','1':'00100/01100/00100/00100/00100/00100/11111',
'2':'01110/10001/00001/00010/00100/01000/11111','3':'11110/00001/00001/01110/00001/00001/11110',
'4':'00010/00110/01010/10010/11111/00010/00010','5':'11111/10000/10000/11110/00001/00001/11110',
'6':'01110/10000/10000/11110/10001/10001/01110','7':'11111/00001/00010/00100/01000/01000/01000',
'8':'01110/10001/10001/01110/10001/10001/01110','9':'01110/10001/10001/01111/00001/00001/01110',
'/':'00001/00001/00010/00100/01000/10000/10000','-':'00000/00000/00000/11111/00000/00000/00000'}
characters=list(patterns)
while len(characters)<48:characters.append(chr(0xf800+len(characters)))
p=canvas(128,24)
for i,char in enumerate(characters):
    for y,row in enumerate(patterns.get(char,'00000/'*6+'00000').split('/')):
        for x,value in enumerate(row):
            if value=='1':rect(p,128,(i%16)*8+x,(i//16)*8+y,1,1,WHITE)
png(ROOT/'taller/textures/font/hud.png',128,24,p)
chars=[''.join(characters[i:i+16]) for i in range(0,48,16)]
for name,ascent in [('label',-2),('value',-14)]:
    meta(name,{'providers':[{'type':'space','advances':{' ':4}},
        {'type':'bitmap','file':'taller:font/hud.png','height':8,'ascent':ascent,'chars':chars}]})
advances={chr(0xf000+bit):1<<bit for bit in range(10)}
advances.update({chr(0xf010+bit):-(1<<bit) for bit in range(10)})
meta('space',{'providers':[{'type':'space','advances':advances}]})
for name in ['white_background','white_progress']:
    png(ROOT/f'minecraft/textures/gui/sprites/boss_bar/{name}.png',182,5,canvas(182,5))
print('Generated original panel, progress frames, switches, alphabet and spacing fonts.')
