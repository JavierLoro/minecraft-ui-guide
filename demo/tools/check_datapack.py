"""Check vanilla pack structure, references and player-safe dialog entry points."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];DP=ROOT/'datapack'
functions=DP/'data/taller/function';dialogs=DP/'data/taller/dialog'
for p in DP.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
assert json.loads((DP/'pack.mcmeta').read_text())['pack']['min_format']==[121,0]
for p in functions.rglob('*.mcfunction'):
    text=p.read_text(encoding='utf-8')
    for name in re.findall(r'\bfunction taller:([a-z0-9_/]+)(?:\s|$)',text):
        assert (functions/(name+'.mcfunction')).is_file(),(p,name)
for p in dialogs.rglob('*.json'):
    def walk(value):
        if isinstance(value,dict):
            if value.get('type') in ['minecraft:run_command','minecraft:dynamic/run_command']:
                assert value.get('command',value.get('template','')).startswith('trigger taller.'),p
            for v in value.values():walk(v)
        elif isinstance(value,list):
            for v in value:walk(v)
    walk(json.loads(p.read_text(encoding='utf-8')))
assert len(list((dialogs/'settings').glob('*.json')))==48
assert (functions/'test/run.mcfunction').is_file()
print('Datapack OK: JSON, function links, 48 settings variants and /trigger-only registered actions.')
