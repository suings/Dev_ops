#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@author:Su
@file:__init__.py
@time:2018/05/22
"""

from cmath import sqrt

a=int(input("请输入ax^2+bx+c=0中a的值(整数): "))
b=int(input("请输入ax^2+bx+c=0中b的值(整数): "))
c=int(input("请输入ax^2+bx+c=0中c的值(整数): "))

print("您输入的方程为%dx^2+ %dx+ %d=0"%(a,b,c))

delta=sqrt(b^2-4*a*c)

if a==0:
    if b==0:
        if c!=0 :
            print("错误的等式")
        else:
            print("恒等式")
    else:
        print("结果为：%f"%(-c/b))
else:
    if delta.imag!=0:
        print("方程无实数解")
    elif delta.real==0:
        print("方程有唯一解：%f"%(-b/(2*a)))
    else:
        print("方程有两个解：x1=%f , x2=%f"%((-b+delta.real)/(2*a),(-b-delta.real)/(2*a)))