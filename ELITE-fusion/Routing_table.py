import numpy as np
import pandas as pd
import math
import fuzzy.FuzzyRouting as FR
import random
import traffic as RNTFA
import fuzzy.AExactData as Exact
import fuzzy.FuzzyRules as rules
import fuzzy.FuzzyRouting as FuzR
import Global_Par as Gp

# 每一个SA维护一个路由表,依托各自的孪生网络进行训练
# SDVN中央控制器实例化多个Slave Agent (SA)

class Routing_Table:
    def __init__(self):
        self.table = self.initial_table()
        self.table_PRR, self.table_AD, self.table_HC, self.table_RC = self.get_table()
        self.table_PRR_norm = self.initial_table()
        self.table_AD_norm = self.initial_table()
        self.table_HC_norm = self.initial_table()
        self.table_RC_norm = self.initial_table()
        self.table_BP = self.initial_table()
        self.table_HRF = self.initial_table()
        self.table_LDF = self.initial_table()
        self.table_LBF = self.initial_table()

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
    def table_config(self, matrix):
        # 读文件获取Q矩阵
        #matrix = self.get_matrix()
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
        # print("row len: ", row_len)
        # print("column_len: ", column_len)
        #----------------------------------
        # np.zeros((row_len, column_len))
        # np.arange(10).reshape(370, 103)
        # matrix
        D = pd.DataFrame(matrix, index=index_, columns=column_)
        #print(D)
        #print(sum(D[47][46]))
        #exit(0)
        return D

    def get_table(self):
        matrix_PRR = self.get_matrix(Gp.file_pdr)
        table_PRR = self.table_config(matrix_PRR)

        matrix_AD = self.get_matrix(Gp.file_ad)
        table_AD = self.table_config(matrix_AD)

        matrix_HC = self.get_matrix(Gp.file_hc)
        table_HC = self.table_config(matrix_HC)

        matrix_RC = self.get_matrix(Gp.file_rc)
        table_RC = self.table_config(matrix_RC)

        return table_PRR, table_AD, table_HC, table_RC

    def initial_table(self):
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
        # a_list = []
        # while len(a_list) < 370*103:
        #     d_int = random.randint(1, 30)
        #     a_list.append(d_int)
        # a = np.array(a_list)
        D = pd.DataFrame(np.zeros((row_len, column_len)), index=index_, columns=column_)
        # #print(D)
        # D.to_csv('table_PRR.csv', sep=',', header=False, index=False)
        # exit(0)
        return D

    # 预处理，归一化操作
    def preprocessing(self):
        # table in (self.table_PRR, self.table_AD, self.table_HC, self.table_RC)
        # 1
        matrix = []
        for cur in Gp.it_pos:
            for neib in Gp.adjacents_comb[cur]:
                row = []
                for des in Gp.it_pos:
                    max1 = self.table_PRR[des][cur].max()
                    if max1 == 0:
                        row.append(0)
                    else:
                        row.append(min(1, (math.log(1 + self.table_PRR[des][cur][neib])) / (math.log(1+max1))))
                matrix.append(row)
        self.table_PRR_norm = self.table_config(matrix)
        # 2
        matrix = []
        for cur in Gp.it_pos:
            for neib in Gp.adjacents_comb[cur]:
                row = []
                for des in Gp.it_pos:
                    max1 = self.table_AD[des][cur].max()
                    if max1 == 0:
                        row.append(0)
                    else:
                        row.append(min(1, (math.log(1 + self.table_AD[des][cur][neib])) / (math.log(1+max1))))
                matrix.append(row)
        self.table_AD_norm = self.table_config(matrix)
        # 3
        matrix = []
        for cur in Gp.it_pos:
            for neib in Gp.adjacents_comb[cur]:
                row = []
                for des in Gp.it_pos:
                    max1 = self.table_HC[des][cur].max()
                    if max1 == 0:
                        row.append(0)
                    else:
                        row.append(min(1, (math.log(1 + self.table_HC[des][cur][neib])) / (math.log(1+max1))))
                matrix.append(row)
        self.table_HC_norm = self.table_config(matrix)
        # 4
        matrix = []
        for cur in Gp.it_pos:
            for neib in Gp.adjacents_comb[cur]:
                row = []
                for des in Gp.it_pos:
                    max1 = self.table_RC[des][cur].max()
                    if max1 == 0:
                        row.append(0)
                    else:
                        row.append(min(1, (math.log(1 + self.table_RC[des][cur][neib])) / (math.log(1+max1))))
                matrix.append(row)
        self.table_RC_norm = self.table_config(matrix)
        return

    # 基于weight的多路由表融合
    # 融合时注意考虑源和目的是同一个的情况
    def fusion_weight(self):
        self.table_BP = self.table_PRR_norm + self.table_AD_norm + self.table_HC_norm + self.table_RC_norm
        self.table_BP = self.table_BP / 4
        print("table_BP:")
        print(self.table_BP)
        #exit(0)
        return

    def break_point(self, m):
        x1 = 0.2 * m
        x2 = 0.5 * m
        x3 = 0.8 * m
        return x1, x2, x3

    # 基于fuzzy的多路由表融合
    def fusion_fuzzy(self):
        # 1
        matrix = []
        for cur, neibs in Gp.adjacents_comb.items():
            for neib in neibs:
                row = []
                for des in Gp.it_pos:
                    if des in neibs or cur == des:
                        if des == neib:
                            row.append(1)
                        else:
                            row.append(0)
                    else:
                        # 确定分界点
                        m1 = self.table_PRR_norm[des][cur].max()
                        # x_prr_l, x_prr_m, x_prr_h = self.break_point(m1)
                        m2 = self.table_AD_norm[des][cur].max()
                        # x_ad_l, x_ad_m, x_ad_h = self.break_point(m2)
                        m3 = self.table_RC_norm[des][cur].max()
                        # x_rc_l, x_rc_m, x_rc_h = self.break_point(m3)
                        # 融合
                        v1 = self.table_PRR_norm[des][cur][neib]
                        v2 = self.table_AD_norm[des][cur][neib]
                        v3 = self.table_RC_norm[des][cur][neib]
                        fusion_result = FR.fuzzy_routing(v1, v2, v3, m1, m2, m3)
                        row.append(fusion_result)
                matrix.append(row)
        self.table_HRF = self.table_config(matrix)
        print("table_HRF:")
        print(self.table_HRF)
        # 2
        matrix = []
        for cur, neibs in Gp.adjacents_comb.items():
            for neib in neibs:
                row = []
                for des in Gp.it_pos:
                    if des in neibs or cur == des:
                        if des == neib:
                            row.append(1)
                        else:
                            row.append(0)
                    else:
                        # 确定分界点
                        m1 = self.table_PRR_norm[des][cur].max()
                        # x_prr_l, x_prr_m, x_prr_h = self.break_point(m1)
                        m2 = self.table_AD_norm[des][cur].max()
                        # x_ad_l, x_ad_m, x_ad_h = self.break_point(m2)
                        m3 = self.table_HC_norm[des][cur].max()
                        # x_hc_l, x_hc_m, x_hc_h = self.break_point(m3)
                        # 融合
                        v1 = self.table_AD_norm[des][cur][neib]
                        v2 = self.table_HC_norm[des][cur][neib]
                        v3 = self.table_PRR_norm[des][cur][neib]
                        fusion_result = FR.fuzzy_routing(v1, v2, v3, m2, m3, m1)
                        row.append(fusion_result)
                matrix.append(row)
        self.table_LDF = self.table_config(matrix)
        print("table_LDF:")
        print(self.table_LDF)
        # 3
        matrix = []
        for cur, neibs in Gp.adjacents_comb.items():
            for neib in neibs:
                row = []
                for des in Gp.it_pos:
                    if des in neibs or cur == des:
                        if des == neib:
                            row.append(1)
                        else:
                            row.append(0)
                    else:
                        # 确定分界点
                        m1 = self.table_HC_norm[des][cur].max()
                        # x_hc_l, x_hc_m, x_hc_h = self.break_point(m1)
                        m2 = self.table_AD_norm[des][cur].max()
                        # x_ad_l, x_ad_m, x_ad_h = self.break_point(m2)
                        m3 = self.table_RC_norm[des][cur].max()
                        # x_rc_l, x_rc_m, x_rc_h = self.break_point(m3)
                        # 融合
                        v1 = self.table_RC_norm[des][cur][neib]
                        v2 = self.table_HC_norm[des][cur][neib]
                        v3 = self.table_AD_norm[des][cur][neib]
                        fusion_result = FR.fuzzy_routing(v1, v2, v3, m3, m1, m2)
                        row.append(fusion_result)
                matrix.append(row)
        self.table_LBF = self.table_config(matrix)
        print("table_LBF:")
        print(self.table_LBF)
        return

