import ast
from collections import namedtuple
from itertools import chain, zip_longest
from operator import eq

def once(i):
    yield i

def resolve_fields(node, strict=False):
    if isinstance(node, ast.AST):
        r = chain(once(type(node)), (
            (k, resolve_fields(v, True))
            for k, v in ast.iter_fields(node)
        ))
        return tuple(r) if strict else r
    elif isinstance(node, list):
        r = (resolve_fields(i, strict) for i in node)
        return list(r) if strict else r
    elif isinstance(node, tuple):
        r = (i for i in node)
        return tuple(r) if strict else r
    else:
        return node if strict else once(node)

def node_eq(*nodes):
    return all(
        all(map(eq, field[:-1], field[1:]))
        for field in zip_longest(
            *map(resolve_fields, nodes), fillvalue=object()
        )
    )

class wildcard:

    def __init__(self):
        self.cmp = list()

    def __eq__(self, other):
        self.cmp.append(other)
        return True

    def last(self):
        return self.cmp[-1]

class Symtable(ast.NodeVisitor):

    LambdaDef = namedtuple('LambdaDef', ('name', 'ast', 'src'))

    def __init__(self):
        self.lambdas = dict()
        self.freevars = list()
        self._ns = list()
        super().__init__()

    def scan(self, src):
        self.visit(ast.parse(src, '', 'exec'))
        return self.lambdas

    def visit_Assign(self, node):
        super().generic_visit(node)
        (_, (name,)), (_, value), *_ = ast.iter_fields(node)
        self.lambdas[name.id] = self.LambdaDef(
            name.id, value, ast.unparse(value)
        )

    def visit_Name(self, node):
        if node.id not in self._ns:
            self.freevars.append(node.id)

    def visit_arguments(self, node):
        for arg in node.args:
            self._ns.append(arg.arg)

    def visit_Lambda(self, node):
        outer = self._ns.copy()
        self.visit(node.args)
        self.visit(node.body)
        self._ns = outer

class LambdaExpander(ast.NodeTransformer):

    def __init__(self, lambdas=None):
        self.lambdas = lambdas or dict()
        super().__init__()

    def expand(self, src):
        return ast.unparse(self.visit(ast.parse(src, '', 'eval')))

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            lambda_def = self.lambdas.get(node.id)
            if lambda_def is not None:
                return ast.copy_location(
                    self.visit(lambda_def.ast), node
                )
        return node

class SKITermRewriter(ast.NodeTransformer):

    def rewrite(self, src):
        return ast.unparse(self.visit(ast.parse(src, '', 'eval')))

    def visit_Call(self, node):
        (_, func), (_, (arg,)), *_ = ast.iter_fields(node)
        # T[E] => (T[E₁] T[E₂])
        return ast.copy_location(
            ast.Call(
                func=self.visit(func),
                args=[self.visit(arg)],
                keywords=[]
            ), node
        )

    def visit_Lambda(self, node):
        (_, args), (_, body) = ast.iter_fields(node)
        st, w_arg = Symtable(), wildcard()
        st.visit(body)
        if node_eq(
            args, ast.arguments(
                args=[ast.arg(arg=w_arg)],
                posonlyargs=[],
                kwonlyargs=[],
                defaults=[],
                kw_defaults=[]
            )
        ):
            if isinstance(body, ast.Name) and w_arg.last() == body.id:
                # T[λx.x] => I
                return ast.Name(ctx=ast.Load(), id='I')
            elif w_arg.last() not in st.freevars:
                # T[λx.E] => (K T[E])
                return ast.Call(
                    func=ast.Name(ctx=ast.Load(), id='K'),
                    args=[self.visit(body)],
                    keywords=[]
                )
            elif isinstance(body, ast.Call):
                # T[λx.E] => (S T[λx.E₁] T[λx.E₂])
                return ast.Call(
                    func=ast.Call(
                        func=ast.Name(ctx=ast.Load(), id='S'),
                        args=[self.visit(
                            ast.Lambda(
                                args=args,
                                body=body.func
                            )
                        )],
                        keywords=[]
                    ),
                    args=[self.visit(
                        ast.Lambda(
                            args=args,
                            body=body.args[0]
                        )
                    )],
                    keywords=[]
                )
            elif isinstance(body, ast.Lambda):
                # T[λx.λy.E] => T[λx.T[λy.E]]
                return self.visit(
                    ast.Lambda(
                        args=args,
                        body=self.visit(body)
                    )
                )
        return node
