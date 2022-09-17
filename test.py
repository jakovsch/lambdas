from lambdas import *

tests = [
    ('LTOLS(APPEND(APPEND(LIST)(ONE))(ONE))', [1, 1]),
    ('LTOI(IF(GT(ONE)(TWO))(ONE)(TEN))', 10),
    ('LTOI(DIV(ADD(MUL(TEN)(FIVE))(FOUR))(SIX))', 9),
    ('LTOLS(MAP(MUL(TWO))(RANGE(TWO)(TEN)))', [4, 6, 8, 10, 12, 14, 16, 18]),
    ('LTOI(ITOL(LTOB(BTOL(None is None))))', 1),
    ('LTOLS(REVERSE(LSTOL([1, 2, 2, 3, 4])))', [4, 3, 2, 2, 1]),
]

for l, r in tests:
    e = expand_lambdas(l)
    assert eval(e) == r
    assert len(e) > len(l)

print('All tests passed.')
