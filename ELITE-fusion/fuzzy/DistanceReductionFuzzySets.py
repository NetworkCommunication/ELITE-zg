import math
class Distance:
    def __init__(self, distance_crisp, m):
        self.distanceCrisp = distance_crisp
        self.ll = 0.2 * m
        self.mm = 0.5 * m
        self.hh = 0.8 * m

    # 更近
    def close(self):
        x1 = self.mm
        y1 = 0
        x2 = self.hh
        y2 = 1
        if self.distanceCrisp < x1:
            return 0
        elif self.distanceCrisp > x2:
            return 1
        else:
            return y1 + (y2-y1) * ((self.distanceCrisp - x1) / (x2 - x1))

    # 差不多
    def medium(self):
        x1 = self.ll
        y1 = 0
        x2 = self.mm
        y2 = 1
        x3 = self.hh
        y3 = 0
        if x1 <= self.distanceCrisp <= x2:
            return y1 + (y2 - y1) * ((self.distanceCrisp - x1) / (x2 - x1))
        elif x2 <= self.distanceCrisp <= x3:
            return y2 + (y3 - y2) * ((self.distanceCrisp - x2) / (x3 - x2))
        else:
            return 0

    # 更远
    def far(self):
        x1 = self.ll
        y1 = 1
        x2 = self.mm
        y2 = 0
        if self.distanceCrisp < x1:
            return 1
        elif self.distanceCrisp > x2:
            return 0
        else:
            return y1 + (y2 - y1) * ((self.distanceCrisp - x1) / (x2 - x1))

    # # 更近
    # def close(self):
    #     a = 0.1
    #     b = 0.5
    #     k = 1
    #     x = self.distanceCrisp
    #     if x < a:
    #         return 1
    #     elif x > b:
    #         return 0
    #     else:
    #         return math.pow((b - x) / (b - a), k)
    #
    # # 差不多
    # def medium(self):
    #     a = 0
    #     b = 0.5
    #     c = 0.5
    #     d = 1.0
    #     k = 1
    #     x = self.distanceCrisp
    #     if a <= x <= b:
    #         return math.pow((x - a) / (b - a), k)
    #     elif c <= x <= d:
    #         return math.pow((d - x) / (d - c), k)
    #     else:
    #         return 0
    #     # a = 1
    #     # b = 0.5
    #     # sig_2 = 0.02
    #     # x = self.distanceCrisp
    #     # return a * math.exp(-1 / (2 * sig_2) * math.pow(x - b, 2))
    #
    # # 更远
    # def far(self):
    #     a = 0.4
    #     b = 0.9
    #     k = 1
    #     x = self.distanceCrisp
    #     if x < a:
    #         return 0
    #     elif x > b:
    #         return 1
    #     else:
    #         return math.pow((x - a) / (b - a), k)