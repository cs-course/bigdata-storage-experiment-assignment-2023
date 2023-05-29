# 画散点图
import matplotlib.pyplot as plt
import re

f = open('MinIO/output_0.txt', 'r')
text = f.read()
f.close()
# 使用正则表达式匹配数字和单位
text = text.split('\n')[12:]
text = '\n'.join(text)
pattern = r'\d+\.\d+s'
# 使用正则表达式匹配每个指标的值
matches = re.findall(pattern, text)
write_time = matches[0:100]
read_time = matches[100:201]
# print(write_time)
# print(read_time)

# 提取时间戳和响应时间
timestamps = [i+1 for i in range(100)]
print(timestamps, write_time, read_time)
# 绘制散点图
plt.scatter(timestamps, write_time, label='write', s=5)
# plt.plot(timestamps, write_time, label='write')
plt.scatter(timestamps, read_time, label='read', s=5)
plt.legend()
plt.ylim(min(min(write_time), min(read_time)), max(max(write_time), max(read_time)))

plt.xlabel('timestamp')
plt.ylabel('response time')

# 将y轴的刻度间隔设置为1秒钟
plt.show()