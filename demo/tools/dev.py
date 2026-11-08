"""Portable local demo launcher. Needs Python 3.10+ and a Java 25 JDK."""
import argparse, hashlib, json, os, shutil, subprocess, sys, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'run'
LOCK = json.loads((ROOT / 'versions.json').read_text(encoding='utf-8'))
UA = 'minecraft-ui-guide/0.1 (https://github.com/JavierLoro/minecraft-ui-guide)'

def java(home):
    candidate = Path(home) / 'bin' / ('java.exe' if os.name == 'nt' else 'java') if home else shutil.which('java')
    if not candidate: raise SystemExit('Java 25 no encontrado. Indica --java-home o JAVA_HOME.')
    candidate = str(candidate)
    result = subprocess.run([candidate, '-version'], capture_output=True, text=True)
    import re
    match = re.search(r'version "(\d+)', result.stdout + result.stderr)
    if result.returncode or not match or int(match[1]) != LOCK['java']:
        raise SystemExit('Usa un JDK de Java 25 para esta demo.')
    return candidate

def prepare():
    artifact = ROOT / 'build/libs/minecraft-ui-demo.jar'
    if not artifact.is_file(): artifact = ROOT / 'dist/minecraft-ui-demo.jar'
    if not artifact.is_file(): raise SystemExit('Primero compila: gradlew.bat build (Windows) o ./gradlew build.')
    RUN.mkdir(exist_ok=True)
    server = RUN / 'paper.jar'
    expected = LOCK['paper']['sha256']
    if not server.exists() or hashlib.sha256(server.read_bytes()).hexdigest() != expected:
        partial = RUN / 'paper.jar.download'
        request = urllib.request.Request(LOCK['paper']['url'], headers={'User-Agent': UA})
        print('Descargando Paper 26.3 build 244...', flush=True)
        try:
            with urllib.request.urlopen(request, timeout=90) as response, partial.open('wb') as target:
                shutil.copyfileobj(response, target)
            if hashlib.sha256(partial.read_bytes()).hexdigest() != expected:
                raise SystemExit('Checksum de Paper incorrecto. No se ejecuta el archivo descargado.')
            partial.replace(server)
        finally:
            partial.unlink(missing_ok=True)
    plugins = RUN / 'plugins'; plugins.mkdir(exist_ok=True)
    shutil.copyfile(artifact, plugins / artifact.name)
    properties = RUN / 'server.properties'
    if not properties.exists():
        properties.write_text('''server-ip=127.0.0.1
server-port=25585
online-mode=true
enforce-secure-profile=true
gamemode=creative
force-gamemode=true
level-type=minecraft:flat
level-name=demo-world
generate-structures=false
spawn-protection=0
difficulty=peaceful
max-players=4
view-distance=5
simulation-distance=3
allow-flight=true
enable-rcon=false
enable-query=false
enable-command-block=false
pause-when-empty-seconds=-1
motd=Taller - Demo de interfaces
''', encoding='utf-8')
    eula = RUN / 'eula.txt'
    if not eula.exists(): eula.write_text('eula=false\n', encoding='utf-8')
    print('Preparado en run/. Servidor: 127.0.0.1:25585. Paquete: 127.0.0.1:8127.', flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare','start'])
    parser.add_argument('--java-home', default=os.environ.get('JAVA_HOME'))
    parser.add_argument('--accept-eula', action='store_true', help='Aceptas personalmente https://www.minecraft.net/eula')
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.accept_eula: parser.error('--accept-eula se utiliza solo al iniciar el servidor.')
        prepare(); return
    executable = java(args.java_home)
    if not (RUN / 'paper.jar').is_file(): raise SystemExit('Ejecuta primero: python tools/dev.py prepare')
    if args.accept_eula: (RUN / 'eula.txt').write_text('eula=true\n', encoding='utf-8')
    accepted = any(line.strip() == 'eula=true' for line in (RUN/'eula.txt').read_text().splitlines())
    if not accepted:
        raise SystemExit('Lee https://www.minecraft.net/eula y, si la aceptas, ejecuta start con --accept-eula. No se ha iniciado el servidor.')
    raise SystemExit(subprocess.call([executable, '-Xms512M', '-Xmx2G', '-jar', 'paper.jar', '--nogui'], cwd=RUN))
if __name__ == '__main__': main()
