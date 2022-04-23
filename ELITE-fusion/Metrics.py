import math
import Global_Par as Gp

# 道路车辆密度
# 输入：车辆数，路长
def density(veh_num, road_len):
    dens = veh_num/road_len
    return dens

# Gp.adjacency_dis, Gp.junction_dis 为公共信息
# 其他的需要传参

#-------------------efficiency-----------------------

# R_len
# 输入：当前路口id，指定邻居路口id
def R_len(c_id, n_id):
    l_cn = Gp.adjacency_dis[c_id][n_id]
    l_list = []
    for k in Gp.adjacency_dis[c_id]:
        l_list.append(Gp.adjacency_dis[c_id][k])
    l_max = max(l_list)
    f1 = 1-(l_cn/l_max)
    return f1

# R_traf
def R_traf(c_id, n_id, road_veh_num, road_veh_num_ow):
    e_ = road_veh_num_ow[c_id][n_id]
    e = road_veh_num[c_id][n_id]
    f2 = 1 / (1+math.exp(-(2 * e_ - e) / 2))
    return f2

# J_dis
def J_dis(c_id, n_id, d_id):
    l_cd = Gp.junction_dis[c_id][d_id]
    l_nd = Gp.junction_dis[n_id][d_id]
    f3 = 1 - min(l_nd/l_cd, 1)
    return f3

#--------------------stability------------------------

# J_dens
# 输入：controller.road_veh_num
def J_dens(c_id, n_id, road_veh_num):
    dens_n = 0
    dens_sum = 0
    for neib in Gp.adjacents_comb[c_id]:
        sum = 0
        for nn in Gp.adjacents_comb[neib]:
            sum += density(road_veh_num[neib][nn], Gp.adjacency_dis[neib][nn])
        avg = sum / len(Gp.adjacents_comb[neib])
        dens_sum += avg
        if n_id == neib:
            dens_n = avg
    dens_avg = dens_sum / len(Gp.adjacents_comb[c_id])
    f4 = min(dens_n/dens_avg, 1)
    return f4

# R_dens
# 输入：controller.road_veh_num
def R_dens(c_id, n_id, road_veh_num):
    dens_cn = density(road_veh_num[c_id][n_id], Gp.adjacency_dis[c_id][n_id])
    dens_sum = 0
    for neib in Gp.adjacents_comb[c_id]:
        dens_sum += density(road_veh_num[c_id][neib], Gp.adjacency_dis[c_id][neib])
    dens_avg = dens_sum / len(Gp.adjacents_comb[c_id])
    f5 = min(math.log(1+dens_cn/dens_avg),1)
    return f5

# V_space
# 输入：controller.all_node_neighbor, controller.veh_
def V_space(c_id, n_id, neib_list, veh_):
    e = len(veh_[c_id][n_id])
    sum = 0
    for veh in veh_[c_id][n_id]:
        num = 0
        for neib in neib_list[veh]:
            if neib in veh_[c_id][n_id]:
                num = num + 1
        sum += num / e
    f6 = sum / e
    return f6

#----------------------load--------------------------

# R_redu
# 输入：Q_table
def R_redu(c_id, n_id, d_id, Q_table):
    Q = Q_table[d_id][c_id][n_id]
    Q_sum = sum(Q_table[d_id][c_id])
    f7 = 1 - (1 / 5) * math.exp(2 * Q / Q_sum)
    return f7

# R_load
# 输入：controller.road_veh_num, 
def R_load(c_id, n_id, road_veh_num, buffer_ilst):

    return

# J_redu
# 输入：Q_table
def J_redu(n_id, d_id, Q_table):
    Q_r = 0
    for neib in Gp.adjacents_comb[n_id]:
        sum1 = sum(Q_table[d_id][neib])
        Q_r += Q_table[d_id][neib][n_id] / sum1
    f9 = 1 - 1 / (1 + 2 * Q_r)
    return f9

