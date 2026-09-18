import sys
import re

interp_file = r'd:\cpcbasic\core\interpreter.py'
with open(interp_file, 'r', encoding='utf-8') as f:
    code = f.read()

def sanitize_name(name):
    return name.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')

eval_patch = '''        elif isinstance(expr, RawExpression):
            s = ""
            for t in expr.tokens:
                if t.type == 'IDENTIFIER':
                    if t.value.upper() == 'INKEY$':
                        inkey_val = self.display.get_inkey_str()
                        s += f'"{inkey_val}"'
                    elif t.value.upper() in ('CHR$', 'LEFT$', 'RIGHT$', 'MID$', 'STR$', 'SPACE$'):
                        s += t.value.upper().replace('$', '_STR')
                    elif t.value.upper() in self.builtins:
                        s += t.value.upper()
                    elif t.value in self.arrays:
                        s += t.value.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')
                    else:
                        val = self.variables.get(t.value, 0)
                        if isinstance(val, str):
                            s += f'"{val}"'
                        else:
                            s += str(val)
                elif t.type == 'SYMBOL' and t.value == '=':
                    s += '=='
                elif t.type == 'SYMBOL' and t.value == '<>':
                    s += '!='
                elif t.type == 'KEYWORD':
                    kw = t.value.upper()
                    if kw == 'MOD': s += ' % '
                    elif kw == 'AND': s += ' and '
                    elif kw == 'OR': s += ' or '
                    elif kw == 'NOT': s += ' not '
                    elif kw == 'XOR': s += ' ^ '
                    else: s += f' {kw} '
                elif t.type == 'STRING':
                    s += f'"{t.value}"'
                else:
                    s += str(t.value)
                    
            try:
                class ArrayWrapper:
                    def __init__(self, arr_dict):
                        self.arr_dict = arr_dict
                    def __call__(self, *args):
                        return self.arr_dict.get(tuple(int(a) for a in args), 0)
                
                eval_globals = self.builtins.copy()
                eval_globals['REMAIN'] = lambda x: 0
                for arr_name, arr_dict in self.arrays.items():
                    safe_name = arr_name.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')
                    eval_globals[safe_name] = ArrayWrapper(arr_dict)
                    
                return eval(s, eval_globals, {})
            except Exception as e:
                print(f"Error evaluando '{s}': {e}")
                return 0
'''

code = re.sub(r'        elif isinstance\(expr, RawExpression\):.*?return 0\n\s+return 0', eval_patch + '\n        return 0', code, flags=re.DOTALL)

with open(interp_file, 'w', encoding='utf-8') as f:
    f.write(code)
