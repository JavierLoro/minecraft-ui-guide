"""Package the vanilla datapack project; never include a server, plugin or world."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
DEMO=ROOT/'demo';OUT=ROOT/'downloads';OUT.mkdir(exist_ok=True)
files=[]
for directory in ['datapack','pack','tools']:
    files.extend(p for p in (DEMO/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ['versions.json','.gitignore','.gitattributes','README.md','AGENTS.md','CAPTURAS.md','LICENSE','NOTICE']:
    files.append(DEMO/name)
def entry(z,name,data):
    info=zipfile.ZipInfo(name,date_time=(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o100644<<16;z.writestr(info,data)
archive=OUT/'minecraft-ui-demo.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):entry(z,p.relative_to(DEMO).as_posix(),p.read_bytes())
    for name in ['taller-datapack.zip','taller-resources.zip']:
        p=DEMO/'build'/name;assert p.is_file();entry(z,'build/'+name,p.read_bytes())
for name in ['taller-datapack.zip','taller-resources.zip']:(OUT/name).write_bytes((DEMO/'build'/name).read_bytes())
for name in ['minecraft-ui-demo.jar','taller-pack.zip']:(OUT/name).unlink(missing_ok=True)
manifest={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
          for p in [archive,OUT/'taller-datapack.zip',OUT/'taller-resources.zip']}
(OUT/'demo-checksums.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any(n.startswith(('run/','run-vanilla/','.gradle/','gradle/','src/')) or n.endswith('.jar') for n in z.namelist())
    assert 'datapack/pack.mcmeta' in z.namelist() and 'pack/pack.mcmeta' in z.namelist()
print('Vanilla project packaged:',archive.stat().st_size,'bytes. No plugins, JARs, worlds or player data.')
