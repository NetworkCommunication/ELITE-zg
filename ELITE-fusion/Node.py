# 节点类，标记节点信息，提供多个方法
import Packet as Pkt
import Global_Par as Gp
import time
import GPSR as gpsr
from math import *

def takeSecond(elem):
    return elem[1]

# 计算两节点之间的距离
def getdis(ax, ay, bx, by):
    temp_x = ax - bx
    temp_y = ay - by
    temp_x = temp_x * temp_x
    temp_y = temp_y * temp_y
    result = sqrt(temp_x+temp_y)
    return result
def angle(x0, y0, x1, y1, x2, y2):
    if x0==x2 and y0==y2:  # 没动地方
        return 0
    cos = ((x1-x0)*(x2-x0)+(y1-y0)*(y2-y0))/(sqrt(pow(x1-x0, 2)+pow(y1-y0, 2))*sqrt(pow(x2-x0, 2)+pow(y2-y0, 2)))
    theta = acos(cos)/pi
    return theta

class Node:
    def __init__(self, node_id, controller):
        self.node_id = node_id  # 节点id
        self.position = [0, 0, 0]  # 位置 三维
        self.velocity = [0, 0, 0]  # 速度
        self.angle = 0 # 行驶方向
        self.acceleration = []  # 加速度
        self.routing_table = []  # 路由表
        self.hello_table = []    # 接收到的hello包
        self.neighbor_list = {}  # 邻居表
        self.data_pkt_list = []  # 数据分组存储
        self.cache = 1024  # 当前缓存
        self.controller = controller  # 自身所属控制器
        self.pkt_seq = 0  # 当前节点包序号
        self.it_cover = {} # 所有节点所属路口 {node:intersection, ...}
        self.area = []

    # 根据数据更新自身位置
    def update_node_position(self, node_id_position):
        self.velocity[0] = node_id_position[self.node_id][0, 0] - self.position[0]
        self.velocity[1] = node_id_position[self.node_id][0, 1] - self.position[1]
        self.velocity[2] = node_id_position[self.node_id][0, 2] - self.position[2]
        self.angle = angle(self.position[0], self.position[1], self.position[0], self.position[1]+1, node_id_position[self.node_id][0, 0],node_id_position[self.node_id][0, 1])
        self.position = [node_id_position[self.node_id][0, 0], node_id_position[self.node_id][0, 1], node_id_position[self.node_id][0, 2]]
        return

    # 向控制器发送hello包，报告车辆节点自身信息
    def generate_hello_c(self, controller):
        # （id，地理位置，速度，加速度，当前剩余缓存）
        controller.hello_list.append(Pkt.Hello_c(self.node_id,  self.position, self.cache))
        Gp.co_count += 1
        return

    # 接收来自控制器的数据包，更新当前节点所属区域信息
    # 当前节点所属的区域，area=[] 为一个列表，可能只有一个元素，也可能有多个元素
    def receive_notify(self, flow_notify):
        self.area = flow_notify.area
        return

    # 当前节点向其他节点广播hello包，报告车辆节点自身信息
    def generate_hello_n(self, node_list):
        # 当前节点通信范围内的所有节点接收hello包，并存储到hello_table中
        for node in node_list:
            if self.node_id == node.node_id: # 忽略当前节点本身
                continue
            d = getdis(self.position[0], self.position[1], node.position[0], node.position[1]) # 距离
            if d < Gp.com_dis: # hello包发送给处于节点通信范围内的邻居节点（id，地理位置，速度，加速度，当前剩余缓存）
                node.hello_table.append(Pkt.Hello(self.node_id,  self.position, self.area, self.velocity,  self.acceleration,  self.cache))
                Gp.co_count += 1
        return

    # 当前节点根据接收到的hello包更新邻居列表，同时删除超时条目
    def update_neighbor_list(self):
        # 删除超时条目(清空)
        self.neighbor_list = {}
        # 更新邻居列表
        for pkt in self.hello_table:
            self.neighbor_list[pkt.node_id] = [pkt.position, pkt.area]
        self.hello_table = []
        return

    # 产生数据包，且向控制器发送请求，自身当前节点包序号加1
    def generate_request(self, des_id, controller, size):
        # 时延处理
        print('node %d generate packet to node %d' % (self.node_id, des_id))
        self.pkt_seq = self.pkt_seq + 1 # 当前节点发出的第pkt_seq个数据包
        # 产生数据包，添加到当前节点数据包列表中 （源节点，目的节点，分组大小，状态，路由发出者节点，路由发出者序号，发出时间）
        self.data_pkt_list.append(Pkt.DataPkt(self.node_id, des_id, size, 0, self.node_id, self.pkt_seq, 1000 * time.time()))
        # 向控制器的路由请求列表中插入路由请求包 （源节点，目的节点，发出者节点，发出者序号）
        controller.flow_request_list.append(Pkt.FlowRequest(self.node_id, des_id, self.node_id, self.pkt_seq))
        return

    # 处理路由回复
    def receive_flow(self, flow_reply):
        for pkt in self.data_pkt_list[::-1]:
            # 把从控制器请求得到的区域路径和汇报标记插入到数据包头中
            if pkt.source_id == self.node_id: #and pkt.seq == self.pkt_seq:
                pkt.insert_info(flow_reply.area_path)
                break
        return

    # 转发自身携带分组
    def forward_pkt(self, node_list, controller):
        # [::-1]将列表内容翻转。
        # 新的数据包插到数据包列表的最后，因此倒着来
        for pkt in self.data_pkt_list[::-1]:
            # 查表确定区域路径时就失败了
            if len(pkt.area_path) == 0:
                # Gp.pkt_delay.append(-1)
                # Gp.hop_list.append(-1)
                return
            #print("当前节点及邻居表信息: ", self.node_id, self.neighbor_list)
            next_hop, curr_area = self.find_next(pkt.des_id, pkt.area_path, node_list)
            # 回路，丢包
            if next_hop != -1:
                if next_hop in pkt.path:
                    pkt.count = 0
                    next_hop = -1
            # 找到下一跳
            if next_hop != -1:
                pkt.count += 1 # 数据包跳数+1
                pkt.path.append(self.node_id)  # 将当前节点的id记录到包路径中
                node_list[next_hop].receive_pkt(pkt, node_list, controller)  # 下一跳节点接收数据包
                #self.data_pkt_list.remove(pkt) # 当前节点中删除这个包
                return
            else:
                # 错误处理
                print("loss")
                Gp.fail_time += 1
                # 分析原因，并向控制器汇报
                # 丢包
                controller.flow_report_list.append(Pkt.FlowReport(pkt.area_path, loss=1, loss_area=curr_area))
                #Gp.delay = round(1000 * (time.time()-pkt.s_time))
                return
        return

    # 接收转发来的分组
    def receive_pkt(self, data_pkt, node_list, controller):
        data_pkt.delay += 0.03
        # 已经到达目的节点
        if data_pkt.des_id == self.node_id:
            data_pkt.e_time = 1000 * time.time() # 数据包到达时间
            # 从产生数据包到数据包被接受的时延
            data_pkt.delay = data_pkt.e_time - data_pkt.s_time
            # 计算传输时延
            dis_all = 0
            data_pkt.path.append(self.node_id)
            for i in range(0, len(data_pkt.path)-1):
                n1 = data_pkt.path[i]
                n2 = data_pkt.path[i+1]
                dis = getdis(node_list[n1].position[0], node_list[n1].position[1], node_list[n2].position[0], node_list[n2].position[1])
                dis_all += dis   # 传输时延+n
            # data_pkt.delay = data_pkt.delay + dis_all * (0.005 / 1000) + data_pkt.count * 0.224
            data_pkt.delay += dis_all * (0.016) + data_pkt.count * 0.224
            # 从源节点到目的节点的时延
            Gp.pkt_delay.append(round(data_pkt.delay, 3))
            if Gp.delay_hop_tag == 800:
                Gp.pkt_delay_800.append(round(data_pkt.delay, 3))
            elif Gp.delay_hop_tag == 1600:
                Gp.pkt_delay_1600.append(round(data_pkt.delay, 3))
            elif Gp.delay_hop_tag == 2400:
                Gp.pkt_delay_2400.append(round(data_pkt.delay, 3))
            elif Gp.delay_hop_tag == 3200:
                Gp.pkt_delay_3200.append(round(data_pkt.delay, 3))

            # 从源节点到目的节点的跳数
            dist = 0
            for i in range(0, len(data_pkt.path)-1):
                current = data_pkt.path[i]
                next = data_pkt.path[i+1]
                xc = node_list[current].position[0]
                yc = node_list[current].position[1]
                xn = node_list[next].position[0]
                yn = node_list[next].position[1]
                d = getdis(xc,yc,xn,yn)
                dist += d
            Gp.hop_list.append(dist) #(len(data_pkt.path))
            if Gp.delay_hop_tag == 800:
                Gp.hop_list_800.append(dist)
            elif Gp.delay_hop_tag == 1600:
                Gp.hop_list_1600.append(dist)
            elif Gp.delay_hop_tag == 2400:
                Gp.hop_list_2400.append(dist)
            elif Gp.delay_hop_tag == 3200:
                Gp.hop_list_3200.append(dist)

            # 从源到目的的路径的控制包数
            if len(data_pkt.path) <= 1:
                c_message = 2
            else:
                c_message = 2
                for n in data_pkt.path:
                    print(len(node_list[n].neighbor_list))
                    c_message += len(node_list[n].neighbor_list) + 1
            Gp.oh_list.append(c_message)  # (len(data_pkt.path))
            if Gp.delay_hop_tag == 800:
                Gp.oh_list_800.append(c_message)
            elif Gp.delay_hop_tag == 1600:
                Gp.oh_list_1600.append(c_message)
            elif Gp.delay_hop_tag == 2400:
                Gp.oh_list_2400.append(c_message)
            elif Gp.delay_hop_tag == 3200:
                Gp.oh_list_3200.append(c_message)

            # 数据包转发成功
            print('%3d to %3d successful transmission！with delay = %3d ' % (data_pkt.source_id, data_pkt.des_id, Gp.pkt_delay[-1]))
            Gp.success_time += 1 # 成功次数+1
            # 向控制器回复
            controller.flow_report_list.append(Pkt.FlowReport(data_pkt.area_path, loss = 0, loss_area=0))
        # 当前为中间节点
        else:
            self.data_pkt_list.append(data_pkt)
            self.forward_pkt(node_list, controller)
        return


    # --------------------------------------------------------------------------------------- #
    #                            路由计算
    # --------------------------------------------------------------------------------------- #
    def link_stability(self, top_k, node_list):
        next_hop = top_k[0]
        return next_hop

    # 判断某一邻居节点是否处在指定(和当前节点同一)区域内
    def is_belong(self, area_set, area):
        for a in area_set:
            if a == area:
                return 1
        return 0

    # 同区域内决策
    def intra_area(self, des_id, destination, curr_area, node_list, k=0.3):
        next_hop = 0
        # 邻居表中存在目的节点
        if des_id in self.neighbor_list.keys():
            next_hop = des_id
        # 不存在
        else:
            # 计算并选出更接近目的节点的邻居
            closer_to_destination = []
            d1 = getdis(self.position[0], self.position[1], destination.position[0], destination.position[1])
            for neib_id, neib_info in self.neighbor_list.items():
                d2 = getdis(neib_info[0][0], neib_info[0][1], destination.position[0], destination.position[1])
                if d1 > d2:
                    # 选择和当前节点属于同一区域的邻居
                    if self.is_belong(neib_info[1], curr_area):
                        closer_to_destination.append((neib_id, d2))

            # 邻居表中存在更接近目的节点的邻居
            if closer_to_destination:
                top_k = []
                max_length = ceil(k * len(closer_to_destination))
                closer_to_destination.sort(key=takeSecond)
                for i in range(0, max_length):
                    top_k.append(closer_to_destination[i][0])
                    next_hop = self.link_stability(top_k, node_list)
            # 不存在
            else:
                # 计算并选出更接近当前区域中心的邻居
                closer_to_current_area = []
                d3 = getdis(self.position[0], self.position[1], Gp.it_pos[curr_area][0], Gp.it_pos[curr_area][1])
                for neib_id, neib_info in self.neighbor_list.items():
                    d4 = getdis(neib_info[0][0], neib_info[0][1], Gp.it_pos[curr_area][0], Gp.it_pos[curr_area][1])
                    if d3 > d4:
                        # 选择和当前节点属于同一区域的邻居
                        if self.is_belong(neib_info[1], curr_area):
                            closer_to_current_area.append((neib_id, d4))

                # 邻居表中存在距离更接近当前区域中心的区域
                if closer_to_current_area:
                    top_k = []
                    max_length = ceil(k * len(closer_to_current_area))
                    closer_to_current_area.sort(key=takeSecond)
                    for i in range(0, max_length):
                        top_k.append(closer_to_current_area[i][0])
                        next_hop = self.link_stability(top_k, node_list)
                # 不存在
                else:
                    next_hop = -1
        return next_hop

    # 跨区域决策
    def inter_area(self, curr_area, next_area, node_list, k=0.3):
        next_hop = 0
        # 查找属于下一区域的邻居
        belong_to_next_area = []
        for neib_id, neib_info in self.neighbor_list.items():
            # 目标下一区域在邻居的区域表中
            if next_area in neib_info[1]:
                d = getdis(neib_info[0][0], neib_info[0][1], Gp.it_pos[next_area][0],Gp.it_pos[next_area][1])
                belong_to_next_area.append((neib_id, d))
        # 邻居表中存在属于下一区域的邻居
        if belong_to_next_area:
            top_k = []
            max_length = ceil(k * len(belong_to_next_area))
            belong_to_next_area.sort(key=takeSecond)
            for i in range(0,max_length):
                top_k.append(belong_to_next_area[i][0])
            next_hop = self.link_stability(top_k, node_list)
        # 不存在
        else:
            # 计算并选出更接近下一区域中心的邻居
            closer_to_next_area = []
            d1 = getdis(self.position[0], self.position[1], Gp.it_pos[next_area][0], Gp.it_pos[next_area][1])
            for neib_id, neib_info in self.neighbor_list.items():
                d2 = getdis(neib_info[0][0], neib_info[0][1], Gp.it_pos[next_area][0], Gp.it_pos[next_area][1])
                if d1 > d2:
                    # 选择和当前节点属于同一区域的邻居
                    if self.is_belong(neib_info[1], curr_area):
                        closer_to_next_area.append((neib_id, d2))

            # 邻居表中存在更接近下一区域中心的邻居
            if closer_to_next_area:
                top_k = []
                max_length = ceil(k * len(closer_to_next_area))
                closer_to_next_area.sort(key=takeSecond)
                for i in range(0, max_length):
                    top_k.append(closer_to_next_area[i][0])
                next_hop = self.link_stability(top_k, node_list)
            # 不存在
            else:
                # 计算并选出更接近当前区域中心的邻居
                closer_to_current_area = []
                d3 = getdis(self.position[0], self.position[1], Gp.it_pos[curr_area][0], Gp.it_pos[curr_area][1])
                for neib_id, neib_info in self.neighbor_list.items():
                    d4 = getdis(neib_info[0][0], neib_info[0][1], Gp.it_pos[curr_area][0], Gp.it_pos[curr_area][1])
                    if d3 > d4:
                        # 选择和当前节点属于同一区域的邻居
                        if self.is_belong(neib_info[1], curr_area):
                            closer_to_current_area.append((neib_id, d4))

                # 邻居表中存在更接近当前区域中心的邻居
                if closer_to_current_area:
                    top_k = []
                    max_length = ceil(k * len(closer_to_current_area))
                    closer_to_current_area.sort(key=takeSecond)
                    for i in range(0, max_length):
                        top_k.append(closer_to_current_area[i][0])
                    next_hop = self.link_stability(top_k, node_list)
                # 不存在
                else:
                    next_hop = -1
        return next_hop

    def find_next(self, des_id, area_list, node_list):
        next_hop = 0 # 下一跳，初始化定义
        # 确定当前节点所处的区域（在区域路径上）
        for a in self.area: # 遍历当前节点所有可能所属区域
            for t in area_list:
                if a == t:
                    index =  area_list.index(t) # area_list.index(self.area)
                    curr_area = a # 当前area
        # 判断当前区域是否为目的区域
        for a in self.area: # 看当前节点所属的多个区域中是否有目的区域
            if a == area_list[-1]:
                destination = node_list[des_id]  # 实例目的节点
                next_hop = self.intra_area(des_id, destination, curr_area, node_list) # 在当前区域内,朝向目的节点查找下一跳
                # 返回下一跳节点，当前区域
                return next_hop, curr_area
        # 不是目的区域，计算，确定下一跳区域
        #print("当前节点id及所属区域及限定区域: ", self.node_id, self.area, curr_area)
        # 根据当前区域确定下一跳区域
        next_area = area_list[index + 1]
        #print("下一区域: ", next_area)
        # 根据下一区域找下一跳
        next_hop = self.inter_area(curr_area, next_area, node_list)
        return next_hop, curr_area



