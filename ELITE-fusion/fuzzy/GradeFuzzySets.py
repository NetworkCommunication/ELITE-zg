import math

class Grade:
    def __init__(self, grade_crisp):
        self.gradeCrisp = grade_crisp
        self.k1 = 5
        self.k2 = -5

    # Outstanding 0.8-1.0
    def outstanding(self):
        if self.gradeCrisp >= 0.8 and self.gradeCrisp <= 1.0:
            return self.k1 * self.gradeCrisp - 4
        else:
            return 0

    # Excellent 0.6-0.8-1.0
    def excellent(self):
        if self.gradeCrisp >= 0.6 and self.gradeCrisp < 0.8:
            return self.k1 * self.gradeCrisp - 3
        elif self.gradeCrisp >= 0.8 and self.gradeCrisp <= 1.0:
            return self.k2 * self.gradeCrisp + 5
        else:
            return 0

    # Good 0.4-0.6-0.8
    def good(self):
        if self.gradeCrisp >= 0.4 and self.gradeCrisp < 0.6:
            return self.k1 * self.gradeCrisp - 2
        elif self.gradeCrisp >= 0.6 and self.gradeCrisp <= 0.8:
            return self.k2 * self.gradeCrisp + 4
        else:
            return 0

    # Medium 0.2-0.4-0.6
    def medium(self):
        if self.gradeCrisp >= 0.2 and self.gradeCrisp < 0.4:
            return self.k1 * self.gradeCrisp - 1
        elif self.gradeCrisp >= 0.4 and self.gradeCrisp <= 0.6:
            return self.k2 * self.gradeCrisp + 3
        else:
            return 0

    # Poor 0-0.2-0.4
    def bad(self):
        if self.gradeCrisp >= 0.0 and self.gradeCrisp < 0.2:
            return self.k1 * self.gradeCrisp
        elif self.gradeCrisp >= 0.2 and self.gradeCrisp <= 0.4:
            return self.k2 * self.gradeCrisp + 2
        else:
            return 0

    # Worst 0-0.2
    def worst(self):
        if self.gradeCrisp >= 0 and self.gradeCrisp <= 0.2:
            return self.k2 * self.gradeCrisp + 1
        else:
            return 0