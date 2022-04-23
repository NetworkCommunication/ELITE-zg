tag = 1
n = 2
file_pdr = 'table_record_' + str(n) + '_pdr.csv'
file_ad = 'table_record_' + str(n) + '_ad.csv'
file_hc = 'table_record_' + str(n) + '_hc.csv'
file_rc = 'table_record_' + str(n) + '_rc.csv'

# 地图中节点数
total_node_num = [1000, 1500, 2000, 2500, 3000]
comb_node_num = [800, 1200, 1600, 2000, 2400]
# 地图边界路口id
map_boundary = [46, 7, 38, 811022916]
# 标记
delay_hop_tag = 0
# 原始信息，读文件时存储信息，实际不使用
intersection = {} # 路口
adjacents = {} # 邻居路口
edges_boundary = {} # 道路连接关系
# 组合路口
all_in_one = {} # {intersection: [i1, i2,...],...}
intersections_combination = [] # 多个路口，其实本是一个路口
it_comb_detail = {} # {id:[id1,...]}
it_comb_pos = {} # 新的路口的信息，编号为0-47 {id:[x1,y1]}
num = 0 # 本为一个路口的路口数
# -------------可用信息-----------------------
it_pos = {} # 处理之后的路口信息 id:[x,y]
adjacents_comb = {} # 处理之后的路口相邻关系
junction_dis = {} # 两区域间距离
adjacency_dis = {} # 相邻两区域道路长度

# road_veh_num = {} # 道路上车辆数
# road_veh_num_ow = {} # 道路上单向行驶车辆数
# all_node_neighbor = {} # 车辆邻居信息
#---------------------------------------------
# 无效边缘路口
un_intersections = [26, 1501191067, 1554161759, 1554162236, 3011987317, 3011958556, 34, 3011970566, 32, 1774678167, 677603150, 1776032723, 6395814545, 18, 0, 5377474182, 1774638801, 6395814548, 2043972045, 5268439719, 1585713352, 28, 1585713348, 19, 2043972058, 1, 6110489165, 6110489168, 6110489172, 25, 27, 4340744995, 4537420835, 29, 5267470789, 5267470788, 4537420815, 4537420818, 4537420819, 4537420821]
# 发送路由请求节点比例
com_node_rate = 0.2
# 画面更新时间
update_period = 1
# 单跳时延
sum = 0
record = []
effi = 0
MAX = 600000
# 重传次数
re_time = 3

#---------------------------------------------
# 分组传输最大距离
com_dis = 350
#---------------------------------------------

# -------------------仿真结果-------------------
oh_list = [] # 开销
oh_list_800 = []
oh_list_1600 = []
oh_list_2400 = []
oh_list_3200 = []
total_oh_list = {} # 每次仿真时的所有开销
total_oh_list_800 = {}
total_oh_list_1600 = {}
total_oh_list_2400 = {}
total_oh_list_3200 = {}
co_list = [] # control overhead开销
# co_list_800 = []
# co_list_1600 = []
# co_list_2400 = []
# co_list_3200 = []
total_co_list = {} # 每次仿真时的所有co开销
# total_co_list_800 = {}
# total_co_list_1600 = {}
# total_co_list_2400 = {}
# total_co_list_3200 = {}
pkt_delay = [] # 从产生数据包到失败或成功接收的时间
pkt_delay_800 = []
pkt_delay_1600 = []
pkt_delay_2400 = []
pkt_delay_3200 = []
hop_list = [] # 数据包跳数
hop_list_800 = []
hop_list_1600 = []
hop_list_2400 = []
hop_list_3200 = []
total_pkt_delay = {} # 每次仿真时的所有数据包时延
total_pkt_delay_800 = {}
total_pkt_delay_1600 = {}
total_pkt_delay_2400 = {}
total_pkt_delay_3200 = {}
total_hop_list = {} # 每次仿真时的所有数据包跳数
total_hop_list_800 = {}
total_hop_list_1600 = {}
total_hop_list_2400 = {}
total_hop_list_3200 = {}
success_time = 0 # 成功次数
success_0_800 = 0
success_800_1600 = 0
success_1600_2400 = 0
success_2400_3200 = 0
fail_time = 0 # 失败次数
loop_fail_time = 0 # 因选区时loop失败次数
success_time_list = [] # 记录x次仿真 每次仿真时从sim到des的成功数据包数
success_0_800_list = []
success_800_1600_list = []
success_1600_2400_list = []
success_2400_3200_list = []
fail_time_list= [] # 记录x次仿真 每次仿真时从sim到des的失败数据包数
loop_file_time_list = [] # 记录x次仿真 每次仿真时从sim到des的选区回路数据包数
#------------------------------------
#-------------------overhead-----------------------
overhead = []
overhead_list = {}
overhead_index = 0
#--------------------------------------------------

# 记录地图中所有的attributes值，用于确定归一化时的最小值，最大值，均值，方差等
distribution_record = []
connectivity_record = []
distance_record = []

# 记录地图中所有归一化后的attributes值，用于确定划分模糊集合时的边界
normalized_distribution_record = []
normalized_connectivity_record = []
normalized_distance_record = []

# 计算valid_distance时的权重(距离a和角度b)
distance_a = 1
distance_b = 0

#------------------------------------------------------------------------------------
# 参数选择次序，0:1000 1:1500 2:2000 3:2500 4:3000
nor_para_seq = 0
# 归一化valid_distance时的最小最大值
distance_min = [0.15774859284379994, 0.15774859284379994, 0.15774859284379994, 0.15774859284379994, 0.15774859284379994]
distance_max = [2.012700464538705, 2.012700464538705, 2.012700464538705, 2.012700464538705, 2.012700464538705]
distance_var = [0.16562740095073933, 0.16562740095073933, 0.16562740095073933, 0.16562740095073933, 0.16562740095073933]
# 归一化connectivity时的最小值和最大值和方差
connectivity_min = [0.0, 0.0, 0.0, 0.0, 0.0]
connectivity_max = [0.13557349860623996, 0.16462165924051375, 0.18465087716246717, 0.19837549834951584, 0.2580033870465819]
#connectivity_var = []
# 归一化distribution时的最小值，最大值和方差
distribution_min = [0.0, 0.0, 0.0, 0.0, 0.0]
distribution_max = [0.14309068246223333, 0.15397449745231395,  0.15397449745231395, 0.22521774788279159, 0.22521774788279159]
#distribution_avg = [0.031106285615615296, 0.039911050336677, 0.047750219374825466, 0.05577953332575896, 0.0638667131537299]
distribution_var = [0.015772824078035194, 0.019545574104876257, 0.02338558433596064, 0.028496788175371233, 0.032770350221516226]
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# valid_distance的模糊集合划分
distance_close_a = 0
distance_close_b = 0
distance_medium_a = 0
distance_medium_b = 0
distance_medium_c = 0
distance_medium_d = 0
distance_far_a = 0
distance_far_b = 0
# connectivity的模糊集合划分
connectivity_low_a = 0
connectivity_low_b = 0
connectivity_middle_a = 0
connectivity_middle_b = 0
connectivity_middle_c = 0
connectivity_middle_d = 0
connectivity_high_a = 0
connectivity_high_b = 0
# distribution的模糊集合划分
distribution_poor_a = 0
distribution_poor_b = 0
distribution_medium_a = 0
distribution_medium_b = 0
distribution_medium_c = 0
distribution_medium_d = 0
distribution_good_a = 0
distribution_good_b = 0
#------------------------------------------------------------------------------------

# qlearning学习率及折扣
q_alpha = 0.3 # 区间为0.3-0.9 这个不用，在树更新时自动决定
q_gamma = 0.1
# 正反馈时reward的三个权重
positive_a = 0.3
positive_b = 0.3
positive_c = 0.4
# 稀疏负反馈时reward两个权重
negative_a = 0.7
negative_b = 0.7

#------------------------------------------------------------------------------------

co_count = 0