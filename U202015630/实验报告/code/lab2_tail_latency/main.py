# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread
from tqdm import tqdm

import swiftclient

endpoint = 'http://47.113.185.143:12345/'
_user = 'test:tester'
_key = 'testing'

conn = swiftclient.Connection(authurl=endpoint + 'auth/v1.0',user=_user,key=_key)

bucket_name = 'testbucket'
object_name_prefix = 'testObj'
object_size = 4 * 1024  # B  =4KB
num_clients = 10
num_samples = 256

# test parameters
print('endpoint: ', endpoint)
print('bucket_name: ', bucket_name)
print('object_name_prefix: ', object_name_prefix)
print('object_size: ', object_size)
print('num_clients: ', num_clients)
print('num_samples: ', num_samples)

conn.put_container(bucket_name)
print('Test bucket %s created.' % bucket_name)

local_file = "_test.bin"
test_bytes = [0xFF for i in range(object_size)]
with open(local_file, "wb") as lf:
    lf.write(bytearray(test_bytes))
print('Test file %s created.' % local_file)


def bench_put(i):
    obj_name = '%s%08d' % (object_name_prefix, i)
    start = time.time()                             # 对一个对象的传输任务的开始时间
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)
    end = time.time()                               # 结束时间
    # print(current_thread().name,'end',end)
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


def bench_get(i):
    obj_name = '%s%08d' % (object_name_prefix, i)
    start = time.time()
    resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
    with open(obj_name, 'wb') as f:
        f.write(obj_contents)
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


def bench_delete(i):
    obj_name = '%s%08d' % (object_name_prefix, i)
    start = time.time()
    conn.delete_object(bucket_name, obj_name)
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


switch = {'put': bench_put, 'get': bench_get, 'delete': bench_delete}


def run_test(test_type):
    print('Running ' + test_type + ' test...')
    latency = []
    failed_requests = []
    test_start_time = time.time()               # 所有对象的传输任务的开始时间
    with tqdm(desc="Accessing S3", total=num_samples) as pbar:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = [executor.submit(switch[test_type],i) for i in range(num_samples)]
            for future in as_completed(futures):
                if future.exception():
                    failed_requests.append(future)
                else:
                    latency.append(future.result())
                pbar.update(1)
    test_end_time = time.time()                 # 所有对象的传输任务的结束时间
    test_duration = test_end_time - test_start_time
    test_transferred = len(latency) * object_size
    print('total duration: ', test_duration, 's')
    print('average latency: ', sum([latency[i][0] for i in range(len(latency))]) / len(latency))
    print('total transferred: ', test_transferred / 1024, 'KB')
    print('total throughput: ', test_transferred/1024 / test_duration, 'KB/s')
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
