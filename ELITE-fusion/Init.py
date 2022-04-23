# init_node
# 初始化节点,创建节点对象,并将各个节点的初始位置和节点编号赋值
# init_controller
# 初始化控制器
# get_communication_node
# 获取通信节点

import Node as Nd
import SDVN_Controller as Sc
import random
import re
import Global_Par as Gp

# 初始化节点列表。创建节点对象,并将各个节点的初始位置和节点编号赋值
def init_node(node_id_position, controller):
    node_list = []
    # 对每一个车辆节点创建节点对象并添加到列表中
    for i in range(node_id_position.shape[0]): # .shape获取矩阵行数，表示车辆节点数目
        node_list.append(Nd.Node(int(node_id_position[i][0, 0]), controller))
    return node_list

# 初始化控制器
def init_controller(node_num, intersection):
    return Sc.SDVNController(node_num, intersection)

# 获取通信的节点，得到n对 数据包收/发节点（自写）
def get_communication_node(node_num, n):
    com_nodelist = [] # 通信节点列表
    #error = [0,2,6,56,61] #失效节点id
    while True:
    # for i in range(node_num):
        if len(com_nodelist) < n:
            # random.random()生成0和1之间的随机浮点数float
            node1_id = round(random.random() * node_num)   # 随机生成一个节点id
            node2_id = round(random.random() * node_num)
            #if node1_id not in error and node2_id not in error:
            com_nodelist.append([node1_id, node2_id])
        else: # 通信节点列表已满，结束
            break
    # 返回 n/2 对通信节点
    return com_nodelist