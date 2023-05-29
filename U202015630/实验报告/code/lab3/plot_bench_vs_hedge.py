import matplotlib.pyplot as plt
import numpy as np

# 生成数据
N = 8
bench = (91.495424,200.810909,175.492525,115.536690,104.833364,94.036102,87.633610,83.541393)
hedge = (94.581556, 134.428024, 128.073454 , 119.081020, 111.328840,101.387739,91.931105,86.335182)


ind = np.arange(N)
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(ind, bench, width)
rects2 = ax.bar(ind + width, hedge, width)

# 设置x轴标签
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('average\nlatency', 'max\nlatency', '99th\nlatency', '95th\nlatency', '90th\nlatency',"75th\nlatency","50th\nlatency","25th\nlatency"),rotation=45)

# 添加题目和图例
ax.set_title("read latency of normol request and hedging request")
ax.legend((rects1[0], rects2[0]), ('normol', 'hedging request'))

plt.tight_layout()
plt.show()
plt.savefig("read latency of normol request and hedging request.png")