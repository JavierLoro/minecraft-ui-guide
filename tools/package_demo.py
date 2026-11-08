"""Package installation for existing servers and the optional editable source project."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
DEMO=ROOT/'demo';OUT=ROOT/'downloads';OUT.mkdir(exist_ok=True)
SITE='https://javierloro.github.io/minecraft-ui-guide'

def entry(z,name,data):
    info=zipfile.ZipInfo(name,date_time=(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o100644<<16;z.writestr(info,data)

datapack=(DEMO/'build/taller-datapack.zip').read_bytes()
resources=(DEMO/'build/taller-resources.zip').read_bytes()
sha1=hashlib.sha1(resources).hexdigest()
pack_path=OUT/'packs'/(sha1+'.zip');pack_path.parent.mkdir(exist_ok=True)
if pack_path.exists():assert pack_path.read_bytes()==resources,'A content-addressed resource pack cannot change'
else:pack_path.write_bytes(resources)
url=SITE+'/downloads/packs/'+sha1+'.zip'
fragment='resource-pack='+url+'\nresource-pack-sha1='+sha1+'\n'
instructions=(DEMO/'install/INSTALACION.template.md').read_text(encoding='utf-8').replace('{{PACK_URL}}',url).replace('{{PACK_SHA1}}',sha1)
assert '{{' not in instructions
(DEMO/'INSTALACION.md').write_text(instructions,encoding='utf-8',newline='\n')
(DEMO/'install/server.properties.fragment').write_text(fragment,encoding='utf-8',newline='\n')
installation=OUT/'taller-instalacion.zip'
contents={
 'taller-datapack.zip':datapack,
 'taller-resources.zip':resources,
 'server.properties.fragment':fragment.encode(),
 'INSTALACION.md':instructions.encode('utf-8')}
with zipfile.ZipFile(installation,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,data in contents.items():entry(z,name,data)
files=[]
for directory in ['datapack','pack','tools','install']:
    files.extend(p for p in (DEMO/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ['versions.json','.gitignore','.gitattributes','README.md','INSTALACION.md','DESARROLLO.md','AGENTS.md','CAPTURAS.md','LICENSE','NOTICE']:
    files.append(DEMO/name)
archive=OUT/'minecraft-ui-demo.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):entry(z,p.relative_to(DEMO).as_posix(),p.read_bytes())
    entry(z,'build/taller-datapack.zip',datapack);entry(z,'build/taller-resources.zip',resources)
(OUT/'taller-datapack.zip').write_bytes(datapack);(OUT/'taller-resources.zip').write_bytes(resources)
artifacts=[installation,archive,OUT/'taller-datapack.zip',OUT/'taller-resources.zip',pack_path]
manifest={p.relative_to(OUT).as_posix():{'sha1':hashlib.sha1(p.read_bytes()).hexdigest(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in artifacts}
(OUT/'demo-checksums.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(installation) as z:
    assert set(z.namelist())==set(contents) and z.testzip() is None
    assert hashlib.sha1(z.read('taller-resources.zip')).hexdigest()==sha1
    assert z.read('server.properties.fragment').decode()==fragment
    assert 'server.properties' not in z.namelist()
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any(n.startswith(('run/','run-vanilla/','.gradle/','gradle/','src/')) or n.endswith('.jar') for n in z.namelist())
print('Installation ready: 2 ZIPs, instructions and existing-server configuration; no Python, new server or installer script.')
print('Resource URL:',url)
