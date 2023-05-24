em_classes = ['常规员工', '专家', '管理员', '未定义']
em_belong = ['大型建筑设备修理', '汽车修理', '家电修理', '计算机修理', '未定义']


def process(employee):
    data = employee.__dict__
    data.update({'em_classes': em_classes[data['em_classes']]})
    data.update({'em_belong': em_belong[data['em_belong']]})
    return data
