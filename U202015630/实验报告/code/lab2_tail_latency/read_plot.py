import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.pyplot import MultipleLocator, plot



latency = pd.read_csv('./get_4096_10_256.csv',usecols=['latency']).apply(pd.to_numeric).values

latency=latency*1000

plt.title('Read Latency Distribution')
plt.subplot(211)
plt.ylabel('Read latency / ms')
plt.plot(latency)
plt.subplot(212)
plt.plot(sorted(latency, reverse=True))
plt.ylabel('Read latency / ms')

plt.savefig('./read_tail_latency.png')
plt.show()

latency=latency[latency[:, 0].argsort()]
cnt=len(latency)
latency_max=latency[cnt-1]
latency_99th=latency[int(cnt*0.99)]
latency_90th=latency[int(cnt*0.9)]
latency_75th=latency[int(cnt*0.75)]
latency_50th=latency[int(cnt*0.50)]
latency_25th=latency[int(cnt*0.25)]
with open("read_tail_latency.txt", "w") as file:
    file.write("read tail latency:\n")
    file.write("latency_max:\t%f ms\n" %(latency_max))
    file.write("latency_99th:\t%f ms\n" % (latency_99th))
    file.write("latency_90th:\t%f ms\n" % (latency_90th))
    file.write("latency_75th:\t%f ms\n" % (latency_75th))
    file.write("latency_50th:\t%f ms\n" % (latency_50th))
    file.write("latency_25th:\t%f ms\n" % (latency_25th))


# 设置百分位纵轴
ax = plt.gca()
# ax.xaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
# 避免横轴数据起始位置与纵轴重合，调整合适座标范围
x_min = max(min(latency) * 0.8, min(latency) - 5)
x_max = max(latency)
plt.xlim(x_min, x_max)
# 绘制实际百分位延迟
plt.hist(latency, cumulative=True, histtype='step', weights=[1./ len(latency)] * len(latency))

# 排队论模型
# F(t)=1-e^(-1*a*t)
alpha = 0.05
X_qt = np.arange(min(latency), max(latency), 1.)
Y_qt = 1 - np.exp(alpha * (min(latency) - X_qt))
# 绘制排队论模型拟合
plt.plot(X_qt, Y_qt)
plt.xlabel('Read latency / ms')
plt.title('Read Latency Distribution')
plt.grid()
plt.show()
plt.savefig('./read_tail_latency_queue.png')

