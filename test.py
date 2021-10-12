from lambdas import *

assert eval(_ := expand_lambdas(
    __ := 'LTOLS(APPEND(APPEND(LIST)(ONE))(ONE))'
)) == [1, 1]
assert len(_) > len(__)

assert eval(_ := expand_lambdas(
    __ := 'LTOI(IF(GT(ONE)(TWO))(ONE)(TEN))'
)) == 10
assert len(_) > len(__)

assert eval(_ := expand_lambdas(
    __ := 'LTOI(DIV(ADD(MUL(TEN)(FIVE))(FOUR))(SIX))'
)) == 9
assert len(_) > len(__)

assert eval(_ := expand_lambdas(
    __ := 'LTOLS(MAP(MUL(TWO))(RANGE(TWO)(TEN)))'
)) == [4, 6, 8, 10, 12, 14, 16, 18]
assert len(_) > len(__)

assert eval(_ := expand_lambdas(
    __ := 'LTOI(ITOL(LTOB(BTOL(None is None))))'
)) == 1
assert len(_) > len(__)

assert eval(_ := expand_lambdas(
    __ := 'LTOLS(REVERSE(LSTOL([1, 2, 2, 3, 4])))'
)) == [4, 3, 2, 2, 1]
assert len(_) > len(__)

print('All tests passed.')
