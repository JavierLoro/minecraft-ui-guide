"""Package the reusable demo with its built plugin, excluding all runtime/player data."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
DEMO=ROOT/'demo'
OUT=ROOT/'downloads';OUT.mkdir(exist_ok=True)
jar=DEMO/'build/libs/minecraft-ui-demo.jar'
pack=DEMO/'build/pack/taller-pack.zip'
assert jar.is_file() and pack.is_file(),'Compile demo first'
files=[]
for directory in ['src','pack','tools','gradle']:
    files.extend(p for p in (DEMO/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ['settings.gradle.kts','build.gradle.kts','gradlew','gradlew.bat','versions.json','.gitignore','.gitattributes','README.md','AGENTS.md','CAPTURAS.md','LICENSE','NOTICE']:
    files.append(DEMO/name)
archive=OUT/'minecraft-ui-demo.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):
        name=p.relative_to(DEMO).as_posix()
        info=zipfile.ZipInfo(name,date_time=(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=(0o100755 if name=='gradlew' else 0o100644)<<16
        z.writestr(info,p.read_bytes())
    for p,name in [(jar,'dist/minecraft-ui-demo.jar'),(pack,'dist/taller-pack.zip')]:
        info=zipfile.ZipInfo(name,date_time=(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes())
(OUT/'minecraft-ui-demo.jar').write_bytes(jar.read_bytes())
(OUT/'taller-pack.zip').write_bytes(pack.read_bytes())
manifest={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
          for p in [archive,OUT/'minecraft-ui-demo.jar',OUT/'taller-pack.zip']}
(OUT/'demo-checksums.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any(name.startswith(('run/','build/','.gradle/')) for name in z.namelist())
    assert 'dist/minecraft-ui-demo.jar' in z.namelist() and 'gradle/wrapper/gradle-wrapper.jar' in z.namelist()
print('Demo packaged:',archive.name,archive.stat().st_size,'bytes; no runtime profiles, world or logs.')
