"""Build the vanilla dialogs and distributable datapack/resource pack."""
from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def build():
    out=ROOT/'datapack/data/taller/dialog/settings';out.mkdir(parents=True,exist_ok=True)
    for hud in range(2):
      for anchor in range(2):
       for goal in range(1,13):
        data={'type':'minecraft:confirmation','title':'Ajustes del taller','pause':False,
         'after_action':'wait_for_response','can_close_with_escape':True,
         'inputs':[
          {'key':'hud','type':'minecraft:boolean','label':'Mostrar HUD','initial':bool(hud),'on_true':'1','on_false':'0'},
          {'key':'anchor','type':'minecraft:single_option','label':'Posición','options':[
           {'id':'0','display':'Centrado','initial':anchor==0},{'id':'1','display':'Esquina izquierda','initial':anchor==1}]},
          {'key':'goal','type':'minecraft:number_range','label':'Piezas por pedido','start':1,'end':12,'step':1,'initial':goal}],
         'yes':{'label':'Guardar','tooltip':'Guarda las preferencias; cambiar el tamaño reinicia el pedido.',
          'action':{'type':'minecraft:dynamic/run_command','template':'trigger taller.form set $(goal)$(hud)$(anchor)'}},
         'no':{'label':'Cancelar','action':{'type':'minecraft:run_command','command':'trigger taller.open'}}}
        (out/f'h{hud}_a{anchor}_g{goal}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    target=ROOT/'build';target.mkdir(exist_ok=True)
    for directory,name in [('datapack','taller-datapack.zip'),('pack','taller-resources.zip')]:
      with zipfile.ZipFile(target/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
       for p in sorted((ROOT/directory).rglob('*')):
        if p.is_file():
         info=zipfile.ZipInfo(p.relative_to(ROOT/directory).as_posix(),date_time=(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
         z.writestr(info,p.read_bytes())
    print('Vanilla build: 48 dialogs, datapack and resource pack. No plugin or Java compilation.')
if __name__=='__main__':build()
