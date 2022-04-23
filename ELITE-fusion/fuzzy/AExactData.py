import math
import numpy as np
import Global_Par as Gp
from math import *

# 角度
# cos值为-1到1，acos为0到pi
# 表现出来的是一种是否同向的关系
def angle(x0, y0, x1, y1, x2, y2):
    cos = ((x1-x0)*(x2-x0)+(y1-y0)*(y2-y0))/(sqrt(pow(x1-x0, 2)+pow(y1-y0, 2))*sqrt(pow(x2-x0, 2)+pow(y2-y0, 2)))
    theta = acos(cos)/pi
    return theta

# 距离
def getdis(ax, ay, bx, by):
    temp_x = ax - bx
    temp_y = ay - by
    temp_x = temp_x * temp_x
    temp_y = temp_y * temp_y
    result = sqrt(temp_x+temp_y)
    return result

# 当前路口与邻居之间的连通性
# input: 当前路口id，邻居路口id，分段车数[num, num,...]，邻居间分段距离len
def connectivity(part_num, part_length):
    connectivity_crisp = 0 # 连通性-精确值
    density = 0 # 分段密度和
    for num in part_num:
        part_den = num / part_length # 分段密度
        density += part_den
    connectivity_crisp = density / len(part_num)
    return connectivity_crisp

# 相对于当前路口，其邻居路口距离目的路口更近的程度
# 输入：当前路口id，邻居路口id, 目的路口id
def valid_distance(current_area, adjacent_area, target_area):
    #print(current_area, adjacent_area, target_area)
    valid_distance_crisp = 0 # 有效距离-准确值
    # 当前区域的坐标
    current_x = Gp.it_pos[current_area][0]
    current_y = Gp.it_pos[current_area][1]
    # 目的区域的坐标
    target_x = Gp.it_pos[target_area][0]
    target_y = Gp.it_pos[target_area][1]
    # 邻居区域的坐标
    adjacency_x = Gp.it_pos[adjacent_area][0]
    adjacency_y = Gp.it_pos[adjacent_area][1]
    # 分别计算c-t和a-t的距离
    dis_current_to_target = getdis(current_x, current_y, target_x, target_y) # 当前区域到目的区域的距离
    dis_adjacency_to_target = getdis(adjacency_x, adjacency_y, target_x, target_y) # 邻居区域到目的区域的距离
    # 距离比值
    dis_ratio = dis_adjacency_to_target / dis_current_to_target
    # 连线c-t和c-n的夹角角度
    ang = angle(current_x, current_y, adjacency_x, adjacency_y, target_x, target_y) / pi
    # 计算加权精确值
    valid_distance_crisp = Gp.distance_a * dis_ratio + Gp.distance_b * ang
    if valid_distance_crisp > 1:
        valid_distance_crisp = 1
    return valid_distance_crisp

# 邻居区域车辆密度分布状况
# 输入：与不同邻居间半程车数[num1,...]，与多个邻居间半程距离[len1,...]
def distribution(half_num, half_length):
    distribution_crisp = 0 # 分布-精确值
    density = 0 # 多条道路的密度和
    for i in range(len(half_num)):
        part_den = half_num[i] / half_length[i] #单条道路车辆密度
        density += part_den
    distribution_crisp = density / len(half_num)
    return distribution_crisp

# 计算得到三个attribute的值
def crisp(current, adjacent, target, intra_vehicles_number, intra_path_length, inter_vehicles_number, inter_part_length):
    distribution_list = []
    # 计算adjacent的distribution的原始值
    half_num = intra_vehicles_number[adjacent]  # 一个列表[]
    half_length = intra_path_length[adjacent]  # []
    distribution_crisp = distribution(half_num, half_length)
    # 计算current到adjacent的connectivity的原始值
    part_num = inter_vehicles_number[current][adjacent]  # 列表 []
    part_length = inter_part_length[current][adjacent]  # float
    connectivity_crisp = connectivity(part_num, part_length)

    conn_sum = 0
    distr_sum = 0
    # 计算current所有邻居的distribution和connectivity
    for ne in Gp.adjacents_comb[current]:
        part_num_ne = inter_vehicles_number[current][ne]  # 列表 []
        part_length_ne = inter_part_length[current][ne]  # float
        half_num_ne = intra_vehicles_number[ne]  # 一个列表[]
        half_length_ne = intra_path_length[ne]  # []
        conn_crisp = connectivity(part_num_ne, part_length_ne)
        dist_crisp = distribution(half_num_ne, half_length_ne)
        distribution_list.append(dist_crisp)
        conn_sum += conn_crisp # 求current和所有邻居的connectivity和
        distr_sum += dist_crisp # 求current的所有邻居的distribution和
    conn_avg = conn_sum / len(Gp.adjacents_comb[current])
    dist_avg = distr_sum / len(Gp.adjacents_comb[current])
    dist_max = max(distribution_list)

    if conn_avg == 0:
        final_connectivity = 0
    else:
        final_connectivity = min(math.log(1 + connectivity_crisp / conn_avg), 1)
    if dist_avg == 0:
        final_distribution = 0
    else:
        final_distribution = min((distribution_crisp / dist_avg) - (distribution_crisp / dist_max), 1)
    final_distance = valid_distance(current, adjacent, target)
    return final_connectivity, final_distribution, final_distance

# # 归一化后的分布清晰输入
# def nor_distribution_crisp(half_num, half_length):
#     pri_distribution_crisp = distribution(half_num, half_length)
#     # distribution_crisp = 1 - math.exp(
#     #     - math.pow((pri_distribution_crisp - Gp.distribution_min[Gp.nor_para_seq]) / Gp.distribution_var[Gp.nor_para_seq], 2))
#     distribution_crisp = (pri_distribution_crisp - Gp.distribution_min[Gp.nor_para_seq]) / (Gp.distribution_max[Gp.nor_para_seq] - Gp.distribution_min[Gp.nor_para_seq])
#     return distribution_crisp
#
# # 归一化后的连通性清晰输入
# def nor_connectivity_crisp(part_num, part_length):
#     pri_connectivity_crisp = connectivity(part_num, part_length)
#     connectivity_crisp = 1 / 2 + (1 / 2) * math.sin((math.pi / (Gp.connectivity_max[Gp.nor_para_seq] - Gp.connectivity_min[Gp.nor_para_seq])) \
#                          * (pri_connectivity_crisp - (
#                 Gp.connectivity_min[Gp.nor_para_seq] + Gp.connectivity_max[Gp.nor_para_seq]) / 2))
#     return connectivity_crisp
#
# # 归一化后的有效距离清晰输入
# def nor_valid_distance_crisp(current_area, adjacent_area, target_area):
#     pri_valid_distance_crisp = valid_distance(current_area, adjacent_area, target_area)
#     alpha = 1.4
#     beta = 2
#     valid_distance_crisp = 1 - (1 / (1 + alpha * pow(pri_valid_distance_crisp - alpha, beta)))
#     return valid_distance_crisp


# # 分布清晰输入
# def final_distribution_crisp(half_num, half_length):
#     pri_distribution_crisp = distribution(half_num, half_length)
#
#     return distribution_crisp
#
# # 连通性清晰输入
# def final_connectivity_crisp(part_num, part_length):
#     pri_connectivity_crisp = connectivity(part_num, part_length)
#
#     return connectivity_crisp
#
# # 有效距离清晰输入
# def final_valid_distance_crisp(current_area, adjacent_area, target_area):
#     pri_valid_distance_crisp = valid_distance(current_area, adjacent_area, target_area)
#
#     return valid_distance_crisp