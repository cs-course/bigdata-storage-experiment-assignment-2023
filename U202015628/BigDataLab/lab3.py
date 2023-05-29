import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import threading
from tqdm import tqdm

import swiftclient

endpoint = 'http://221.9.165.166:12345/'
_user = 'test:tester'
_key = 'testing'

conn = swiftclient.Connection(
    authurl=endpoint + 'auth/v1.0',
    user=_user,
    key=_key
)

bucket_name = 'testbucket'
object_name_prefix = 'testObj'
object_size = 4 * 1024  # 4KB
num_clients = 5
num_samples = 200
wait_time = 0.1263  # 相邻两次对冲请求发起的时间间隔，若wait_time=0即为关联请求
request_num = 5  # 对冲/关联请求总共发起的请求数

# test parameters
print('endpoint: ', endpoint)
print('bucket_name: ', bucket_name)
print('object_name_prefix: ', object_name_prefix)
print('object_size: ', object_size)
print('num_clients: ', num_clients)
print('num_samples: ', num_samples)
print('wait_time: ', wait_time)
print('request_num: ', request_num)

# 新建一个实验用 bucket (注意："bucket name" 中不能有下划线)
conn.put_container(bucket_name)
print('Test bucket %s created.' % bucket_name)

# 准备负载，可以按照几种不同请求到达率 (Inter-Arrival Time, IAT) 设置。
# 初始化本地数据文件
local_file = "_test.bin"
test_bytes = [0xFF for i in range(object_size)]  # 填充至所需大小
with open(local_file, "wb") as lf:
    lf.write(bytearray(test_bytes))
print('Test file %s created.' % local_file)

fup = open(local_file, 'rb')


def bench_put(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 所建对象名
    flag = True
    end = 0

    def func():
        nonlocal end
        nonlocal flag
        if (flag):
            conn.put_object(bucket_name, obj_name, fup)  # 将本地文件上传为对象
        if (flag):
            end = time.time() * 1000
        if (flag):
            flag = False

    start = time.time() * 1000
    for _ in range(request_num):
        if (not flag):
            break
        t1 = threading.Thread(target=func)
        if (not flag):
            break
        t1.start()
        if (not flag):
            break
        time.sleep(wait_time)
    while (flag):
        pass
    duration = end - start
    # print(duration)
    client = threading.current_thread().name
    return (duration, start, end, client)


switch = {'put': bench_put}


def run_test(test_type):
    print('Running ' + test_type + ' test...')
    latency = []
    failed_requests = []
    test_start_time = time.time() * 1000
    with tqdm(desc="Accessing S3", total=num_samples) as pbar:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:  # 通过 max_workers 设置并发线程数
            futures = [
                executor.submit(
                    switch[test_type],
                    i) for i in range(num_samples)  # 为保证线程安全，应给每个任务申请一个新 resource
            ]
            for future in as_completed(futures):  # as_completed(futures)把futures中所有任务按完成时间先后顺序排序！！
                if future.exception():
                    failed_requests.append(future)
                else:
                    latency.append(future.result())  # 正确完成的请求，采集延迟
                pbar.update(1)
    test_end_time = time.time() * 1000
    test_duration = test_end_time - test_start_time
    test_transferred = len(latency) * object_size
    print('total duration: ', test_duration / 1024, 's')
    print('average latency: ', sum([latency[i][0] for i in range(len(latency))]) / len(latency))
    print('total transferred: ', test_transferred / 1024, 'KB')
    print('total throughput: ', test_transferred / test_duration, 'KB/s')
    print('success rate: ', len(latency) / num_samples * 100, '%')

    tracefile_name = 'h_' + str(wait_time) + '_' + str(request_num) + '_' + test_type + '_' + str(
        object_size) + '_' + str(num_clients) + '_' + str(num_samples) + '.csv'
    with open(tracefile_name, "w+") as tracefile:
        tracefile.write("id,latency,start,end,client\n")
        tracefile.writelines([','.join(map(str, (i,) + latency[i])) + '\n' for i in range(len(latency))])


run_test('put')

fup.close()

os.remove(local_file)
print('Test file %s deleted.' % local_file)

# conn.delete_container(bucket_name)
# print('Test bucket %s deleted.'%bucket_name)
