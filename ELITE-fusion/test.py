import Get_Move as Gm
import Init
import numpy as np
import Global_Par as Gp
import time as t
import traffic as rntfa
import random
import matplotlib.pyplot as plt
import copy
from math import *
node_list = [] # 所有节点
com_node_list = [] # 通信的节点
begin_time = 290 # 仿真开始时间
sim_time = 300 # 仿真结束阈值
valid_nodes_num = [] # 有效节点数

# 距离
def getdis(ax, ay, bx, by):
    temp_x = ax - bx
    temp_y = ay - by
    temp_x = temp_x * temp_x
    temp_y = temp_y * temp_y
    result = sqrt(temp_x+temp_y)
    return result

if __name__ == '__main__':
    # 选择移动文件
    for u in [0,1,2,3,4]:
        Gp.nor_para_seq = u
        if u==0:
            movement_file = "de-500.mobility.tcl" #  350 14p/s
            pkt_num = 16
            begin_time = 80
            sim_time = 100
        elif u==1:
            movement_file = "de-1000.mobility.tcl" # 700 27p/s
            pkt_num = 24
            begin_time = 120
            sim_time = 140
        elif u==2:
            movement_file = "de-1500.mobility.tcl" # 1050 40p/s
            pkt_num = 40
            begin_time = 120
            sim_time = 140
        elif u==3:
            movement_file = "de-2000.mobility.tcl" # 1400 54p/s
            pkt_num = 56
            begin_time = 240
            sim_time = 260
        elif u == 4:
            movement_file = "de-2500.mobility.tcl"  # 2000 67p/s
            pkt_num = 68
            begin_time = 350
            sim_time = 370
        # elif u==5:
        #     movement_file = "de-3000.mobility.tcl" # 2400 80p/s
        #     pkt_num = 80
        # elif u==6:
        #     movement_file = "de-3500.mobility.tcl" # 3200 107p/s
        #     pkt_num = 108
        # elif u==7:
        #     movement_file = "de-4000.mobility.tcl" # 4000 134p/s
        #     pkt_num = 136
        else:
            print('wrong~')
            movement_file = 'de-1000.mobility.tcl'
            pkt_num = 24

        # 位置文件读取
        # get_position()获取“车辆运动轨迹，车辆节点初始位置”
        # 其中，“车辆运动轨迹”为一个矩阵，每一行元素分别为“时间，id，x，y，z”；“车辆节点初始位置”为一个矩阵，每一行元素为“id，x，y”
        print("get movement...")
        movement_matrix, init_position_matrix = Gm.get_position(movement_file)
        node_num = init_position_matrix.shape[0]  # 矩阵第一维的数量（行数），表示车辆节点数量

        # 位置数据处理
        # 对车辆节点初始位置矩阵进行处理：按照第一列（id）的顺序进行排序
        init_position_arranged = init_position_matrix[np.lexsort(init_position_matrix[:, ::-1].T)]
        node_position = init_position_arranged[0]

        # 路口 {it_1:[x,y], it_2:[x,y], ..., it_n:[x,y]}
        Gp.intersection = rntfa.junction()
        Gp.edges_boundary = rntfa.edge()
        Gp.adjacents = rntfa.adjacent(Gp.edges_boundary, Gp.intersection)
        Gp.it_pos = copy.deepcopy(Gp.intersection)
        Gp.adjacents_comb = copy.deepcopy(Gp.adjacents)

        # rntfa.intersection_combination(Gp.intersection) # intersections_combination：[[],[],...]
        # rntfa.combination() # it_pos
        # rntfa.comb_adjacent() # adjacents_comb

        # 限制
        Gp.it_pos, Gp.adjacents_comb = rntfa.process(Gp.it_pos, Gp.adjacents_comb, 300, 2100, 0, 1600)
        Gp.adjacents_comb[1481558096].append(1481558100)
        Gp.adjacents_comb[1481558096].remove(1481558098)
        Gp.adjacents_comb[1481558100].remove(1481558098)
        Gp.adjacents_comb[1481558100].append(1481558096)
        Gp.it_pos.pop(1481558098)
        Gp.adjacents_comb.pop(1481558098)
        print("intersections: ", Gp.it_pos)
        print("adjacency: ", Gp.adjacents_comb)
        print("number of intersections: ", len(Gp.it_pos))
        rntfa.junction_dis()  # 路口间距离
        rntfa.adjacency_dis()  # 相邻路口间路长

        x = []
        y = []
        txt = []
        for it, pos in Gp.it_pos.items():
            txt.append(it)
            x.append(pos[0])
            y.append(pos[1])
        plt.scatter(x, y)
        for i in range(len(x)):
            plt.annotate(txt[i], xy=(x[i], y[i]), xytext=(x[i] + 0.5, y[i] + 0.5))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.show()
        # exit(0)

        # 控制器初始化
        controller = Init.init_controller(node_num, Gp.it_pos)

        controller.table_fusion()

        # 节点初始化，获得车辆节点列表node_list，列表中每一个元素代表一个节点,具有自己的id
        node_list = (Init.init_node(node_position, controller))

        # 计算时间，时延，抖动初始化
        effi = 0
        delay = 0
        std2 = 0

        # 多次训练
        for x in range(1):
            Gp.tag = x
            for y in range(1):
                Gp.tag = x
                start_time = t.time() # 获取开始时间
                # 在begin_time到sim_time时间段内仿真
                for time in range(begin_time, sim_time): #sim_time
                #for time in range(450, 451):
                    print('\nTime: %d'% time) # 打印当前时刻（200-sim_time）
                    # np.nonzero()返回数组中非零元素的索引值数组
                    # .A 将矩阵转化为数组类型
                    # 这里是将“车辆运动轨迹”中时间为当前time的所有行取出存放到current_move中 （==time 为 true）
                    current_move = movement_matrix[np.nonzero(movement_matrix[:, 0].A == time)[0], :]
                    # 更新节点位置
                    for value in current_move:
                        for i in range(1, 4): # 0:id, 1:x, 2:y, 3:z
                            node_position[int(value[0, 1]), i] = value[0, i+1]
                    # 截取 (x,y,z) 坐标，用于下面节点位置更新
                    node_id_position = node_position[:, [1, 2, 3]]

                    # 所有节点更新位置，并发送hello至控制器
                    # 所有节点广播hello包，向控制器报告位置
                    for node in node_list:
                        node.update_node_position(node_id_position)
                        node.generate_hello_c(controller) # 控制器

                    # 控制器更新网络全局情况
                    controller.predict_position() # 节点信息更新了，控制器也要根据hello列表的信息更新全局记录

                    # 控制器获取区域和车的关系
                    controller.analyze()

                    # # 最开始初始化路由表，此后一个时间段内根据路由情况更新路由表
                    # if time == begin_time: #and x == 0:
                    #     controller.init_routing_table()

                    # 控制器向所有节点发送其所属区域信息
                    controller.send_area_info(node_list)

                    # 所有节点广播hello包，向其他节点报告自身信息
                    for node in node_list:
                        node.generate_hello_n(node_list) # 其他节点

                    # 每个节点更新邻居表情况(包括邻居的基本信息以及所属区域信息)
                    for node in node_list:
                        node.update_neighbor_list()

                    # 每秒发送多个数据包，选择数据发送节点和接收节点对:
                    b = int(pkt_num / 4)
                    b1 = 0
                    b2 = b
                    b3 = 2 * b
                    b4 = 3 * b
                    for yy in range(0, pkt_num):
                        if yy == b1:
                            print("-----------------0-375----------------------")
                        if yy == b2:
                            print("---------------375-750-------------------------")
                        if yy == b3:
                            print("----------------750-1125---------------------------")
                        if yy == b4:
                            print("-----------------1125-1500---------------------------")

                        if yy == b1 or yy == b2 or yy == b3 or yy == b4:
                            temp = Gp.success_time

                        source_id = -1
                        destination_id = -1
                        # 由远到近选择区域对，并在区域对中选择节点对
                        if yy >= b1 and yy < b2:
                            Gp.delay_hop_tag = 800
                            d_min = 0
                            d_max = 375
                        elif yy >= b2 and yy < b3:
                            Gp.delay_hop_tag = 1600
                            d_min = 375
                            d_max = 750
                        elif yy >= b3 and yy < b4:
                            Gp.delay_hop_tag = 2400
                            d_min = 750
                            d_max = 1125
                        else:
                            Gp.delay_hop_tag = 3200
                            d_min = 1125
                            d_max = 1500
                        # 随机选择区域对
                        while 1:
                            source_area = random.choice(list(Gp.it_pos))
                            candidate = []
                            for it, pos in Gp.it_pos.items():
                                x1 = Gp.it_pos[source_area][0]
                                y1 = Gp.it_pos[source_area][1]
                                x2 = pos[0]
                                y2 = pos[1]
                                d1 = getdis(x1, y1, x2, y2)
                                if d1 >= d_min and d1 <= d_max:
                                    candidate.append(it)
                            # 在区域对中选择
                            while candidate:
                                destination_area = random.choice(candidate)
                                if controller.junc_veh[source_area] and controller.junc_veh[destination_area]:
                                    source_id = random.choice(controller.junc_veh[source_area])
                                    destination_id = random.choice(controller.junc_veh[destination_area])
                                    break
                                candidate.remove(destination_area)
                            if source_id != -1 and destination_id != -1:
                                break

                        node_list[source_id].generate_request(destination_id, controller, 1024)

                        # 控制器处理路由请求
                        controller.resolve_request(node_list)

                        # 源节点发送数据包
                        node_list[source_id].forward_pkt(node_list, controller)

                        if yy == b2 - 1:
                            Gp.success_0_800 += Gp.success_time - temp
                        elif yy == b3-1:
                            Gp.success_800_1600 += Gp.success_time - temp
                        elif yy == b4-1:
                            Gp.success_1600_2400 += Gp.success_time - temp
                        elif yy == pkt_num-1:
                            Gp.success_2400_3200 += Gp.success_time - temp
                        else:
                            continue

                    # for sor_area in Gp.it_pos:
                    #     for des_area in Gp.it_pos:
                    #         source_id = -1
                    #         destination_id = -1
                    #         if controller.junc_veh[sor_area] and controller.junc_veh[des_area]:
                    #             source_id = random.choice(controller.junc_veh[sor_area])
                    #             destination_id = random.choice(controller.junc_veh[des_area])
                    #         else:
                    #             continue
                    #     # 源节点发出路由请求（目的节点，控制器，包大小）
                    #     # 包大小为1024 bytes 总带宽为1930M byte ps = 1930 * 1024 * 1024 byte/s = 1930 * 2^20 bytes/s
                    #     # 1930*1024 = 1976320
                    #     # channel bandwidth = 6Mbps = 0.75 * 1024 * 1024 byte/s = 768 * 1024 byte/s
                    #         node_list[source_id].generate_request(destination_id, controller, 1024)
                    #
                    #     # 控制器处理路由请求
                    #         controller.resolve_request(node_list)
                    #
                    #     # 源节点发送数据包
                    #         node_list[source_id].forward_pkt(node_list, controller)
                    #
                    #     # if y==b2-1:
                    #     #     Gp.success_0_800 += Gp.success_time - temp
                    #     # elif y==b3-1:
                    #     #     Gp.success_800_1600 += Gp.success_time - temp
                    #     # elif y==b4-1:
                    #     #     Gp.success_1600_2400 += Gp.success_time - temp
                    #     # elif y==pkt_num-1:
                    #     #     Gp.success_2400_3200 += Gp.success_time - temp
                    #     # else:
                    #     #     continue

                    # 控制器处理汇报信息，更新路由表
                    controller.resolve_report()

                    # Gp.co_count += pkt_num
                    Gp.co_list.append(Gp.co_count * 2 + pkt_num)  # (len(data_pkt.path))
                    # if Gp.delay_hop_tag == 800:
                    #     Gp.co_list_800.append(c_message)
                    # elif Gp.delay_hop_tag == 1600:
                    #     Gp.co_list_1600.append(c_message)
                    # elif Gp.delay_hop_tag == 2400:
                    #     Gp.co_list_2400.append(c_message)
                    # elif Gp.delay_hop_tag == 3200:
                    #     Gp.co_list_3200.append(c_message)
                    Gp.co_count = 0

                # 一轮仿真结束，获取结束时间
                end_time = t.time()

                # 数据包时延
                Gp.total_pkt_delay[x] = Gp.pkt_delay
                Gp.total_pkt_delay_800[x] = Gp.pkt_delay_800
                Gp.total_pkt_delay_1600[x] = Gp.pkt_delay_1600
                Gp.total_pkt_delay_2400[x] = Gp.pkt_delay_2400
                Gp.total_pkt_delay_3200[x] = Gp.pkt_delay_3200
                # 数据包跳数
                Gp.total_hop_list[x] = Gp.hop_list
                Gp.total_hop_list_800[x] = Gp.hop_list_800
                Gp.total_hop_list_1600[x] = Gp.hop_list_1600
                Gp.total_hop_list_2400[x] = Gp.hop_list_2400
                Gp.total_hop_list_3200[x] = Gp.hop_list_3200
                # 开销
                Gp.total_oh_list[x] = Gp.oh_list
                Gp.total_oh_list_800[x] = Gp.oh_list_800
                Gp.total_oh_list_1600[x] = Gp.oh_list_1600
                Gp.total_oh_list_2400[x] = Gp.oh_list_2400
                Gp.total_oh_list_3200[x] = Gp.oh_list_3200
                # 开销CO
                Gp.total_co_list[x] = Gp.co_list
                # Gp.total_co_list_800[x] = Gp.co_list_800
                # Gp.total_co_list_1600[x] = Gp.co_list_1600
                # Gp.total_co_list_2400[x] = Gp.co_list_2400
                # Gp.total_co_list_3200[x] = Gp.co_list_3200

                # 数据包
                print("success num:", Gp.success_time)
                print("loss num:", Gp.fail_time)
                print("loss in area selection:", Gp.loop_fail_time)
                #print("delay from generation to delivery or loss: ")

                # 记录单次仿真情况到列表
                Gp.success_time_list.append(Gp.success_time)
                Gp.success_0_800_list.append(Gp.success_0_800)
                Gp.success_800_1600_list.append(Gp.success_800_1600)
                Gp.success_1600_2400_list.append(Gp.success_1600_2400)
                Gp.success_2400_3200_list.append(Gp.success_2400_3200)
                Gp.fail_time_list.append(Gp.fail_time)
                Gp.loop_file_time_list.append(Gp.loop_fail_time)
                # 清空临时存储
                Gp.success_time = 0
                Gp.success_0_800 = 0
                Gp.success_800_1600 = 0
                Gp.success_1600_2400 = 0
                Gp.success_2400_3200 = 0
                Gp.fail_time = 0
                Gp.loop_fail_time = 0
                Gp.pkt_delay = []
                Gp.pkt_delay_800 = []
                Gp.pkt_delay_1600 = []
                Gp.pkt_delay_2400 = []
                Gp.pkt_delay_3200 = []
                Gp.hop_list = []
                Gp.hop_list_800 = []
                Gp.hop_list_1600 = []
                Gp.hop_list_2400 = []
                Gp.hop_list_3200 = []
                Gp.oh_list = []
                Gp.oh_list_800 = []
                Gp.oh_list_1600 = []
                Gp.oh_list_2400 = []
                Gp.oh_list_3200 = []
                Gp.co_list = []
                # Gp.co_list_800 = []
                # Gp.co_list_1600 = []
                # Gp.co_list_2400 = []
                # Gp.co_list_3200 = []

            # 在一个场景下进行多次仿真
            # 仿真结束后计算总值
            success = np.array(Gp.success_time_list)
            fail = np.array(Gp.fail_time_list)
            loop = np.array(Gp.loop_file_time_list)
            succ = np.sum(success) # 总成功次数
            total = np.sum(success) + np.sum(fail) + np.sum(loop) # 总数据包数
            ratio = round(succ / total,3) # 到达率
            success_800 = np.array(Gp.success_0_800_list)
            success_1600 = np.array(Gp.success_800_1600_list)
            success_2400 = np.array(Gp.success_1600_2400_list)
            success_3200 = np.array(Gp.success_2400_3200_list)
            succ_800 = np.sum(success_800)
            succ_1600 = np.sum(success_1600)
            succ_2400 = np.sum(success_2400)
            succ_3200 = np.sum(success_3200)
            ratio_800 = round(succ_800 / (total / 4),3)
            ratio_1600 = round(succ_1600 / (total / 4),3)
            ratio_2400 = round(succ_2400 / (total / 4),3)
            ratio_3200 = round(succ_3200 / (total / 4),3)
            print("---------------total-------------------")
            # print(Gp.success_time_list, Gp.success_0_800_list, Gp.success_800_1600_list, Gp.success_1600_2400_list,
            #       Gp.success_2400_3200_list)
            print("generated packets: " , total)
            # print(ratio_800, ratio_1600, ratio_2400, ratio_3200)
            average_hop = [] # 每次仿真的平均跳数
            average_hop_800 = []
            average_hop_1600 = []
            average_hop_2400 = []
            average_hop_3200 = []
            average_delay = [] # 每次仿真的平均时延
            average_delay_800 = []
            average_delay_1600 = []
            average_delay_2400 = []
            average_delay_3200 = []
            average_oh = [] # 每次仿真平均开销
            average_oh_800 = []
            average_oh_1600 = []
            average_oh_2400 = []
            average_oh_3200 = []
            average_co = []  # 每次仿真CO平均开销
            # average_co_800 = []
            # average_co_1600 = []
            # average_co_2400 = []
            # average_co_3200 = []

            # 补全hop
            # for x_, hop_list in Gp.total_hop_list.items():
            #     max_hop = max(hop_list)
            #     for i_ in range(0, total-len(hop_list)):
            #         Gp.total_hop_list[x_].append(max_hop)
            # for x_, hop_list in Gp.total_hop_list_800.items():
            #     max_hop = max(hop_list)
            #     for i_ in range(0,int(total/4)-len(hop_list)):
            #         Gp.total_hop_list_800[x_].append(max_hop)
            # for x_, hop_list in Gp.total_hop_list_1600.items():
            #     max_hop = max(hop_list)
            #     for i_ in range(0,int(total/4)-len(hop_list)):
            #         Gp.total_hop_list_1600[x_].append(max_hop)
            # for x_, hop_list in Gp.total_hop_list_2400.items():
            #     max_hop = max(hop_list)
            #     for i_ in range(0,int(total/4)-len(hop_list)):
            #         Gp.total_hop_list_2400[x_].append(max_hop)
            # for x_, hop_list in Gp.total_hop_list_3200.items():
            #     max_hop = max(hop_list)
            #     for i_ in range(0,int(total/4)-len(hop_list)):
            #         Gp.total_hop_list_3200[x_].append(max_hop)
            # 计算hop
            for x_, hop_list in Gp.total_hop_list.items():
                hops = np.array(hop_list)
                average_hop.append(np.mean(hops))
            for x_, hop_list in Gp.total_hop_list_800.items():
                hops = np.array(hop_list)
                average_hop_800.append(np.mean(hops))
            for x_, hop_list in Gp.total_hop_list_1600.items():
                hops = np.array(hop_list)
                average_hop_1600.append(np.mean(hops))
            for x_, hop_list in Gp.total_hop_list_2400.items():
                hops = np.array(hop_list)
                average_hop_2400.append(np.mean(hops))
            for x_, hop_list in Gp.total_hop_list_3200.items():
                hops = np.array(hop_list)
                average_hop_3200.append(np.mean(hops))

            # 补全delay
            # for x_, delay_list in Gp.total_pkt_delay.items():
            #     max_delay = max(delay_list)
            #     for i_ in range(0, int(total/4)-len(delay_list)):
            #         Gp.total_pkt_delay[x_].append(max_delay)
            # for x_, delay_list in Gp.total_pkt_delay_800.items():
            #     max_delay = max(delay_list)
            #     for i_ in range(0, int(total/4)-len(delay_list)):
            #         Gp.total_pkt_delay_800[x_].append(max_delay)
            # for x_, delay_list in Gp.total_pkt_delay_1600.items():
            #     max_delay = max(delay_list)
            #     for i_ in range(0, int(total/4)-len(delay_list)):
            #         Gp.total_pkt_delay_1600[x_].append(max_delay)
            # for x_, delay_list in Gp.total_pkt_delay_2400.items():
            #     max_delay = max(delay_list)
            #     for i_ in range(0, int(total/4)-len(delay_list)):
            #         Gp.total_pkt_delay_2400[x_].append(max_delay)
            # for x_, delay_list in Gp.total_pkt_delay_3200.items():
            #     max_delay = max(delay_list)
            #     for i_ in range(0, int(total/4)-len(delay_list)):
            #         Gp.total_pkt_delay_3200[x_].append(max_delay)
            # 计算delay
            for x_, delay_list in Gp.total_pkt_delay.items():
                delays = np.array(delay_list)
                average_delay.append(np.mean(delays))
            for x_, delay_list in Gp.total_pkt_delay_800.items():
                delays = np.array(delay_list)
                average_delay_800.append(np.mean(delays))
            for x_, delay_list in Gp.total_pkt_delay_1600.items():
                delays = np.array(delay_list)
                average_delay_1600.append(np.mean(delays))
            for x_, delay_list in Gp.total_pkt_delay_2400.items():
                delays = np.array(delay_list)
                average_delay_2400.append(np.mean(delays))
            for x_, delay_list in Gp.total_pkt_delay_3200.items():
                delays = np.array(delay_list)
                average_delay_3200.append(np.mean(delays))

            # 计算开销
            for x_, oh_list in Gp.total_oh_list.items():
                oh = np.array(oh_list)
                average_oh.append(np.mean(oh))
            for x_, oh_list in Gp.total_oh_list_800.items():
                oh = np.array(oh_list)
                average_oh_800.append(np.mean(oh))
            for x_, oh_list in Gp.total_oh_list_1600.items():
                oh = np.array(oh_list)
                average_oh_1600.append(np.mean(oh))
            for x_, oh_list in Gp.total_oh_list_2400.items():
                oh = np.array(oh_list)
                average_oh_2400.append(np.mean(oh))
            for x_, oh_list in Gp.total_oh_list_3200.items():
                oh = np.array(oh_list)
                average_oh_3200.append(np.mean(oh))

            # 计算control overhead开销
            for x_, co_list in Gp.total_co_list.items():
                co = np.array(co_list)
                average_co.append(np.mean(co))
            # for x_, co_list in Gp.total_co_list_800.items():
            #     co = np.array(co_list)
            #     average_co_800.append(np.mean(co))
            # for x_, co_list in Gp.total_co_list_1600.items():
            #     co = np.array(co_list)
            #     average_co_1600.append(np.mean(co))
            # for x_, co_list in Gp.total_co_list_2400.items():
            #     co = np.array(co_list)
            #     average_co_2400.append(np.mean(co))
            # for x_, co_list in Gp.total_co_list_3200.items():
            #     co = np.array(co_list)
            #     average_co_3200.append(np.mean(co))

            # 切换车辆文件，将本次记录写入文件中
            with open('result_record1028.txt', 'a+') as f:
                f.write(movement_file + '\n')
                f.write(str(Gp.tag) + '\n')
                f.write("success nums: " +  str(Gp.success_time_list) + '\n')
                f.write("loss nums: " +  str(Gp.fail_time_list) + '\n')
                f.write("loss in area selection nums: " +  str(Gp.loop_file_time_list) + '\n')
                f.write("total delivery time: " + str(succ) + '\n')
                f.write("total packets time: " + str(total) + '\n')
                f.write("delivery rate: " + str(ratio) + '\n')
                f.write("delivery rate in 0-800: " + str(ratio_800) + '\n')
                f.write("delivery rate in 800-1600: " + str(ratio_1600) + '\n')
                f.write("delivery rate in 1600-2400: " + str(ratio_2400) + '\n')
                f.write("delivery rate in 2400-3200: " + str(ratio_3200) + '\n')
                f.write("average hops: " + str(np.mean(np.array(average_hop))) + '\n')
                f.write("average hops in 0-800: " + str(np.mean(np.array(average_hop_800))) + '\n')
                f.write("average hops in 800-1600: " + str(np.mean(np.array(average_hop_1600))) + '\n')
                f.write("average hops in 1600-2400: " + str(np.mean(np.array(average_hop_2400))) + '\n')
                f.write("average hops in 2400-3200: " + str(np.mean(np.array(average_hop_3200))) + '\n')
                f.write("average delay: " + str(np.mean(np.array(average_delay))) + '\n')
                f.write("average delay in 0-800: " + str(np.mean(np.array(average_delay_800))) + '\n')
                f.write("average delay in 800-1600: " + str(np.mean(np.array(average_delay_1600))) + '\n')
                f.write("average delay in 1600-2400: " + str(np.mean(np.array(average_delay_2400))) + '\n')
                f.write("average delay in 2400-3200: " + str(np.mean(np.array(average_delay_3200))) + '\n')
                f.write("communication overhead: " + str(np.mean(np.array(average_oh))) + '\n')
                f.write("communication overhead in 0-800: " + str(np.mean(np.array(average_oh_800))) + '\n')
                f.write("communication overhead in 800-1600: " + str(np.mean(np.array(average_oh_1600))) + '\n')
                f.write("communication overhead in 1600-2400: " + str(np.mean(np.array(average_oh_2400))) + '\n')
                f.write("communication overhead in 2400-3200: " + str(np.mean(np.array(average_oh_3200))) + '\n')
                f.write("routing overhead: " + str(np.mean(np.array(average_co))) + '\n')
                # f.write("routing overhead in 0-800: " + str(np.mean(np.array(average_co_800))) + '\n')
                # f.write("routing overhead in 800-1600: " + str(np.mean(np.array(average_co_1600))) + '\n')
                # f.write("routing overhead in 1600-2400: " + str(np.mean(np.array(average_co_2400))) + '\n')
                # f.write("routing overhead in 2400-3200: " + str(np.mean(np.array(average_co_3200))) + '\n')
                print("delivery rate: " + str(ratio))
                print("average hops: " + str(np.mean(np.array(average_hop))))
                print("average delay: " + str(np.mean(np.array(average_delay))))
                f.write('\n')

            # 清空存储
            Gp.total_test_num = {}
            Gp.total_pkt_delay = {}
            Gp.total_pkt_delay_800 = {}
            Gp.total_pkt_delay_1600 = {}
            Gp.total_pkt_delay_2400 = {}
            Gp.total_pkt_delay_3200 = {}
            Gp.total_hop_list = {}
            Gp.total_hop_list_800 = {}
            Gp.total_hop_list_1600 = {}
            Gp.total_hop_list_2400 = {}
            Gp.total_hop_list_3200 = {}
            Gp.success_time_list = []
            Gp.success_0_800_list = []
            Gp.success_800_1600_list = []
            Gp.success_1600_2400_list = []
            Gp.success_2400_3200_list = []
            Gp.fail_time_list = []
            Gp.loop_file_time_list = []
            Gp.test_loop_fail_time_list = []



