'''
    Booleans. Numbers. Pairs. Lists. Recursion.
    None are fundamental.
'''

IDENT = lambda λ: λ

IF    = IDENT
TRUE  = lambda p: lambda q: p
FALSE = lambda p: lambda q: q

OR  = lambda a: lambda b: a(TRUE)(b)
AND = lambda a: lambda b: a(b)(FALSE)
NOT = lambda a: a(FALSE)(TRUE)

XOR  = lambda a: lambda b: a(NOT(b))(b)
XNOR = lambda a: lambda b: NOT(XOR(a)(b))
NAND = lambda a: lambda b: NOT(AND(a)(b))

B = lambda f: lambda g: lambda h: f(g(h))
C = lambda f: lambda g: lambda h: f(h)(g)
I = IDENT
K = TRUE
S = lambda f: lambda g: lambda h: f(h)(g(h))
U = lambda f: f(f)
W = lambda f: lambda g: f(g)(g)
Y = lambda f: (
    (lambda g: f(g(g)))
    (lambda g: f(g(g)))
)
Z = lambda f: (
    (lambda g: f(
        lambda a: g(g)(a)
    ))
    (lambda g: f(
        lambda a: g(g)(a)
    ))
)
Y = Z

CONS = lambda a: lambda b: lambda c: c(a)(b)
CAR  = lambda p: p(TRUE)
CDR  = lambda p: p(FALSE)

NULL   = lambda _: TRUE
ISNULL = lambda _: lambda _: FALSE

INC = lambda n: lambda a: lambda b: a(n(a)(b))
ADD = lambda a: lambda b: a(INC)(b)
MUL = lambda a: lambda b: lambda c: a(b(c))
DEC = lambda n: lambda f: lambda x: (
    n(lambda g: lambda h: h(g(f)))
    (lambda _: x)
    (IDENT)
)
SUB = lambda a: lambda b: b(DEC)(a)
POW = lambda a: lambda b: b(a)
DIFF = lambda a: lambda b: (
    ADD(SUB(a)(b))
    (SUB(b)(a))
)

ISZERO = lambda a: a(lambda _: FALSE)(TRUE)
GTE = lambda a: lambda b: ISZERO(SUB(b)(a))
LTE = lambda a: lambda b: ISZERO(SUB(a)(b))
GT  = lambda a: lambda b: ISZERO(SUB(INC(b))(a))
LT  = lambda a: lambda b: ISZERO(SUB(INC(a))(b))
EQ  = lambda a: lambda b: AND(GTE(a)(b))(LTE(a)(b))
MIN = lambda a: lambda b: LTE(a)(b)(a)(b)
MAX = lambda a: lambda b: GTE(a)(b)(a)(b)

ZERO  = FALSE
ONE   = IDENT
TWO   = ADD(ONE)(ONE)
THREE = ADD(TWO)(ONE)
FOUR  = INC(THREE)
FIVE  = ADD(TWO)(THREE)
SIX   = MUL(TWO)(THREE)
SEVEN = INC(SIX)
EIGHT = MUL(FOUR)(TWO)
NINE  = POW(THREE)(TWO)
TEN   = MUL(FIVE)(TWO)

DIV = Y(
    lambda f: lambda a: lambda b: LT(a)(b)
    (lambda _: ZERO)
    (lambda _: INC(f(SUB(a)(b))(b)))
    (ZERO)
)
MOD = Y(
    lambda f: lambda a: lambda b: LT(a)(b)
    (lambda _: a)
    (lambda _: f(SUB(a)(b))(b))
    (ZERO)
)
EVEN = lambda a: ISZERO(MOD(a)(TWO))
ODD  = lambda a: NOT(EVEN(a))

FAC = Y(
    lambda f: lambda n: ISZERO(n)
    (lambda _: ONE)
    (lambda _: (
        MUL(n)
        (f(DEC(n)))
    ))
    (ZERO)
)
FIB = Y(
    lambda f: lambda n: LTE(n)(TWO)
    (lambda _: ONE)
    (lambda _: (
        ADD(f(DEC(n)))
        (f(DEC(DEC(n))))
    ))
    (ZERO)
)

SIGN   = lambda n: CONS(TRUE)(n)
NEG    = lambda p: (
    CONS
    (NOT(CAR(p)))
    (CDR(p))
)
ISPOS  = lambda p: CAR(p)
ISNEG  = lambda p: NOT(CAR(p))
UNSIGN = lambda p: CDR(p)
SADD   = lambda a: lambda b: (
    XNOR(CAR(a))(CAR(b))
    (
        CONS
        (CAR(a))
        (ADD(CDR(a))(CDR(b)))
    )
    (
        CONS
        (XOR(CAR(a))(LTE(CDR(a))(CDR(b))))
        (DIFF(CDR(a))(CDR(b)))
    )
)
SSUB = lambda a: lambda b: (
    SADD(a)
    (
        CONS
        (NOT(CAR(b)))
        (CDR(b))
    )
)
SMUL = lambda a: lambda b: (
    CONS
    (XNOR(CAR(a))(CAR(b)))
    (MUL(CDR(a))(CDR(b)))
)

LIST    = CONS(TRUE)(TRUE)
EMPTY   = lambda xs: CAR(xs)
HEAD    = lambda xs: CAR(CDR(xs))
TAIL    = lambda xs: CDR(CDR(xs))
PREPEND = lambda xs: lambda x: CONS(FALSE)(CONS(x)(xs))
APPEND  = Y(
    lambda f: lambda xs: lambda x: EMPTY(xs)
    (lambda _: PREPEND(xs)(x))
    (lambda _: CONS(FALSE)(CONS(HEAD(xs))(f(TAIL(xs))(x))))
    (TRUE)
)
REVERSE = Y(
    lambda f: lambda xs: EMPTY(xs)
    (lambda _: LIST)
    (lambda _: APPEND(f(TAIL(xs)))(HEAD(xs)))
    (TRUE)
)
MAP = Y(
    lambda f: lambda a: lambda xs: EMPTY(xs)
    (lambda _: LIST)
    (lambda _: PREPEND(f(a)(TAIL(xs)))(a(HEAD(xs))))
    (TRUE)
)
RANGE = Y(
    lambda f: lambda a: lambda b: GTE(a)(b)
    (lambda _: LIST)
    (lambda _: PREPEND(f(INC(a))(b))(a))
    (TRUE)
)

LTOB = lambda f: IF(f)(True)(False)
BTOL = lambda x: TRUE if x else FALSE
LTOI = lambda f: f(lambda x: x + 1)(0)
ITOL = lambda x: Y(
    lambda f: lambda xs: lambda x: BTOL(x <= 0)
    (lambda _: xs)
    (lambda _: f(INC(xs))(x - 1))
    (ZERO)
)(ZERO)(x)
LTOLS = lambda f: Y(
    lambda f: lambda xs: lambda x: EMPTY(xs)
    (lambda _: x)
    (lambda _: f(TAIL(xs))(x + [LTOI(HEAD(xs))]))
    ([])
)(f)([])
LSTOL = lambda x: Y(
    lambda f: lambda xs: lambda x: BTOL(len(xs) == 0)
    (lambda _: x)
    (lambda _: f(xs[1:])(APPEND(x)(ITOL(xs[0]))))
    (LIST)
)(x)(LIST)
