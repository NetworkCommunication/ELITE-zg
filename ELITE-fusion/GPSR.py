from math import *
import Global_Par as Gp

# 计算两节点之间的距离
def getdis(ax, ay, bx, by):
    temp_x = ax - bx
    temp_y = ay - by
    temp_x = temp_x * temp_x
    temp_y = temp_y * temp_y
    result = sqrt(temp_x+temp_y)
    return result

# 基于给定线相对角度计算绝对角度
def angle(x1, y1, x2, y2):
    line_len = sqrt((x2-x1)**2 + (y2-y1)**2)
    if line_len == 0:
        # print("2 nodes are the same\n")
        return 0
    sin_theta = (y2-y1)/line_len
    cos_theta = (x2-x1)/line_len
    theta = acos(cos_theta)
    if sin_theta < 0:
        theta = 2*pi - theta
    return theta

# 检查两条线是否在本地交叉
def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    if min(x1, x2)<=max(x3, x4) and min(x3, x4)<=max(x1, x2) and \
        min(y1, y2)<=max(y3, y4) and min(y3, y4)<=max(y1, y2):

        u = (x3-x1)*(y2-y1) - (x2-x1)*(y3-y1)
        v = (x4-x1)*(y2-y1) - (x2-x1)*(y4-y1)
        w = (x1-x3)*(y4-y3) - (x4-x3)*(y1-y3)
        z = (x2-x3)*(y4-y3) - (x4-x3)*(y2-y3)
        if u*v <0 and w*z<0:
            return 1
    return 0

# 贪婪转发,返回选择下一跳节点id
def gf_nexthop(node_id, neib_list, des_id, node_list):
    current = node_list[node_id] # 当前节点
    destination = node_list[des_id] # 目的节点
    nexthop = -1
    mindis = getdis(current.position[0], current.position[1], destination.position[0], destination.position[1])
    # 遍历邻居节点
    for node in neib_list:
        nx = node_list[node].position[0] # 邻居节点x坐标
        ny = node_list[node].position[1] # 邻居节点y坐标
        tempdis = getdis(nx, ny, destination.position[0], destination.position[1])
        if tempdis < mindis:
            mindis = tempdis
            nexthop = node
    # 返回选定的下一跳id
    return nexthop

# gg平面化
def gg_planarize(node_id, neib_list, node_list):
    result = []
    current = node_list[node_id]  # 当前节点
    for node in neib_list:
        flag = 1
        midpx = current.position[0] + (node_list[node].position[0] - current.position[0])/2
        midpy = current.position[1] + (node_list[node].position[1] - current.position[1])/2
        mdis = getdis(current.position[0], current.position[1], midpx, midpy)  # 圆半径
        for other in neib_list: # 判断邻居表中所有节点是否在圆的范围内
            if node_list[other].node_id != node_list[node].node_id:
                tempdis = getdis(midpx, midpy, node_list[other].position[0], node_list[other].position[1])
                if tempdis < mdis:
                    flag = 0
                    break
        if flag == 1: # 在圆范围内不存在节点，可以选择index节点
            result.append(node)
    return result

# 周边转发，返回下一跳节点id
def peri_nexthop(node_id, neib_list, des_id, node_list, last):
    current = node_list[node_id]
    destination = node_list[des_id]
    #source = node_list[sou_id]
    nexthop = node_id # 先把下一跳设置为本节点
    planar_neighbors = gg_planarize(node_id, neib_list, node_list) # gg平面化
    if last > -1: # 存在上一跳节点
        lastnb = node_list[last]
        if lastnb == None:
            print("Wrong last nb %d -> %d \n" % (last, node_id))
            return -1
        alpha = angle(current.position[0], current.position[1], node_list[last].position[0], node_list[last].position[1]) # 计算当前节点与上一跳节点连线的夹角
    else: # 不存在上一跳节点
        alpha = angle(current.position[0], current.position[1], destination.position[0], destination.position[1]) # 计算当前节点与目的节点的连线
    minagle = 10000
    for temp_id in planar_neighbors:
        temp = node_list[temp_id]
        if temp.node_id != last:
            delta = angle(current.position[0], current.position[1], temp.position[0], temp.position[1])
            delta = delta - alpha
            # print(temp.getid(), delta, last)
            # 选取逆时针方向的节点，
            # 且“当前节点与邻居节点连线” 与“当前节点与目的节点连线”或“当前节点与上一跳节点连线”
            # 的夹角是最小的
            if delta < 0.0 :
                delta = 2*pi + delta
            if delta < minagle:
                minagle = delta
                nexthop = temp.node_id
    next = node_list[nexthop]
    if next == None:
        return -1
    # if len(neib_list)>1 and intersect(current.position[0], current.position[1], next.position[0], next.position[1], source.position[0], source.position[1], destination.position[0], destination.position[1]):
    #    return peri_nexthop(node_id, neib_list, des_id, node_list, sou_id, nexthop)
    return nexthop

# 转发数据包
def find_next(node_id, neib_list, des_id, node_list):
    forward_type = 0
    current = node_list[node_id]  # 当前节点
    destination = node_list[des_id]  # 目的节点
    # 上一次是周边转发
    if Gp.forward_type != 2:
        nexthop = peri_nexthop(node_id, neib_list, des_id, node_list, -1)
        Gp.forward_type -= 1
    # 上一次不是周边转发
    else:
        mindis = getdis(current.position[0], current.position[1], destination.position[0], destination.position[1])
        # 判断转发方式，根据判断结果选择贪婪/周边转发
        for neib in neib_list: # 遍历邻居表
            dis = getdis(node_list[neib].position[0], node_list[neib].position[1], destination.position[0], destination.position[1])
            if dis<mindis:
                forward_type = 1 # 存在比当前节点更靠近目的节点的节点，贪婪转发
                break
        # 根据判断结果选择选择下一跳的方式
        if forward_type == 1:
            nexthop = gf_nexthop(node_id, neib_list, des_id, node_list)
        else:
            nexthop = peri_nexthop(node_id, neib_list, des_id, node_list, -1)
            Gp.forward_type -= 1
    # 连续周边转发3次，就不限制了
    if Gp.forward_type == 0:
        Gp.forward_type = 2
    # 返回下一跳节点的id
    return nexthop






########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
# # mmgpsr周边转发
# def peri_nexthop(node_id, neib_list, des_id, node_list):
#     current = node_list[node_id]  # 当前节点
#     destination = node_list[des_id]  # 目的节点
#     next_hop = -1  # 选择的下一跳节点的id
#     min_theta = 100
#     planar_neighbors = gg_planarize(node_id, neib_list, node_list)
#     for neib in planar_neighbors:
#     #for neib in neib_list:
#         node = node_list[neib]
#         delta_cd = angle(current.position[0], current.position[1], destination.position[0], destination.position[1]) # 当前节点与目的节点连线的绝对角度
#         delta_cn = angle(current.position[0], current.position[1], node.position[0], node.position[1]) # 当前节点与邻居节点连线的绝对角度
#         delta = delta_cn-delta_cd
#         # 根据c在以sd为y轴的不同象限来确定sd与sc的夹角
#         # 这时候要根据sd的绝对角度（sd是在x轴上还是下）来区别不同的角度计算方法。
#         if delta_cd>0 and delta_cd<pi:
#             if delta<0:
#                 theta = -delta
#             elif delta>0 and delta<pi:
#                 theta = delta
#             else:
#                 theta = 2*pi - delta
#         else:
#             if delta > 0:
#                 theta = delta
#             elif delta < 0 and delta > -pi:
#                 theta = -delta
#             else:
#                 theta = 2*pi + delta
#         # 找出sc 和 sd 夹角最小的c
#         if min_theta > theta:
#             min_theta = theta
#             next_hop = neib
#     return next_hop


