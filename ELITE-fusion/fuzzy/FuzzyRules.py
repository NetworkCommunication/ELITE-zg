import fuzzy.ConnectivityFuzzySets as ct
import fuzzy.DistributionFuzzySets as dtri
import fuzzy.DistanceReductionFuzzySets as dtan
import fuzzy.GradeFuzzySets as grade
import numpy as np

# 获取三个变量的清晰输入
# 创建input对象
# 创建rule对象
# 调用 方法
#   调用aggregate方法获取输出项的模糊集以及对应的值 Max
#   调用rules方法得到每一条规则的值 Min

# 输入，根据精确数值确定其所属的类别
class input:
    def __init__(self, distribution_crisp, connectivity_crip, distance_crisp, m1, m2, m3):
        self.distribution_crisp = distribution_crisp # 分布的清晰输入
        self.connectivity_crisp = connectivity_crip # 连通性的清晰输入
        self.distance_crisp = distance_crisp # 距离的清晰输入
        self.distribution_fuzzy = ['Good', 'Medium', 'Poor'] # 分布的模糊集
        self.connectivity_fuzzy = ['High', 'Middle', 'Low'] # 连通性的模糊集
        self.distance_fuzzy = ['Close', 'Medium', 'Far'] # 距离的模糊集
        self.distribution_member = dtri.Distribution(distribution_crisp, m1)  # 分布隶属度对象
        self.connectivity_member = ct.Connectivity(connectivity_crip, m2) # 连通性隶属度对象
        self.distance_member = dtan.Distance(distance_crisp, m3) # 距离隶属度对象

    # 计算得到对每一个模糊集合的隶属度，格式为{set1:membership1, set2:membership2, ...}
    def distribution(self):
        distribution_sets = {}
        distribution_sets['Good'] = self.distribution_member.good()
        distribution_sets['Medium'] = self.distribution_member.medium()
        distribution_sets['Poor'] = self.distribution_member.poor()
        return distribution_sets

    def connectivity(self):
        connectivity_sets = {}
        connectivity_sets['High'] = self.connectivity_member.high()
        connectivity_sets['Middle'] = self.connectivity_member.middle()
        connectivity_sets['Low'] = self.connectivity_member.low()
        return connectivity_sets

    def distance(self):
        distance_sets = {}
        distance_sets['Close'] = self.distance_member.close()
        distance_sets['Medium'] = self.distance_member.medium()
        distance_sets['Far'] = self.distance_member.far()
        return distance_sets

# 规则
# distribution_fuzzy = ['Good', 'Medium', 'Poor']
# connectivity_fuzzy = ['High', 'Middle', 'Low']
# distance_fuzzy = ['Close', 'Medium', 'Far']
class rule:
    def __init__(self, input):
        # self.distributionMembership = dtri.Distribution(input.distribution_crisp)
        # self.connectivityMembership = ct.Connectivity(input.connectivity_crisp)
        # self.distanceMembership = dtan.Distance(input.distance_crisp)
        self.distributionFuzzy = input.distribution() # 分布所属类别以及对应的隶属度
        self.connectivityFuzzy = input.connectivity() # 连通所属类别以及对应的隶属度
        self.distanceFuzzy = input.distance() # 距离所属类别以及对应的隶属度
        self.k1 = 5
        self.k2 = -5

    # 输入为所属的模糊集合以及隶属度
    # 输出为规则结果的集合以及权重 采用Min-Max方法
    def rules(self, distribution_set, distribution_member, connectivity_set, connectivity_member, distance_set, distance_member):
        # 得到所有隶属度里最小的
        Min = min([distribution_member, connectivity_member, distance_member])

        if distribution_set == 'Good' and connectivity_set == 'High' and distance_set == 'Close':

            return 'Excellent', Min

        elif distribution_set == 'Good' and connectivity_set == 'High' and distance_set == 'Medium':

            return 'Excellent', Min

        elif distribution_set == 'Good' and connectivity_set == 'High' and distance_set == 'Far':

            return 'Good', Min

        elif distribution_set == 'Good' and connectivity_set == 'Middle' and distance_set == 'Close':

            return 'Excellent', Min

        elif distribution_set == 'Good' and connectivity_set == 'Middle' and distance_set == 'Medium':

            return 'Good', Min

        elif distribution_set == 'Good' and connectivity_set == 'Middle' and distance_set == 'Far':

            return 'Medium', Min

        elif distribution_set == 'Good' and connectivity_set == 'Low' and distance_set == 'Close':

            return 'Good', Min

        elif distribution_set == 'Good' and connectivity_set == 'Low' and distance_set == 'Medium':

            return 'Medium', Min

        elif distribution_set == 'Good' and connectivity_set == 'Low' and distance_set == 'Far':

            return 'Medium', Min

        # xxx
        elif distribution_set == 'Medium' and connectivity_set == 'High' and distance_set == 'Close':

            return 'Good', Min

        elif distribution_set == 'Medium' and connectivity_set == 'High' and distance_set == 'Medium':

            return 'Medium', Min

        elif distribution_set == 'Medium' and connectivity_set == 'High' and distance_set == 'Far':

            return 'Medium', Min

        elif distribution_set == 'Medium' and connectivity_set == 'Middle' and distance_set == 'Close':

            return 'Medium', Min

        elif distribution_set == 'Medium' and connectivity_set == 'Middle' and distance_set == 'Medium':

            return 'Medium', Min

        elif distribution_set == 'Medium' and connectivity_set == 'Middle' and distance_set == 'Far':

            return 'Bad', Min

        elif distribution_set == 'Medium' and connectivity_set == 'Low' and distance_set == 'Close':

            return 'Medium', Min

        elif distribution_set == 'Medium' and connectivity_set == 'Low' and distance_set == 'Medium':

            return 'Bad', Min

        elif distribution_set == 'Medium' and connectivity_set == 'Low' and distance_set == 'Far':

            return 'Worst', Min

        # xxx
        elif distribution_set == 'Poor' and connectivity_set == 'High' and distance_set == 'Close':

            return 'Medium', Min

        elif distribution_set == 'Poor' and connectivity_set == 'High' and distance_set == 'Medium':

            return 'Bad', Min

        elif distribution_set == 'Poor' and connectivity_set == 'High' and distance_set == 'Far':

            return 'Worst', Min

        elif distribution_set == 'Poor' and connectivity_set == 'Middle' and distance_set == 'Close':

            return 'Bad', Min

        elif distribution_set == 'Poor' and connectivity_set == 'Middle' and distance_set == 'Medium':

            return 'Bad', Min

        elif distribution_set == 'Poor' and connectivity_set == 'Middle' and distance_set == 'Far':

            return 'Worst', Min

        elif distribution_set == 'Poor' and connectivity_set == 'Low' and distance_set == 'Close':

            return 'Bad', Min

        elif distribution_set == 'Poor' and connectivity_set == 'Low' and distance_set == 'Medium':

            return 'Worst', Min

        elif distribution_set == 'Poor' and connectivity_set == 'Low' and distance_set == 'Far':

            return 'Worst', Min

    # 计算出结果中每一个集合的切割比
    # 输出 {out_set: mem, ...}
    def aggregate(self):
        rank = {'Excellent':[], 'Good':[], 'Medium':[], 'Bad':[], 'Worst':[]} # 后面记录了所有由规则得到的值
        Min_Max = {}
        for dtri_set, dtri_mem in self.distributionFuzzy.items():
            for con_set, con_mem in self.connectivityFuzzy.items():
                for dtan_set, dtan_mem in self.distanceFuzzy.items():
                    set, mem = self.rules(dtri_set, dtri_mem, con_set, con_mem, dtan_set, dtan_mem)
                    rank[set].append(mem)
        for key, value in rank.items():
            if len(value) != 0:
                Min_Max[key] = max(value)
        #print("Min-Max: ", Min_Max)
        return Min_Max

    def calculate_y(self, x, x1, y1, x2, y2):
        y = y1 + (y2 - y1) * ((x - x1) / (x2 - x1))
        return y

    # Excellent
    def excellent(self, x):
        if x >= 0.75 and x <= 1:
            y = self.calculate_y(x, 0.75, 0, 1, 1)
            return y
        else:
            return 0

    # Good
    def good(self, x):
        if x >= 0.5 and x < 0.75:
            y = self.calculate_y(x, 0.5, 0, 0.75, 1)
            return y
        elif x >= 0.75 and x <= 1:
            y = self.calculate_y(x, 0.75, 1, 1, 0)
            return y
        else:
            return 0

    # Medium
    def medium(self, x):
        if x >= 0.25 and x < 0.5:
            y = self.calculate_y(x, 0.25, 0, 0.5, 1)
            return y
        elif x >= 0.5 and x <= 0.75:
            y = self.calculate_y(x, 0.5, 1, 0.75, 0)
            return y
        else:
            return 0

    # Poor
    def bad(self, x):
        if x >= 0.0 and x < 0.25:
            y = self.calculate_y(x, 0, 0, 0.25, 1)
            return y
        elif x >= 0.25 and x <= 0.5:
            y = self.calculate_y(x, 0.25, 1, 0.5, 0)
            return y
        else:
            return 0

    # Worst
    def worst(self, x):
        if x >= 0 and x <= 0.25:
            y = self.calculate_y(x, 0, 1, 0.25, 0)
            return y
        else:
            return 0

    # 接收某一个模糊集合以及对它的切割
    # 根据模糊集合的隶属度函数，计算x对应的y=mem(x)，并返回[x,y]
    def points(self, set, mem, step):
        single_pre = []
        if set == 'Excellent':
            for x in np.arange(0, 1+step, step):
                y = self.excellent(x)
                if y != 0:
                    if y >= mem:
                        y = mem
                    single_pre.append([x,y])
        elif set == 'Good':
            for x in np.arange(0, 1+step, step):
                y = self.good(x)
                if y != 0:
                    if y >= mem:
                        y = mem
                    single_pre.append([x,y])
        elif set == 'Medium':
            for x in np.arange(0, 1+step, step):
                y = self.medium(x)
                if y != 0:
                    if y >= mem:
                        y = mem
                    single_pre.append([x,y])
        elif set == 'Bad':
            for x in np.arange(0, 1+step, step):
                y = self.bad(x)
                if y != 0:
                    if y >= mem:
                        y = mem
                    single_pre.append([x,y])
        elif set == 'Worst':
            for x in np.arange(0, 1+step, step):
                y = self.worst(x)
                if y != 0:
                    if y >= mem:
                        y = mem
                    single_pre.append([x,y])
        else:
            single_pre = []
            print("wrong in defuzzification")
        return single_pre

    # 质心法求清晰输出 step 为步长
    def defuzzy(self, Min_Max, step = 0.1):
        pre = [] # 用于存储所有模糊集合的x和mem(x)
        num = 0
        den = 0
        # 分别计算每个集合的x和mem(x)，存储到列表中
        for set, mem in Min_Max.items():
            #print(set, mem)
            single_set = self.points(set, mem, step)
            pre.extend(single_set)
        for value in pre:
            num += value[0] * value[1]
            den += value[1]
        result = round(num / den, 2)
        return result