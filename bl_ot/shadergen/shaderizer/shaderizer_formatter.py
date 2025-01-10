import re

from ....util.util import *
from .. import shadergen_data as sgd
from ..shadergen_util import *

def format_code(code):
    code = cleanup_code(code)
    code = relax_code(code)
    code = force_newline(code)
    code = clear_indent(code)
    res_code = ''
    indent_string = '  '
    indent_level = 0
    for line in code.splitlines():
        if line.count('{') == 0 and line.count('}') > 0: indent_level-=1
        res_code += indent_string*indent_level + line + '\n'
        if line.count('{') > 0 and line.count('}') == 0: indent_level+=1
    return res_code

def force_newline(code):
    res_code = ''
    for line in code.splitlines():
        if line.count(';') > 1 and line.count('for')==0:
            res_code += line.replace(';', ';\n') + '\n'
        else:
            res_code += line + '\n'
    return res_code

def clear_indent(code):
    res_code = ''
    for line in code.splitlines():
        res_code += line.strip() + '\n'
    return res_code

def relax_code(code):
    code = code.replace(',', ', ')
    return code
    
def cleanup_code(code):
    code = re.sub('\n+', '\n', code)
    code = code.replace(', ', ',')
    code = code.replace(' = ', '=')
    code = code.replace(' + ', '+')
    code = code.replace(' - ', '-')
    code = code.replace(' * ', '*')
    code = code.replace(' / ', '/')
    code = code.replace(' > ', '>')
    code = code.replace(' < ', '<')
    code = code.replace(' << ', '<<')
    code = code.replace(' >> ', '>>')
    code = code.replace(' >= ', '>=')
    code = code.replace(' <= ', '<=')
    code = code.replace(' += ', '+=')
    code = code.replace(' -= ', '-=')
    code = code.replace(' *= ', '*=')
    code = code.replace(' /= ', '/=')
    code = code.replace(') {', '){')
    code = code.replace(')\n{', '){')
    code = code.replace(' )', ')')
    code = code.replace('( ', '(')
    code = code.replace('; ', ';')
    code = code.replace('}void ', '}\nvoid ')

    return code

