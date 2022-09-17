import os
from .λ import *
from .transform import Symtable, LambdaExpander, SKITermRewriter

with open(
    os.path.join(os.path.dirname(__file__), 'λ.py'),
    encoding='utf-8'
) as src:
    expand_lambdas = (lambda defs:
        lambda src: LambdaExpander(defs).expand(src)
    )(Symtable().scan(src.read()))
    ski_rewrite = SKITermRewriter().rewrite
