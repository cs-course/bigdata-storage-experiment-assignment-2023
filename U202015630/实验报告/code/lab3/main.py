# -*- coding: utf-8 -*-
import os
import time
from threading import current_thread
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED,as_completed

import swiftclient

# endpoint = 'http://47.113.185.143:12345/'
endpoint='http://221.9.165.166:12345/'
_user = 'test:tester'
_key = 'testing'

conn = swiftclient.Connection(authurl=endpoint + 'auth/v1.0',user=_user,key=_key)

bucket_name = 'testbucket'
object_name_prefix = 'testObj'
object_size = 1 * 512  # B    0.25 KB * 1024 = 0.25 MB
num_clients = 4
num_samples = 1024

print('endpoint: ', endpoint)
print('bucket_name: ', bucket_name)
print('object_name_prefix: ', object_name_prefix)
print('object_size: ', object_size/1024, "KB")
print('num_clients: ', num_clients)
print('num_samples: ', num_samples)

conn.put_container(bucket_name)
print('Test bucket %s created.' % bucket_name)

local_file = "_test.bin"
test_bytes = [0xFF for i in range(object_size)]
with open(local_file, "wb") as lf:
    lf.write(bytearray(test_bytes))
print('Test file %s created.' % local_file)

hedge_flag=0
hedge_record=[]
hedge_time=0.1155
# hedge_time=0.133
hedge_cnt=1

def bench_put(i):
    obj_name = '%s%08d' % (object_name_prefix, i)
    start = time.time()                             # 鐎甸€涚娑擃亜顕挒锛勬畱娴肩姾绶禒璇插閻ㄥ嫬绱戞慨瀣闂傦拷
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)
    end = time.time()                               # 缂佹挻娼弮鍫曟？
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

def hedge_get(i):
    obj_name = '%s%08d' % (object_name_prefix, i)
    start = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        future=executor.submit(conn.get_object,bucket_name,obj_name)
        wait([future],timeout=hedge_time)
        if not future.done():
            hedge_record.append(i)
            hedge_requests = [executor.submit(conn.get_object,bucket_name,obj_name) for i in range(hedge_cnt)]
            hedge_requests.append(future)
            done, not_done = wait(hedge_requests, return_when=FIRST_COMPLETED)
            for future in not_done:
                future.cancel()
            resp_headers, obj_contents = done.pop().result()
        else:
            resp_headers, obj_contents = future.result()
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

switch = {'put': bench_put,'bench_get': bench_get, 'delete': bench_delete,'hedge_get':hedge_get}

def run_test(test_type):
    print('Running ' + test_type + ' test...')
    latency = []
    failed_requests = []
    test_start_time = time.time()
    with tqdm(desc="Accessing S3", total=num_samples) as pbar:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = [executor.submit(switch[test_type],i) for i in range(num_samples)]
            for future in as_completed(futures):
                if future.exception():
                    failed_requests.append(future)
                else:
                    latency.append(future.result())
                pbar.update(1)
    test_end_time = time.time()
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
if hedge_flag:
    run_test('hedge_get')
else:
    run_test('bench_get')
run_test('delete')

for i in range(num_samples):
    obj_name = '%s%08d' % (object_name_prefix, i)  #
    os.remove(obj_name)
print('Downloaded files deleted.')

os.remove(local_file)
print('Test file %s deleted.' % local_file)

conn.delete_container(bucket_name)
print('Test bucket %s deleted.' % bucket_name)
print(hedge_record)