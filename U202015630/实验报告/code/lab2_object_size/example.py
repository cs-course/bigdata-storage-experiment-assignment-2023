# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread
from tqdm import tqdm

import swiftclient


def bench_put(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 鎵€寤哄璞″悕
    start = time.time()
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)  # 灏嗘湰鍦版枃浠朵笂浼犱负瀵硅薄
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


def bench_get(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 鎵€寤哄璞″悕
    start = time.time()
    # print(current_thread().name,'start',start)
    resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
    with open(obj_name, 'wb') as f:
        f.write(obj_contents)
    end = time.time()
    # print(current_thread().name,'end',end)
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


def bench_delete(i):
    obj_name = '%s%08d' % (object_name_prefix, i)  # 鎵€寤哄璞″悕
    start = time.time()
    conn.delete_object(bucket_name, obj_name)
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)


switch = {'write': bench_put, 'read': bench_get, 'delete': bench_delete}
def run_test(test_type):
    print('-----' + test_type + '-----')
    latency = []
    failed_requests = []
    test_start_time = time.time()
    with tqdm(desc="Accessing S3", total=num_samples) as pbar:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:  # 閫氳繃 max_workers 璁剧疆骞跺彂绾跨▼鏁�
            futures = [
                executor.submit(
                    switch[test_type],
                    i) for i in range(num_samples)  # 涓轰繚璇佺嚎绋嬪畨鍏紝搴旂粰姣忎釜浠诲姟鐢宠涓€涓柊 resource
            ]
            for future in as_completed(futures):  # as_completed(futures)鎶奻utures涓墍鏈変换鍔℃寜瀹屾垚鏃堕棿鍏堝悗椤哄簭鎺掑簭锛侊紒
                if future.exception():
                    failed_requests.append(future)
                else:
                    latency.append(future.result())  # 姝ｇ‘瀹屾垚鐨勮姹傦紝閲囬泦寤惰繜
                pbar.update(1)
    test_end_time = time.time()
    test_duration = test_end_time - test_start_time # s
    test_transferred = len(latency) * object_size # KB
    test_total_throughput=test_transferred/test_duration # KB/s
    test_average_latency=sum([latency[i][0] for i in range(len(latency))]) / len(latency) # s
    print('total duration: ', test_duration , 's')
    print('average latency: ', test_average_latency,"s")
    print('total transferred: ', test_transferred , 'KB')
    print('total throughput: ', test_transferred / test_duration, 'KB/s')
    print('success rate: ', len(latency) / num_samples * 100, '%')

    # tracefile_name = test_type + '_' + str(object_size) + '_' + str(num_clients) + '_' + str(num_samples) + '.csv'
    # with open(tracefile_name, "w+") as tracefile:
    #     tracefile.write("id,latency,start,end,client\n")
    #     tracefile.writelines([','.join(map(str, (i,) + latency[i])) + '\n' for i in range(len(latency))])
    if test_type=="write":
        with open(result_file,"a") as rf:
            rf.write("object_size: " + str(object_size) + " KB\n")
            rf.write("num_samples: " + str(num_samples) + "\n")
            rf.write("write_total_throughput: " + str(test_total_throughput) + " KB/s\n")
            rf.write("write_average_latency: " +str(test_average_latency) + " s\n")
    if test_type == "read":
        with open(result_file, "a") as rf:
            rf.write("object_size: " + str(object_size) + " KB\n")
            rf.write("num_samples: " + str(num_samples) + "\n")
            rf.write("read_total_throughput: " + str(test_total_throughput) + " KB/s\n")
            rf.write("read_average_latency: " + str(test_average_latency) + " s\n")


endpoint = 'http://123.60.165.6:12345/'
_user = 'test:tester'
_key = 'testing'
bucket_name = 'testbucket'
object_name_prefix = 'testObj'
object_sizes=[1,2,4,8,16,32,64,128,256,512,1024] # /KB
total_size= 4*1024 # /KB    4MB
num_clients = 10
result_file="result.out"
print('endpoint: ', endpoint)
print('bucket_name: ', bucket_name)
print('object_name_prefix: ', object_name_prefix)
print('num_clients: ', num_clients)


if os.path.exists(result_file):
    os.remove(result_file)

# 连接
conn = swiftclient.Connection(authurl=endpoint + 'auth/v1.0',user=_user,key=_key)

for object_size in object_sizes:
    num_samples = int(total_size/object_size)
    print("=====TEST=====")
    print("object_size:",object_size)
    print("num_samples:",num_samples)
    # 建立新容器
    conn.put_container(bucket_name)
    print('Test bucket %s created.' % bucket_name)

    # 初始化大小为object_size的文件
    local_file = "_test.bin"
    test_bytes = [0xFF for i in range(object_size*1024)]
    with open(local_file, "wb") as lf:
        lf.write(bytearray(test_bytes))
    print('Test file %s created.' % local_file)

    run_test('write')
    run_test('read')
    run_test('delete')

    # 删除本地文件
    for i in range(num_samples):
        obj_name = '%s%08d' % (object_name_prefix, i)
        os.remove(obj_name)
    print('Downloaded files deleted.')

    # 删除数据文件
    os.remove(local_file)
    print('Test file %s deleted.' % local_file)

    # 删除容器
    conn.delete_container(bucket_name)
    print('Test bucket %s deleted.' % bucket_name)
