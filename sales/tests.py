from django.test import TestCase

# Create your tests here.

# class ball(object):
#     def play(self):
#         print('123')
#
# class animal:
#     def dog(self,ball):
#         # print(ball)
#         self.ball = ball
#         self.ball.play()
#
#
# b = ball()
# a = animal()
#
# a.dog(b)


l1 = [1,2,3]
print(id(l1))
def f(a):
    a = a +[3]
    print(id(a))
    print(a)
f(l1)
print(l1)


l=[1,2,3]
def a(x):
  x=x+[4]
a(l)
print(l)

import copy
a = [1,2,3,[3,2,1]]
b=a
c= copy.copy(a)
d = copy.deepcopy(a)
print(id(a),id(b),id(c),id(d))
c[3].append(4)
print(a,b,c,d)
s = (i for i in range(10))
print(id(s))
list(s)
print(s,list(s),id(list(s)))