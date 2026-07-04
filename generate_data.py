import ast
import json
from pathlib import Path

src = Path(r'g:/マイドライブ/Webサイト関係/その他プログラム/MIMI Time/MIMI Time_anniversary_edition/MIMI Time_anniversary_edition.py')
text = src.read_text(encoding='utf-8')
module = ast.parse(text, filename=str(src))

assignments = {}
for node in module.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                assignments[target.id] = node.value


def to_js(value):
    if isinstance(value, ast.List):
        return '[' + ', '.join(to_js(elt) for elt in value.elts) + ']'
    if isinstance(value, ast.Tuple):
        return '[' + ', '.join(to_js(elt) for elt in value.elts) + ']'
    if isinstance(value, ast.Dict):
        items = []
        for k, v in zip(value.keys, value.values):
            if k is None:
                items.append('[' + to_js(v) + ']')
            else:
                items.append(to_js(k) + ': ' + to_js(v))
        return '{' + ', '.join(items) + '}'
    if isinstance(value, ast.Constant):
        if value.value is None:
            return 'null'
        if isinstance(value.value, bool):
            return 'true' if value.value else 'false'
        if isinstance(value.value, str):
            return json.dumps(value.value)
        return repr(value.value)
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub):
        return f'-{to_js(value.operand)}'
    raise TypeError(f'Unsupported node: {ast.dump(value)}')

names = ['TIME_LABEL','FOOTER_TEXT','TEXT_COLOR_MAIN','TEXT_COLOR_SUB','TEXT_COLOR_FAINT','BG_COLOR','ALL_VIDEOS','VIDEO_TITLES','DEV_ALL_VIDEOS','DEV_VIDEO_TITLES']
out = []
for name in names:
    if name in assignments:
        out.append(f'const {name} = {to_js(assignments[name])};')
out.append('')
out_path = src.parent / 'mimi-data.js'
out_path.write_text('\n'.join(out), encoding='utf-8')
print(f'wrote {out_path}')
