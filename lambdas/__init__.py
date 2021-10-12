import re, os
from .λ import *

_indent = r'\n[ ]{2,}'
_ws = r'\n|[ ]{2,}'
_rp = r'^\)'
_name = r'\w+'
_b_name_b = r'\b{}\b'

def _getsource():
    src = re.sub(_indent, '', open(
        os.path.join(os.path.dirname(__file__), 'λ.py'),
        encoding='utf-8'
    ).read()).split('\n')
    try:
        for i in range(len(src)):
            if re.match(_rp, src[i+1]):
                yield re.sub(_ws, '', src[i]+src[i+1]).split('=', 1)
            else:
                yield re.sub(_ws, '', src[i]).split('=', 1)
    except IndexError:
        return

def expand_lambdas(src):
    for k in _sources.keys():
        while k in re.findall(_name, src):
            src = re.sub(
                _b_name_b.format(k),
                expand_lambdas(f'({_sources[k]})'),
                src
            )
    return src

_sources = {
    line[0].rstrip():
    line[-1].lstrip()
    for line in _getsource()
    if re.match(_name, line[0])
}

for name in _sources.keys():
    func = eval(name)
    func.__name__ = name
    func.__qualname__ = name
