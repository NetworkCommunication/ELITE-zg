
# 计算模糊规则表
m = []
L1 = 'Good'
L2 = 'High'
L3 = 'Close'
R1 = 'Excellent'
g_all = []
g_list = []
for score1 in (1, 2/3, 1/3):
    if score1 == 1:
        L1 = 'Good'
    elif score1 == 2/3:
        L1= 'Medium'
    else:
        L1 = 'Poor'
    for score2 in (1, 2/3, 1/3):
        if score2 == 1:
            L2 = 'High'
        elif score2 == 2 / 3:
            L2 = 'Middle'
        else:
            L2 = 'Low'
        g_ll = []
        for score3 in (1, 2/3, 1/3):
            if score3 == 1:
                L3 = 'Close'
            elif score3 == 2 / 3:
                L3 = 'Medium'
            else:
                L3 = 'Far'
            r = [L1, L2, L3]
            g = score1*(1/2) + score2*(1/4) + score3*(1/4)
            g_ll.append(round(g,3))
            g_all.append(round(g,3))
            if g < 0.5:
                R1 = 'Worst'
            elif g>=0.5 and g<0.65:
                R1 = 'Bad'
            elif g>=0.65 and g<=0.75:
                R1 = 'Medium'
            elif g>0.75 and g<=0.9:
                R1 = 'Good'
            elif g>0.9 and g<=1:
                R1 = 'Excellent'
            r.append(R1)
            m.append(r)
        g_list.append(g_ll)
print(m)
for mm in m:
    print(mm)
print(g_list)
print(len(g_list))
for l in g_list:
    print(l)
g_all.sort()
print(g_all)


