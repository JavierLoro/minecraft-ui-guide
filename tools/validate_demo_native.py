"""Validate vanilla commands/dialog codecs without starting Minecraft gameplay or a server."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,tempfile,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home',default=os.environ.get('JAVA_HOME'))
    parser.add_argument('--server-jar',type=Path)
    args=parser.parse_args()
    java=str(Path(args.java_home)/'bin'/('java.exe' if os.name=='nt' else 'java')) if args.java_home else shutil.which('java')
    if not java:raise SystemExit('Use --java-home with a Java 25 JDK.')
    lock=json.loads((ROOT/'demo/versions.json').read_text(encoding='utf-8'))
    cache=Path(tempfile.gettempdir())/'minecraft-ui-vanilla-validation';cache.mkdir(exist_ok=True)
    server=args.server_jar or cache/'server.jar'
    if not server.exists():
        if args.server_jar:raise SystemExit('Server JAR not found.')
        request=urllib.request.Request(lock['server']['url'],headers={'User-Agent':'minecraft-ui-guide/1.0'})
        server.write_bytes(urllib.request.urlopen(request,timeout=90).read())
    assert hashlib.sha1(server.read_bytes()).hexdigest()==lock['server']['sha1'],'Official server hash mismatch'
    jars=[]
    with zipfile.ZipFile(server) as z:
        for name in ['META-INF/versions.list','META-INF/libraries.list']:
            prefix='META-INF/versions/' if 'versions.list' in name else 'META-INF/libraries/'
            for row in z.read(name).decode().splitlines():
                digest,_,relative=row.split('\t')
                data=z.read(prefix+relative)
                assert hashlib.sha256(data).hexdigest()==digest,relative
                path=(cache/prefix/relative).resolve()
                assert path.is_relative_to(cache.resolve()),relative
                path.parent.mkdir(parents=True,exist_ok=True)
                if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:path.write_bytes(data)
                jars.append(str(path))
    result=subprocess.call([java,'-cp',os.pathsep.join(jars),str(ROOT/'tools/native/ValidateData.java'),str(ROOT/'demo/datapack')],cwd=cache)
    raise SystemExit(result)
if __name__=='__main__':main()
