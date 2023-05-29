# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread
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

# test parameters
print('endpoint: ', endpoint)
print('bucket_name: ', bucket_name)
print('object_name_prefix: ', object_name_prefix)
print('object_size: ', object_size)
print('num_clients: ', num_clients)
print('num_samples: ', num_samples)

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


def bench_put(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 所建对象名
    start = time.time() * 1000  # 换算为毫秒
    # print(current_thread().name,'start',start)
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)  # 将本地文件上传为对象
    end = time.time() * 1000
    # print(current_thread().name,'end',end)
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


def bench_get(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 所建对象名
    start = time.time() * 1000  # 换算为毫秒
    # print(current_thread().name,'start',start)
    resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
    with open(obj_name, 'wb') as f:
        f.write(obj_contents)
    end = time.time() * 1000
    # print(current_thread().name,'end',end)
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


def bench_delete(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 所建对象名
    start = time.time() * 1000  # 换算为毫秒
    # print(current_thread().name,'start',start)
    conn.delete_object(bucket_name, obj_name)
    end = time.time() * 1000
    # print(current_thread().name,'end',end)
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


switch = {'put': bench_put, 'get': bench_get, 'delete': bench_delete}


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

    tracefile_name = test_type + '_' + str(object_size) + '_' + str(num_clients) + '_' + str(num_samples) + '.csv'
    with open(tracefile_name, "w+") as tracefile:
        tracefile.write("id,latency,start,end,client\n")
        tracefile.writelines([','.join(map(str, (i,) + latency[i])) + '\n' for i in range(len(latency))])


run_test('put')
run_test('get')
run_test('delete')

for i in range(num_samples):
    obj_name = '%s%08d' % (object_name_prefix, i)  #
    os.remove(obj_name)
print('Downloaded files deleted.')

os.remove(local_file)
print('Test file %s deleted.' % local_file)

conn.delete_container(bucket_name)
print('Test bucket %s deleted.' % bucket_name)
