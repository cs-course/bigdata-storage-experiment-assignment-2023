# -*- coding: utf-8 -*-
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread

import swiftclient

endpoint = 'http://localhost:12345/'
_user = 'hustobs:hustobs'
_key = 'key'

conn = swiftclient.Connection(
    authurl=endpoint+'auth/v1.0',
    user=_user,
    key=_key
)

if len(sys.argv) != 4:
    print('Please input object_size, num_clients and num_samples')
    sys.exit()

bucket_name = 'test-bucket'
object_name_prefix = 'test-obj'
object_size = int(sys.argv[1])
num_clients = int(sys.argv[2])
num_samples = int(sys.argv[3])

# test parameters
print('endpoint: ', endpoint)
print('bucket_name: ', bucket_name)
print('object_name_prefix: ', object_name_prefix)
print('object_size: ', object_size, 'B')
print('num_clients: ', num_clients)
print('num_samples: ', num_samples)

conn.put_container(bucket_name)
print('Test bucket %s created.' % bucket_name)

# 初始化本地数据文件
local_file = "test.bin"
test_bytes = [0xFF for i in range(object_size)]  # 填充至所需大小
with open(local_file, "wb") as lf:
    lf.write(bytearray(test_bytes))
print('Test file %s created.' % local_file)


def bench_put(i):
    obj_name = object_name_prefix + str(i)  
    start = time.time()
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)  
    end = time.time()
    return (end - start) * 1000


def bench_get(i):
    obj_name = object_name_prefix + str(i) 
    start = time.time()
    _, obj_contents = conn.get_object(bucket_name, obj_name)
    with open(obj_name, 'wb') as f:
        f.write(obj_contents)
    end = time.time()
    return (end - start) * 1000


def bench_delete(i):
    obj_name = object_name_prefix + str(i)
    start = time.time()
    conn.delete_object(bucket_name, obj_name)
    end = time.time()
    return (end - start) * 1000


def run_test(func):
    print('Running ' + func.__name__[6:] + ' test...')
    latency = []
    failed_requests = []
    test_start = time.time()
    # 通过 max_workers 设置并发线程数
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [
            # 为保证线程安全，应给每个任务申请一个新 resource
            executor.submit(func, i) for i in range(num_samples)
        ]
        # as_completed(futures)把futures中所有任务按完成时间先后顺序排序！！
        for future in as_completed(futures):
            if future.exception():
                failed_requests.append(future)
            else:
                latency.append(future.result())  # 正确完成的请求，采集延迟
    test_end = time.time()
    test_duration = test_end - test_start
    test_transferred = len(latency) * object_size
    print('total duration: ', test_duration, 's')
    print('average latency: ', sum(latency) / len(latency), 'ms')
    print('total transferred: ', test_transferred / 1024, 'KB')
    print('total throughput: ', test_transferred / 1024 / test_duration, 'KB/s')
    print('success rate: ', len(latency) / num_samples * 100, '%')

    tracefile_name = func.__name__[6:] + '_' + \
        str(object_size)+'_'+str(num_clients)+'_'+str(num_samples)+'.csv'
    print('writing latency to %s' % tracefile_name)
    with open(tracefile_name, "w+") as tracefile:
        tracefile.write("latency\n")
        tracefile.writelines([str(l) + '\n' for l in latency])
    print('----------------------------------------------------')


run_test(bench_put)
run_test(bench_get)
run_test(bench_delete)


for i in range(num_samples):
    obj_name = object_name_prefix + str(i)
    os.remove(obj_name)
print('Downloaded files deleted.')

# os.remove(local_file)
print('Test file %s deleted.' % local_file)

# conn.delete_container(bucket_name)
# print('Test bucket %s deleted.' % bucket_name)

