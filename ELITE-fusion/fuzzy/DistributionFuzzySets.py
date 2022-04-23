import math
class Distribution:
    def __init__(self, distribution_crisp, m):
        self.distributionCrisp = distribution_crisp
        self.ll = 0.2 * m
        self.mm = 0.5 * m
        self.hh = 0.8 * m

    # 好
    def good(self):
        x1 = self.mm
        y1 = 0
        x2 = self.hh
        y2 = 1
        if self.distributionCrisp < x1:
            return 0
        elif self.distributionCrisp > x2:
            return 1
        else:
            return y1 + (y2-y1) * ((self.distributionCrisp - x1) / (x2 - x1))

    # 中
    def medium(self):
        x1 = self.ll
        y1 = 0
        x2 = self.mm
        y2 = 1
        x3 = self.hh
        y3 = 0
        if x1 <= self.distributionCrisp <= x2:
            return y1 + (y2-y1) * ((self.distributionCrisp - x1) / (x2 - x1))
        elif x2 <= self.distributionCrisp <= x3:
            return y2 + (y3-y2) * ((self.distributionCrisp - x2) / (x3 - x2))
        else:
            return 0

    # 差
    def poor(self):
        x1 = self.ll
        y1 = 1
        x2 = self.mm
        y2 = 0
        if self.distributionCrisp < x1:
            return 1
        elif self.distributionCrisp > x2:
            return 0
        else:
            return y1 + (y2-y1) * ((self.distributionCrisp - x1) / (x2 - x1))

    # # 好
    # def good(self):
    #     a = 0.4
    #     b = 0.6
    #     c1 = 5
    #     c2 = -2
    #     if self.distributionCrisp < a:
    #         return 0
    #     elif self.distributionCrisp > b:
    #         return 1
    #     else:
    #         return c1 * self.distributionCrisp + c2
    #         # return math.pow((x - a) / (b - a), k)
    #
    # # 中
    # def medium(self):
    #     a = 0
    #     b = 0.2
    #     c = 0.2
    #     d = 0.6
    #     c1 = 5
    #     c2 = 0
    #     c3 = -2.5
    #     c4 = 1.5
    #     if a <= self.distributionCrisp <= b:
    #         return c1 * self.distributionCrisp + c2
    #         # return math.pow((x - a) / (b - a), k)
    #     elif c <= self.distributionCrisp <= d:
    #         return c3 * self.distributionCrisp + c4
    #         # return math.pow((d - x) / (d - c), k)
    #     else:
    #         return 0
    #
    # # 差
    # def poor(self):
    #     a = 0
    #     b = 0.2
    #     c1 = -5
    #     c2 = 1
    #     if self.distributionCrisp < a:
    #         return 1
    #     elif self.distributionCrisp > b:
    #         return 0
    #     else:
    #         return c1 * self.distributionCrisp + c2
    #         # return math.pow((b - x) / (b - a), k)
