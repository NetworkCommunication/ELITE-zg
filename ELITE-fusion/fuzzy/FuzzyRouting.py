import fuzzy.AExactData as Exact
import fuzzy.FuzzyRules as rule
import math
import Global_Par as Gp

def fuzzy_routing(distribution_crisp, connectivity_crisp, valid_distance_crisp, m1, m2, m3):
    # 模糊推理
    In = rule.input(distribution_crisp, connectivity_crisp, valid_distance_crisp, m1, m2, m3)
    Ru = rule.rule(In)
    Min_Max = Ru.aggregate()
    result = Ru.defuzzy(Min_Max, step=0.1)
    return result

def break_point():

    return

#half_num 当前区域和邻居区域的半程车辆数 {neib1:num1, neib2:num2,...}
#half_length 当前区域和邻居区域的半程道路长度 {neib1:len1, neib2:len2,...}
#part_num 当前区域和邻居区域之间分段车辆数目 [num1,num2,...]
#part_length 当前车和邻居车之间分段道路长度 len
# def fuzzy_routing(current_area, adjacent_area, target_area, half_num, half_length, part_num, part_length):
#     # 获取清晰输入
#     print("initialization, [current_area, adjacent_area, target_area]:",current_area, adjacent_area, target_area)
#     connectivity_crisp = Exact.nor_connectivity_crisp(part_num, part_length)
#     valid_distance_crisp = Exact.nor_valid_distance_crisp(current_area, adjacent_area, target_area)
#     distribution_crisp = Exact.nor_distribution_crisp(half_num, half_length)
#     # 模糊推理
#     In = rule.input(distribution_crisp, connectivity_crisp, valid_distance_crisp)
#     Ru = rule.rule(In)
#     Min_Max = Ru.aggregate()
#     result = Ru.defuzzy(Min_Max, step=0.1)
#     return result