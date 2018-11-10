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

# file = open(“testfile.txt”, ”w”)
#
# file.write(“Hello
# World”)
# file.write(“This is our
# new
# text
# file”)
# file.write(“ and this is another
# line.”)
# file.write(“Why? Because
# we
# can.”)
#
# file.close()
import numpy as np
# myarray = np.fromfile('usa_00001.dat', dtype=float)
# print(myarray.size)
# print(myarray.ndim)
# # for data in myarray:
# #     print(data)

cur_str = '1\n 2\n 3 4 5 6 \n 7 8 9 10'
print(cur_str)
lists = cur_str.split('\n')
print(lists.__len__())
list1 = lists[2:4]
list1 = np.asarray(list1)
print(list1)
print(type(list1))
print(list1.__len__())

list2 = np.array(list1)
print(list2)

list3 = np.asarray(list1[0])
list4 = np.asarray(list1[1])

final_list = []
final_list.append(list3)
final_list.append(list4)
print(final_list)