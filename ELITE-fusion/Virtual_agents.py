import pandas as pd
import Global_Par as Gp

# 每一个SA维护一个路由表,依托各自的孪生网络进行训练
# SDVN中央控制器实例化多个Slave Agent (SA)

class Virtual_agent:
    def __init__(self, agent_id):
        self.id = agent_id # 智能体id
        self.table = self.table_config() # 智能体维护路由表
        self.road_length = 0 # 道路长度
        self.road_vehicle_num = 0 # 道路上车辆数

    # 读文件，初始化
    def get_matrix(self, table_name):
        matrix = []
        # 训练时，读一个全是0的
        with open(table_name, 'r') as file:
            for line in file:
                str = line.split(',')
                if str:
                    row = []
                    for x in str:
                        row.append(float(x))
                    matrix.append(row)
        return matrix

    # 路由表矩阵, dataframe
    # 在选择元素时，先定位列（target），再定位第一维行（current），最后第二维行（adjacent）
    # table[target_area][current_area][next_area]
    # 使用loc[]选择某一行
    def table_config(self):
        # 读文件获取Q矩阵
        matrix = self.get_matrix()
        index1 = []
        index2 = []
        column_ = []
        column_len = len(Gp.it_pos)
        row_len = 0
        for it, neibs in Gp.adjacents_comb.items():
            column_.append(it)
            row_len += len(neibs)
            index2.extend(neibs)
            for i in range(0, len(neibs)):
                index1.append(it)
        index_ = [index1, index2]
        print("row len: ", row_len)
        print("column_len: ", column_len)
        # np.zeros((row_len, column_len))
        # matrix
        D = pd.DataFrame(matrix, index=index_, columns=column_)
        print(D)
        return D

    # 更新路由表
    def update(self, path):
        if len(path) == 1:
            return
        target_ = path[-1]  # 目的状态
        for i in range(len(path)-1, 0, -1):
            current_ = path[i-1] # 当前状态
            candidate_ = path[i] # 下一状态
            Max = max(self.table[target_][candidate_]) # 未来奖励
            R = 0 # 实时奖励
            self.table[target_][current_][candidate_] += Gp.q_alpha * (R + Gp.q_gamma * (Max - self.table[target_][current_][candidate_]))
        return

    # 基于孪生网络的路由策略学习
    def learning(self):

        return