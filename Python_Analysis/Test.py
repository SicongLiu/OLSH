# NMinimize[{TotalError,
#   totalHashUsed <= totalBudget && TotalError < 10 && aaa >= 1 &&
#    bbb >= 1 && ccc >= 1 && ddd >= 1 && eee >= 1 && fff >= 1 &&
#    ggg >= 1 && hhh >= 1 && iii >= 1 && jjj >= 1 && kkk >= 1 &&
#    lll >= 1 && mmm >= 1 && nnn >= 1 && ooo >= 1 && ppp >= 1 &&
#    qqq >= 1 && rrr >= 1 && sss >= 1 && ttt >= 1 && uuu >= 1 &&
#    vvv >= 1 && www >= 1 && xxx >= 1 && yyy >= 1 && zzz >= 1 &&
#    aaaa >= 1 && bbbb >= 1 && cccc >= 1 && dddd >= 1 && eeee >= 1 &&
#    ffff >= 1 && gggg >= 1 && hhhh >= 1 && iiii >= 1 && jjjj >= 1 &&
#    kkkk >= 1 && llll >= 1 && mmmm >= 1 && nnnn >= 1 && oooo >= 1 &&
#    pppp >= 1 && qqqq >= 1 && rrrr >= 1 && ssss >= 1 && tttt >= 1 &&
#    uuuu >= 1 && vvvv >= 1 && wwww >= 1 && xxxx >= 1 && yyyy >= 1 &&
#    zzzz >= 1 &&
#    aaa > bbb > ccc > ddd > eee > fff > ggg > hhh > iii > jjj > kkk >
#     lll > mmm > nnn > ooo > ppp > qqq > rrr > sss > ttt > uuu > vvv >
#     www > xxx > yyy > zzz > aaaa > bbbb > cccc > dddd > eeee > ffff >
#     gggg > hhhh > iiii > jjjj > kkkk > llll > mmmm > nnnn > oooo >
#     pppp > qqqq > rrrr > ssss > tttt > uuuu > vvvv > wwww >
#     xxxx}, {aaa, bbb , ccc, ddd , eee, fff, ggg , hhh , iii , jjj,
#   kkk, lll, mmm, nnn, ooo, ppp, qqq, rrr, sss, ttt, uuu, vvv, www,
#   xxx, yyy, zzz, aaaa, bbbb, cccc, dddd, eeee, ffff, gggg, hhhh, iiii,
#    jjjj, kkkk, llll, mmmm, nnnn, oooo, pppp, qqqq, rrrr, ssss, tttt,
#   uuuu, vvvv, wwww, xxxx}, MaxIterations -> 1000]

# a = [1, 2, 3, 4, 5]
# b = [2, 3, 4, 5, 6]
#
# s = "  ".join(map(str, a))
#
# print(s)
# import re
#
# def separate_string(input_string):
#     items = []
#     match = re.match(r"([a-z]+)([0-9]+)", input_string, re.I)
#     if match:
#         items = match.groups()
#         print(items)
#         print(items[0])
#         bb = int(items[1]) + 3
#         print(bb)
#     return items[0] + str(int(items[1]) + 3)
#
# my_string = 'AP32'
# items = separate_string(my_string)
# print(items)
#
# cur = 'A'
import numpy as np

a = [1, 2, 3, 4]
b = [1, 2, 3, 4]
c = [2, 3, 4, 5]
d = [1, 2, 3, 4]
e = [3, 4, 5, 6]

a = np.asarray(a)
b = np.asarray(b)
c = np.asarray(c)
d = np.asarray(d)
e = np.asarray(e)

xx = []
xx.append(a)
xx.append(b)
xx.append(c)
xx.append(d)
xx.append(e)
xx = np.asarray(xx)

print(xx)

my_row = np.where((xx == a).all(axis=1))[0]
if my_row.size > 1:
    print(my_row)
    print(a)
xx = np.delete(xx, my_row, 0)

print(xx)










