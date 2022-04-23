import numpy as np
import matplotlib.pyplot as plt
import math


# ------------------------------------连通性
# 高
def high(x):
    a = 0.7
    b = 1.0
    c1 = 10 / 3
    c2 = -7 / 3
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return c1 * x + c2
        #return math.pow((x - a) / (b - a), k)

# 中
def middle(x):
    a = 0.4
    b = 0.7
    c = 0.7
    d = 1.0
    c1 = 10 / 3
    c2 = -4 / 3
    c3 = -10 / 3
    c4 = 10 / 3
    if a <= x < b:
        return c1 * x + c2
        #return math.pow((x - a) / (b - a), k)
    elif c <= x <= d:
        return c3 * x + c4
        #return math.pow((d - x) / (d - c), k)
    else:
        return 0

# 低
def low(x):
    a = 0.4
    b = 0.7
    c1 = -10 / 3
    c2 = 7 / 3
    if x < a:
        return 1
    elif x > b:
        return 0
    else:
        return c1 * x + c2
        #return math.pow((b - x) / (b - a), k)

# ------------------------------------分布
# 好
def good(x):
    a = 0.2
    b = 0.6
    c1 = 2.5
    c2 = -0.5
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return c1 * x + c2
        #return math.pow((x - a) / (b - a), k)

# 中
def medium1(x):
    a = 0
    b = 0.2
    c = 0.2
    d = 0.4
    c1 = 5
    c2 = 0
    c3 = -5
    c4 = 2
    if a <= x <= b:
        return c1 * x + c2
        #return math.pow((x - a) / (b - a), k)
    elif c <= x <= d:
        return c3 * x + c4
        #return math.pow((d - x) / (d - c), k)
    else:
        return 0

# 差
def poor(x):
    a = 0
    b = 0.2
    c1 = -5
    c2 = 1
    if x < a:
        return 1
    elif x > b:
        return 0
    else:
        return c1 * x + c2
        #return math.pow((b - x) / (b - a), k)

# ------------------------------------距离
# 更近
def close(x):
    a = 0.8
    b = 0.9
    c1 = -10
    c2 = 9
    if x < a:
        return 1
    elif x > b:
        return 0
    else:
        return c1 * x + c2
        # return math.pow((b - x) / (b - a), k)

# 差不多
def medium2(x):
    a = 0.8
    b = 0.9
    c = 0.9
    d = 1.0
    c1 = 10
    c2 = -8
    c3 = -10
    c4 = 10
    if a <= x <= b:
        return c1 * x + c2
        #return math.pow((x - a) / (b - a), k)
    elif c <= x <= d:
        return c3 * x + c4
        #return math.pow((d - x) / (d - c), k)
    else:
        return 0

# 更远
def far(x):
    a = 0.9
    b = 1.0
    c1 = 10
    c2 = -9
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return c1 * x + c2
        #return math.pow((x - a) / (b - a), k)

# --------------------------------结果
k1 = 5
k2 = -5
# Outstanding 0.8-1.0
def outstanding(x):
    if x >= 0.8 and x <= 1.0:
        return k1 * x - 4
    else:
        return 0

# Excellent 0.6-0.8-1.0
def excellent(x):
    if x >= 0.6 and x < 0.8:
        return k1 * x - 3
    elif x >= 0.8 and x <= 1.0:
        return k2 * x + 5
    else:
        return 0

# Good 0.4-0.6-0.8
def good3(x):
    if x >= 0.4 and x < 0.6:
        return k1 * x - 2
    elif x >= 0.6 and x <= 0.8:
        return k2 * x + 4
    else:
        return 0

# Medium 0.2-0.4-0.6
def medium3(x):
    if x >= 0.2 and x < 0.4:
        return k1 * x - 1
    elif x >= 0.4 and x <= 0.6:
        return k2 * x + 3
    else:
        return 0

# Poor 0-0.2-0.4
def poor3(x):
    if x >= 0.0 and x < 0.2:
        return k1 * x
    elif x >= 0.2 and x <= 0.4:
        return k2 * x + 2
    else:
        return 0

# Worst 0-0.2
def worst(x):
    if x >= 0 and x <= 0.2:
        return k2 * x + 1
    else:
        return 0


y_con_1 = []
y_con_2 = []
y_con_3 = []
y_dtb_1 = []
y_dtb_2 = []
y_dtb_3 = []
y_dta_1 = []
y_dta_2 = []
y_dta_3 = []
y_grade_1 = []
y_grade_2 = []
y_grade_3 = []
y_grade_4 = []
y_grade_5 = []
y_grade_6 = []

x = np.linspace(0,1,100)
for v in x:
    y_con_1.append(high(v))
    y_con_2.append(middle(v))
    y_con_3.append(low(v))
    y_dtb_1.append(good(v))
    y_dtb_2.append(medium1(v))
    y_dtb_3.append(poor(v))
    y_dta_1.append(close(v))
    y_dta_2.append(medium2(v))
    y_dta_3.append(far(v))
    y_grade_1.append(outstanding(v))
    y_grade_2.append(excellent(v))
    y_grade_3.append(good3(v))
    y_grade_4.append(medium3(v))
    y_grade_5.append(poor3(v))
    y_grade_6.append(worst(v))

# x = [0, 0.2, 0.4, 0.6, 0.8, 1]
# y_con_1 = [0, 0, 0, 0.5, 1, 0]
# y_con_2 = [0, 0.5, 1, 0.5, 0, 0]
# y_con_3 = [1, 0, 0, 0, 0, 0]
# y_dtb_1 = [0, 0, 0, 1, 1, 1]
# y_dtb_2 = [0, 0, 1, 0, 0, 0]
# y_dtb_3 = [1, 0.5, 0, 0, 0, 0]
# y_dta_1 = []
# y_dta_2 = []
# y_dta_3 = [1, , , 0, 0, 0]
# y_grade_1 = []
# y_grade_2 = []
# y_grade_3 = []
# y_grade_4 = []
# y_grade_5 = []
# y_grade_6 = []

plt.figure(figsize=(10,10))
plt.subplot2grid((4,4),(0,0), colspan=2, rowspan=2)
plt.title('connectivity')
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
plt.plot(x,y_con_1, label='high')
plt.plot(x,y_con_2, label='middle')
plt.plot(x,y_con_3, label='low')
plt.legend(loc='upper left')
# plt.show()
# plt.figure()
plt.subplot2grid((4,4),(0,2), colspan=2, rowspan=2)
plt.title('distribution')
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
plt.plot(x,y_dtb_1, label='good')
plt.plot(x,y_dtb_2, label='medium')
plt.plot(x,y_dtb_3, label='poor')
plt.legend(loc='upper left')

plt.subplot2grid((4,4),(2,0), colspan=2, rowspan=2)
plt.title('distance')
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
plt.plot(x,y_dta_1, label='close')
plt.plot(x,y_dta_2, label='medium')
plt.plot(x,y_dta_3, label='far')
plt.legend(loc='upper left')
# plt.show()
# plt.figure()

plt.subplot2grid((4,4),(2,2), colspan=2, rowspan=2)
plt.title('grade')
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])#([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
plt.plot(x,y_grade_1, label='outstanding')
plt.plot(x,y_grade_2, label='excellent')
plt.plot(x,y_grade_3, label='good')
plt.plot(x,y_grade_4, label='medium')
plt.plot(x,y_grade_5, label='poor')
plt.plot(x,y_grade_6, label='worst')
plt.legend(loc='upper left')

plt.show()
