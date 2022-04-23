# get_position
# 获取车量节点的初始位置以及运动轨迹的变化情况
# 返回值：“车辆运动轨迹，车辆节点初试位置”
# 其中，“车辆运动轨迹”为一个矩阵，每一行元素分别为“时间，id，x，y，z”；“车辆节点初试位置”为一个矩阵，每一行元素为“id，x，y”
# update_node_position
# 节点位置的变化情况，共有6个元素，包括时间，节点编号，当前x坐标，当前y坐标，目的位置x坐标，目的位置y坐标,节点移动速度

import numpy as np
import re 
import matplotlib.pyplot as plt
import Init
import Global_Par as gp

# 获取车量节点的初始位置以及运动轨迹的变化情况
def get_position(mobile_file_path):
    x_max = 0
    y_max = 0
    z_max = 0
    with open(mobile_file_path, 'r') as f:
        movement_list = []
        init_position_list = []
        item_list = []
        key = 0
        # 遍历f中的每一行
        for line in f:
            line_list = re.split('[\s]', line) # 根据空白字符切割每一行
            #print(line_list)
            if line_list[5] != 'set':
                item_list.append(int(float(line_list[2]))) # 时间
                item_list.append(float(line_list[3][8:-1])) # id
                if float(line_list[5]) > x_max:
                    x_max = float(line_list[5]) # x坐标
                if float(line_list[6]) > y_max:
                    y_max = float(line_list[6]) # y坐标
                if float(line_list[7][0:-1]) > z_max:
                    z_max = float(line_list[7][0:-1]) # z坐标 （表示除了最后一个元素读取全部）
                item_list.append(float(line_list[5]))
                item_list.append(float(line_list[6]))
                item_list.append(float(line_list[7][0:-1]))
                # 向item_list中依次添加本行 时间、id、x、y、z
                # 然后将该列表存入列表movement_list中
                movement_list.append(item_list)
                item_list = []
            else:
                key = key + 1
                # 将节点编号写入列表
                if key % 3 == 1:
                    item_list.append(int(line_list[2][7:-1]))  # id
                # 将节点的位置(x,y)写入列表
                if key % 3 != 0:
                    item_list.append(float(line_list[7])) # x
                if key % 3 == 0:
                    item_list.append(float(line_list[7])) # y
                    # 向item_list中依次添加 id、x、y
                    # 然后将该列表（代表一辆车的坐标）添加到列表init_position_list中
                    init_position_list.append(item_list)
                    item_list = []
        # print(x_max)
        # print(y_max)
        # print(z_max)
        movement_matrix = np.mat(movement_list) # 创建矩阵
        init_position_matrix = np.mat(init_position_list)
        return movement_matrix, init_position_matrix


# node_position节点位置的变化情况，共有6个元素，包括时间，节点编号，当前x坐标，当前y坐标，目的位置x坐标，目的位置y坐标,节点移动速度
def update_node_position(movement_matrix, node_position, start_t, update_period, animation, nodelist, com_nodelist, controller):

    print('开始时间:', start_t)
    active_route = []
    current_move = movement_matrix[np.nonzero(movement_matrix[:, 0].A == start_t)[0], :]
    print(current_move)
    for value in current_move:
        for i in range(2, 4):
            node_position[int(value[0, 1]), i+2] = value[0, i]
    speed_x = node_position[:, 4] - node_position[:, 2]
    speed_y = node_position[:, 5] - node_position[:, 3]
    for i in range(0, int(1.0/gp.update_period)):
        node_position[:, 2] = node_position[:, 2] + speed_x * gp.update_period
        node_position[:, 3] = node_position[:, 3] + speed_y * gp.update_period
        node_id_position = node_position[:, [1, 2, 3]]
        if nodelist == [] or com_nodelist == []:
            nodelist.extend(Init.init_node(node_id_position, controller))
            com_nodelist.extend(Init.get_communication_node(node_id_position.shape[0]))
            print('所有通信节点:', com_nodelist) 
#         active_route = simulation(node_id_position,nodelist,com_nodelist,i,active_route)
#         print(active_route)
        if animation:
            plt.clf()
            plt.plot(node_position[:, 2], node_position[:, 3], '.m')
            plt.pause(0.01)
