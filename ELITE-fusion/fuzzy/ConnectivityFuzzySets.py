import math

# 抛物型函数
#
#       ((x-a) / (b-a))^k   a<= x <=b
#       1                   b<= x <=c
#       ((d-x) / (d-c))^k   c<= x <=d
#       0                   x<a, x>=d
# 无==1
#
#       ((x-a) / (b-a))^k   a<= x <=b
#                           b == c
#       ((d-x) / (d-c))^k   c<= x <=d
#       0                   x<a, x>=d

class Connectivity:
    def __init__(self, connectivity_crisp, m):
        self.connectivityCrisp = connectivity_crisp
        self.ll = 0.2 * m
        self.mm = 0.5 * m
        self.hh = 0.8 * m

    # 高
    def high(self):
        x1 = self.mm
        y1 = 0
        x2 = self.hh
        y2 = 1
        if self.connectivityCrisp < x1:
            return 0
        elif self.connectivityCrisp > x2:
            return 1
        else:
            return y1 + (y2-y1) * ((self.connectivityCrisp - x1) / (x2 - x1))

    # 中
    def middle(self):
        x1 = self.ll
        y1 = 0
        x2 = self.mm
        y2 = 1
        x3 = self.hh
        y3 = 0
        if x1 <= self.connectivityCrisp <= x2:
            return y1 + (y2 - y1) * ((self.connectivityCrisp - x1) / (x2 - x1))
        elif x2 <= self.connectivityCrisp <= x3:
            return y2 + (y3 - y2) * ((self.connectivityCrisp - x2) / (x3 - x2))
        else:
            return 0

    # 低
    def low(self):
        x1 = self.ll
        y1 = 1
        x2 = self.mm
        y2 = 0
        if self.connectivityCrisp < x1:
            return 1
        elif self.connectivityCrisp > x2:
            return 0
        else:
            return y1 + (y2 - y1) * ((self.connectivityCrisp - x1) / (x2 - x1))

    # # 高
    # def high(self):
    #     a = 0.8
    #     b = 1.0
    #     c1 = 5
    #     c2 = -4
    #     if self.connectivityCrisp < a:
    #         return 0
    #     elif self.connectivityCrisp > b:
    #         return 1
    #     else:
    #         return c1 * self.connectivityCrisp + c2
    #         # return math.pow((x - a) / (b - a), k)
    #
    # # 中
    # def middle(self):
    #     a = 0.4
    #     b = 0.7
    #     c = 0.7
    #     d = 1.0
    #     c1 = 10 / 3
    #     c2 = -4 / 3
    #     c3 = -10 / 3
    #     c4 = 10 /3
    #     if a <= self.connectivityCrisp < b:
    #         return c1 * self.connectivityCrisp + c2
    #         # return math.pow((x - a) / (b - a), k)
    #     elif c <= self.connectivityCrisp <= d:
    #         return c3 * self.connectivityCrisp + c4
    #         # return math.pow((d - x) / (d - c), k)
    #     else:
    #         return 0
    #
    # # 低
    # def low(self):
    #     a = 0.2
    #     b = 0.6
    #     c1 = -2.5
    #     c2 = 1.5
    #     if self.connectivityCrisp < a:
    #         return 1
    #     elif self.connectivityCrisp > b:
    #         return 0
    #     else:
    #         return c1 * self.connectivityCrisp + c2
    #         # return math.pow((b - x) / (b - a), k)