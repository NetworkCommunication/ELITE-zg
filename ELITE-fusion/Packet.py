# 信息更新包 属性：id，地理位置，速度，加速度，当前剩余缓存, 当前所属区域
class Hello:
    def __init__(self, node_id, position, area, velocity, acceleration, current_cache):
        self.node_id = node_id
        self.position = position
        self.area = area
        self.velocity = velocity
        self.acceleration = acceleration
        self.current_cache = current_cache

class Hello_c:
    def __init__(self, node_id, position, current_cache):
        self.node_id = node_id
        self.position = position
        self.current_cache = current_cache

# 路由请求 属性：源节点，目的节点，发出者节点，发出者序号, 发出者所在区域， 目的节点所在区域
class FlowRequest:
    def __init__(self, source_id, des_id, node_id, seq):
        self.source_id = source_id
        self.des_id = des_id
        self.seq = seq
        self.node_id = node_id

# 路由回复 属性：区域路径
class FlowReply:
    def __init__(self, area_path):
        self.area_path = area_path

# 路由回复，通知所有节点其所属的区域信息
class FlowNotify:
    def __init__(self, area):
        self.area = area # []

# 路由汇报，通知控制器更新路由表
class FlowReport:
    def __init__(self, area_path, loss, loss_area):
        self.area_path = area_path
        self.loss = loss
        self.loss_area = loss_area

# 路由错误请求 属性： 源节点，目的节点，错误节点，错误次数，路由发出者序号，错误发出者序号
class FlowError:
    def __init__(self, source_id, des_id, error_id, time, source_seq, error_seq):
        self.source_id = source_id
        self.des_id = des_id
        self.error_id = error_id
        self.time = time
        self.source_seq = source_seq
        self.error_seq = error_seq

# 数据分组 属性：源节点，目的节点，分组大小，状态，路由发出者节点，路由发出者序号，发出时间
class DataPkt:
    def __init__(self, source_id, des_id, pkt_size, state, node_id, seq, s_time):
        self.source_id = source_id
        self.des_id = des_id
        self.pkt_size = pkt_size
        self.state = state
        self.seq = seq
        self.node_id = node_id
        self.s_time = s_time # 发出时间
        self.initial_intersection = 0 # 源节点所在的cluster area
        self.target_intersection = 0 # 目的节点所在的cluster area
        self.path = [] # 数据包经过的路径
        self.last_area = -1 # 数据包刚经过的区域
        self.area_path = [] # 数据包所延的区域路径
        self.e_time = 0 # 到达目的节点时间
        self.delay = 0 # 时延
        self.count = 0

    def insert_info(self, area_path):
        self.area_path = area_path

    def update1(self, s_belong_it, d_belong_it):
        self.initial_intersection = s_belong_it
        self.target_intersection = d_belong_it

