import re
import math
import Global_Par as Gp
import copy

# 点到直线的距离
def nldis(pointX,pointY,lineX1,lineY1,lineX2,lineY2):
    a=lineY2-lineY1
    b=lineX1-lineX2
    c=lineX2*lineY1-lineX1*lineY2
    dis=(math.fabs(a*pointX+b*pointY+c))/(math.pow(a*a+b*b,0.5))
    return dis

# 计算两节点之间的距离
def nndis(ax, ay, bx, by):
    temp_x = ax - bx
    temp_y = ay - by
    temp_x = temp_x * temp_x
    temp_y = temp_y * temp_y
    result = math.sqrt(temp_x+temp_y)
    return result

# 角度
def angle(x0, y0, x1, y1, x2, y2):
    cos = ((x1-x0)*(x2-x0)+(y1-y0)*(y2-y0))/(math.sqrt(pow(x1-x0, 2)+pow(y1-y0, 2)) * math.sqrt(pow(x2-x0, 2)+pow(y2-y0, 2)))
    theta = math.acos(cos) / math.pi
    return theta

# 路口的id 位置
# 返回 {intersection:[x,y], ...}
def junction():
    junction_file = "de_intersection.xml"
    junctions_coordinate = {} # id:[x,y]
    junctions_connect = {} #id:[id,id,...,id]
    with open(junction_file, 'r') as f:
        for line in f:
            line_list = re.split('[\s]', line) # 根据空白字符切割每一行
            if line_list[0] == '<junction':
                id = int(float(line_list[1][4:-1]))
                x = float(line_list[3][3:-1])
                y = float(line_list[4][3:-1])
                junctions_coordinate[id] = [x,y]
    return junctions_coordinate

# 道路的id 起始点 坐标线
def edge():
    edge_file = "de_edges.xml"
    edges_line = {} # id:[x,y]
    edges_boundary = {} #id:[junction_id,junction_id]
    with open(edge_file, 'r') as f:
        for line in f:
            line_list = re.split('[\s]', line)  # 根据空白字符切割每一行
            if line_list[0] == '<edge':
                id = line_list[1][4:-1]
                source = int(float(line_list[2][6:-1]))
                target = int(float(line_list[3][4:-1]))
                edges_boundary[id] = [source, target]
    return edges_boundary

# 路口间的相邻关系
# 注意多个路口的结合，保存为comb_adjacent
# 返回 {current:[neighbor_1, ..., neighbor_n], ...}
def adjacent(edges_boundary, junctions_coordinate):
    adjacents = {} # id:[neighbor_id, neighbor_id]
    for jun in junctions_coordinate.keys():
        adjacents[jun] = []
    for edge_id, edge_end in edges_boundary.items():
        source = edge_end[0]
        target = edge_end[1]
        if target not in adjacents[source]:
            adjacents[source].append(target)
        if source not in adjacents[target]:
            adjacents[target].append(source)
    return adjacents

# 本为同一个路口的多个路口
def intersection_combination(junctions_coordinate):
    for it1, pos1 in junctions_coordinate.items():
        lis = []
        for it2, pos2 in junctions_coordinate.items():
            # 排除自身
            if it1 == it2:
                continue
            # 距离，小于30代表他们本为一个路口
            dis = nndis(pos1[0], pos1[1], pos2[0], pos2[1])
            if dis <= 30:
                lis.append(it2)
        if lis:
            Gp.all_in_one[it1] = lis
    # 不重复的
    for c, n in Gp.all_in_one.items():
        f = 0
        for l in Gp.intersections_combination:
            if c in l:
                f = 1
        if f == 0:
            x = copy.deepcopy(n)
            x.append(c)
            Gp.intersections_combination.append(x)
            Gp.num += 1
    return

# 合并
def combination():
    i = 0
    for pair in Gp.intersections_combination:
        Gp.it_comb_detail[i] = pair
        x = 0
        y = 0
        for it in pair:
            x += Gp.intersection[it][0]
            y += Gp.intersection[it][1]
        Gp.it_comb_pos[i] = [round(x/len(pair), 2), round(y/len(pair), 2)]
        i += 1
    # 新的路口位置信息，不覆盖原来的
    Gp.it_pos = copy.deepcopy(Gp.intersection)
    for area in Gp.all_in_one:
        del Gp.it_pos[area]
    Gp.it_pos.update(Gp.it_comb_pos)
    return

# 合并之后的相邻关系
def comb_adjacent():
    Gp.adjacents_comb = copy.deepcopy(Gp.adjacents)
    temp = {i:[] for i in range(0,48)}
    # 删除分裂的
    for it, detail in Gp.it_comb_detail.items():
        for small_it in detail:
            #temp[it].extend(Gp.adjacents[small_it])
            # 删除重复和分裂 合并后的：其他
            for neb in Gp.adjacents[small_it]:
                if neb not in temp[it] and neb not in detail:
                    temp[it].append(neb)
            del Gp.adjacents_comb[small_it]
    Gp.adjacents_comb.update(temp)

    # 其他：合并后的
    for current, neib_set in Gp.adjacents_comb.items():
        for it, detail in Gp.it_comb_detail.items():
            for small_it in detail:
                if small_it in neib_set:
                    #Gp.adjacents_comb[current].remove(small_it)
                    if it not in Gp.adjacents_comb[current]:
                        Gp.adjacents_comb[current].append(it)
    for it, detail in Gp.it_comb_detail.items():
        for small_it in detail:
            for current in Gp.adjacents_comb:
                if small_it in Gp.adjacents_comb[current]:
                    Gp.adjacents_comb[current].remove(small_it)
    return

# 路网中每两个路口之间的距离
def junction_dis():
    # 新建字典
    for c_id in Gp.it_pos:
        Gp.junction_dis[c_id] = {}
    # 更新字典
    for c_id in Gp.it_pos:
        c_x = Gp.it_pos[c_id][0]
        c_y = Gp.it_pos[c_id][1]
        for d_id in Gp.it_pos:
            if c_id == d_id:
                d_cd = 0
            else:
                d_x = Gp.it_pos[d_id][0]
                d_y = Gp.it_pos[d_id][1]
                d_cd = nndis(c_x, c_y, d_x, d_y)
            Gp.junction_dis[c_id][d_id] = d_cd
    return

# 相邻路口间的道路长度
def adjacency_dis():
    # 新建字典
    for c_id in Gp.it_pos:
        Gp.adjacency_dis[c_id] = {}
    # 更新字典
    for c_id in Gp.it_pos:
        c_x = Gp.it_pos[c_id][0]
        c_y = Gp.it_pos[c_id][1]
        for n_id in Gp.adjacents_comb[c_id]:
            if c_id == n_id:
                d_cn = 0
            else:
                n_x = Gp.it_pos[n_id][0]
                n_y = Gp.it_pos[n_id][1]
                d_cn = nndis(c_x, c_y, n_x, n_y)
            Gp.adjacency_dis[c_id][n_id] = d_cn
    return

# 相邻路口之间的道路上的车辆数，车辆id
def inter_vehicles_num(node_info_dict, junctions_coordinate, adjacents):
    veh_num = {v: {u: 0 for u in adjacents[v]} for v in adjacents.keys()}  # 道路上车数
    veh_ = {v: {u: [] for u in adjacents[v]} for v in adjacents.keys()} # 道路上车辆信息
    one_way_veh_num = {v: {u: 0 for u in adjacents[v]} for v in adjacents.keys()}  # 道路上单向车数

    for current, adjacent_set in adjacents.items():
        for neighbor in adjacent_set:
            current_x = junctions_coordinate[current][0]  # x
            current_y = junctions_coordinate[current][1]  # y
            neighbor_x = junctions_coordinate[neighbor][0]  # x
            neighbor_y = junctions_coordinate[neighbor][1]  # y
            # 边界[x_min,y_min,x_max,y_max]
            if current_x > neighbor_x and current_y < neighbor_y:
                boundary = [neighbor_x, current_y, current_x, neighbor_y]
            elif current_x < neighbor_x and current_y < neighbor_y:
                boundary = [current_x, current_y, neighbor_x, neighbor_y]
            elif current_x < neighbor_x and current_y > neighbor_y:
                boundary = [current_x, neighbor_y, neighbor_x, current_y]
            elif current_x > neighbor_x and current_y > neighbor_y:
                boundary = [neighbor_x, neighbor_y, current_x, current_y]
            else:
                boundary = [0, 0, 0, 0]
                print("存在同轴的道路！")

            # 扩大覆盖范围
            if abs(current_x - neighbor_x) > abs(current_y - neighbor_y):
                    boundary[1] -= 60
                    boundary[3] += 60
            else:
                    boundary[0] -= 60
                    boundary[2] += 60

            # 统计每个邻居、每段上的车辆数
            num = 0
            # 遍历所有节点
            for node_id, node_pos in node_info_dict.items():
                if node_pos[0][0] >= boundary[0] and node_pos[0][0] <= boundary[2] and node_pos[0][1] >= boundary[1] and \
                        node_pos[0][1] <= boundary[3]:
                    num += 1
                    veh_[current][neighbor].append(node_id)
            veh_num[current][neighbor] = num
    return veh_num, veh_, one_way_veh_num

# 路口车辆
def intra_vehicles_num(node_info_dict, junctions_coordinate, adjacents):
    veh_detail = {v: [] for v in adjacents.keys()} # 每个区域范围内所有车 area_id: [node_id1,...],...
    node_area = {node: [] for node in node_info_dict} # 每个车所属的区域 node_id: [area1,...]...

    for current, adjacent_set in adjacents.items():
        for neighbor in adjacent_set:
            c_h = []
            current_x = junctions_coordinate[current][0]  # x
            current_y = junctions_coordinate[current][1]  # y
            neighbor_x = junctions_coordinate[neighbor][0]  # x
            neighbor_y = junctions_coordinate[neighbor][1]  # y
            half_x = (current_x + neighbor_x) / 2
            half_y = (current_y + neighbor_y) / 2
            # 根据两个路口的位置确定坐标范围（半程）
            if current_x > neighbor_x and current_y < neighbor_y:
                c_h = [[half_x, current_x], [current_y, half_y]]
            elif current_x < neighbor_x and current_y < neighbor_y:
                c_h = [[current_x, half_x], [current_y, half_y]]
            elif current_x < neighbor_x and current_y > neighbor_y:
                c_h = [[current_x, half_x], [half_y, current_y]]
            elif current_x > neighbor_x and current_y > neighbor_y:
                c_h = [[half_x, current_x], [half_y, current_y]]
            else:
                print("存在同轴的道路！")
            # 判断车辆属于两点（路口中心和车道中心）规定的范围内
            if abs(current_x - neighbor_x) > abs(current_y - neighbor_y):
                c_h[1][0] -= 60
                c_h[1][1] += 60
            else:
                c_h[0][0] -= 60
                c_h[0][1] += 60

            # 遍历所有的节点
            for node_id, node_pos in node_info_dict.items():
                # 车在范围内
                if node_pos[0][0] >= c_h[0][0] and node_pos[0][0] <= c_h[0][1] and node_pos[0][1] >= c_h[1][0] and \
                        node_pos[0][1] <= c_h[1][1]:
                    if current not in node_area[node_id]:
                        node_area[node_id].append(current)
                    veh_detail[current].append(node_id)
    return veh_detail, node_area

def process(it_pos, adjacent_comb, x_min, x_max, y_min, y_max):
    it_new = {}
    ad_new = {}
    for it, pos in it_pos.items():
        if (pos[0]>x_min and pos[0]<x_max) and (pos[1]>y_min and pos[1]<y_max):
        # if (pos[0] > 2000 and pos[0] < 3000) and (pos[1] > 2000 and pos[1] < 3000):
            it_new[it] = [pos[0], pos[1]]
    for ad, item in adjacent_comb.items():
        if ad in it_new:
            ad_new[ad] = []
            for i in item:
                if i in it_new:
                    ad_new[ad].append(i)
    # print(len(it_new))
    # for it, neibs in ad_new.items():
    #     if not neibs:
    #         print('errrrrr')
    x = []
    for jun in it_new:
        if len(ad_new[jun]) <= 1:
            for v in ad_new[jun]:
                ad_new[v].remove(jun)
            ad_new.pop(jun)
            x.append(jun)
    for x1 in x:
        it_new.pop(x1)
    # for it, neibs in ad_new.items():
    #     if len(neibs) <= 1:
    #         print('errrrrre')
    # for j, ns in ad_new.items():
    #     print(j, ns)
    # print(len(it_new), len(ad_new))
    return it_new, ad_new