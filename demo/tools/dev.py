"""Prepare and run the unmodified Minecraft vanilla server for the demo."""
import argparse,hashlib,http.server,json,os,shutil,subprocess,threading,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'run-vanilla'
LOCK=json.loads((ROOT/'versions.json').read_text(encoding='utf-8'))
def java(home):
    executable=str(Path(home)/'bin'/('java.exe' if os.name=='nt' else 'java')) if home else shutil.which('java')
    if not executable:raise SystemExit('Necesitas Java 25; indica JAVA_HOME o --java-home.')
    result=subprocess.run([executable,'-version'],capture_output=True,text=True)
    import re
    version=re.search(r'version "(\d+)',result.stdout+result.stderr)
    if not version or int(version[1])!=25:raise SystemExit('Esta demo requiere Java 25.')
    return executable

def prepare():
    for name in ['taller-datapack.zip','taller-resources.zip']:
        if not (ROOT/'build'/name).exists():raise SystemExit('Ejecuta primero: python tools/build.py')
    RUN.mkdir(exist_ok=True)
    server=RUN/'server.jar'
    expected=LOCK['server']['sha1']
    if not server.exists() or hashlib.sha1(server.read_bytes()).hexdigest()!=expected:
        req=urllib.request.Request(LOCK['server']['url'],headers={'User-Agent':'minecraft-ui-guide/1.0'})
        part=RUN/'server.jar.download'
        try:
            with urllib.request.urlopen(req,timeout=90) as src,part.open('wb') as dst:shutil.copyfileobj(src,dst)
            if hashlib.sha1(part.read_bytes()).hexdigest()!=expected:raise SystemExit('Hash incorrecto; no se ejecuta la descarga.')
            part.replace(server)
        finally:part.unlink(missing_ok=True)
    packs=RUN/'world/datapacks';packs.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'build/taller-datapack.zip',packs/'taller.zip')
    props=RUN/'server.properties'
    if not props.exists():
        pack_hash=hashlib.sha1((ROOT/'build/taller-resources.zip').read_bytes()).hexdigest()
        props.write_text('\n'.join([
            'server-ip=127.0.0.1','server-port=25585','online-mode=true','white-list=false',
            'gamemode=creative','force-gamemode=true','difficulty=peaceful','level-type=minecraft:flat',
            'generate-structures=false','spawn-protection=0','max-players=4','view-distance=5','simulation-distance=3',
            'enable-rcon=false','enable-query=false','enable-command-block=false',
            'resource-pack=http://127.0.0.1:8127/pack.zip','resource-pack-sha1='+pack_hash,
            'require-resource-pack=true','motd=Taller - Minecraft vanilla 26.3',
            'initial-enabled-packs=vanilla,file/taller.zip','pause-when-empty-seconds=-1'])+'\n',encoding='utf-8')
    else:
        lines=props.read_text(encoding='utf-8').splitlines()
        pack_hash=hashlib.sha1((ROOT/'build/taller-resources.zip').read_bytes()).hexdigest()
        lines=[line for line in lines if not line.startswith('resource-pack-sha1=')]
        props.write_text('\n'.join(lines+['resource-pack-sha1='+pack_hash])+'\n',encoding='utf-8')
    if not (RUN/'eula.txt').exists():(RUN/'eula.txt').write_text('eula=false\n',encoding='utf-8')
    print('Preparado servidor VANILLA en run-vanilla/. No usa Paper ni plugins.',flush=True)

class PackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/pack.zip':self.send_error(404);return
        content=(ROOT/'build/taller-resources.zip').read_bytes()
        self.send_response(200);self.send_header('Content-Type','application/zip')
        self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
    def log_message(self,*args):pass

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['prepare','start'])
    parser.add_argument('--java-home',default=os.environ.get('JAVA_HOME'))
    parser.add_argument('--accept-eula',action='store_true',help='Aceptas https://www.minecraft.net/eula')
    args=parser.parse_args()
    if args.command=='prepare':prepare();return
    executable=java(args.java_home)
    if not (RUN/'server.jar').exists():raise SystemExit('Ejecuta primero prepare.')
    if args.accept_eula:(RUN/'eula.txt').write_text('eula=true\n',encoding='utf-8')
    if 'eula=true' not in (RUN/'eula.txt').read_text().splitlines():
        raise SystemExit('Lee la EULA; si la aceptas, inicia con --accept-eula. No se ha arrancado el servidor.')
    server=http.server.ThreadingHTTPServer(('127.0.0.1',8127),PackHandler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:return subprocess.call([executable,'-Xms512M','-Xmx2G','-jar','server.jar','--nogui'],cwd=RUN)
    finally:server.shutdown();server.server_close()
if __name__=='__main__':raise SystemExit(main())
