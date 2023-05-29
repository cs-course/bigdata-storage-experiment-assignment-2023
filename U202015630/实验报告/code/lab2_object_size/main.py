# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread
from tqdm import tqdm

import swiftclient


def bench_put(i):
    """
    向容器内写入object_name_prefix+i
    :param i:
    :return:
    """
    obj_name="%s%08d" %(object_name_prefix,i) # 对象名 一个对象大小为object_size,共num_samples个对象
    start=time.time()*1000 # 开始时间
    with open(local_file,"rb") as f:
        conn.put_object(bucket_name,obj_name,f) # 上传到swift  容器名 | 对象名 | 文件名
    end=time.time()*1000 # 结束时间
    return (end - start, start, end, current_thread().name)

def bench_get(i):
    """
    从容器内读object_name_prefix+i到本地
    :param i:
    :return:
    """
    obj_name = "%s%08d" % (object_name_prefix, i)
    start=time.time()*1000
    resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
    with open(obj_name, 'wb') as f:
        f.write(obj_contents)
    end=time.time()*1000
    return (end-start,start,end,current_thread().name)

def bench_delete(i):
    """
    从容器中删除object_name_prefix+i
    :param i:
    :return:
    """
    obj_name = "%s%08d" % (object_name_prefix, i)
    start=time.time()*1000
    conn.delete_object(bucket_name,obj_name)
    end=time.time()*1000
    return (end-start,start,end,current_thread().name)

switch={"write":bench_put,"read":bench_get,"delete":bench_delete}
def run_test(test_type):
    print("-----"+test_type+"-----")
    latency=[]          # 延迟
    failed_requests=[]
    test_start_time=time.time()*1000    # 开始时间/s
    with tqdm(desc="Accessing S3", total=num_samples) as pbar:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:  # 通过 max_workers 设置并发线程数
            futures = [executor.submit(switch[test_type],i) for i in range(num_samples)]  # 为保证线程安全，应给每个任务申请一个新 resource
            for future in as_completed(futures):  # as_completed(futures)把futures中所有任务按完成时间先后顺序排序！！
                if future.exception():
                    failed_requests.append(future)
                else:
                    latency.append(future.result())  # 正确完成的请求，采集延迟
                pbar.update(1)

            executor.shutdown()
    test_end_time=time.time()*1000

    test_duration=test_end_time-test_start_time # 总传输时间 s
    test_transferred=len(latency)*object_size # 总传输数据量 KB
    test_total_throuthput=test_transferred / test_duration # 总传输带宽 KB/s
    test_average_latency=sum([latency[i][0] for i in range(len(latency))]) / len(latency)
    print('total duration:', test_duration , 's')
    print('average latency:', test_average_latency,"s")
    print('total transferred:', test_transferred , 'KB')
    print('total throughput:', test_total_throuthput, 'KB/s')
    print('success rate: ', len(latency) / num_samples * 100, '%')

    # tracefile_name = test_type + '_' + str(object_size) + '_' + str(num_clients) + '_' + str(num_samples) + '.csv'
    # with open(tracefile_name, "w+") as tracefile:
    #     tracefile.write("id,latency,start,end,client\n")
    #     tracefile.writelines([','.join(map(str, (i,) + latency[i])) + '\n' for i in range(len(latency))])
    print(test_type)
    if test_type=="write":
        with open(result_file,"a") as rf:
            rf.write("object_size: " + str(object_size) + " KB\n")
            rf.write("num_samples: " + str(num_samples) + "\n")
            rf.write("write_total_throughput: " + str(test_total_throuthput) + " KB/s\n")
            rf.write("write_average_latency: " +str(test_average_latency) + " s\n")
    if test_type == "read":
        with open(result_file, "a") as rf:
            rf.write("object_size: " + str(object_size) + " KB\n")
            rf.write("num_samples: " + str(num_samples) + "\n")
            rf.write("read_total_throughput: " + str(test_total_throuthput) + " KB/s\n")
            rf.write("read_average_latency: " + str(test_average_latency) + " s\n")



AUTH="http://123.60.165.6:12345/auth/v1.0"
USER="test:tester"
KEY="testing"


object_sizes=[1,2,4,8,16,32,64,128,256,512,1024]  # 单位 KB 1KB 2KB 4KB 8KB 64KB 128KB 256KB 512KB 1024KB
bucket_name="lab2bucket"
object_name_prefix="lab2obj"
local_file = "_test.bin"
result_file = "result.out"
total_size= 1*1024              # 单位KB 数据总量为1024KB
num_clients=10                  # 客户端的数量

print("AUTH:",AUTH)
print("USER:",USER)
print("KEY:",KEY)
print("bucket_name:",bucket_name)
print("object_name_prefix:",object_name_prefix)
print("num_clients:",num_clients)
print("total_size:",total_size,"KB")


# 连接openstack-swift
conn=swiftclient.Connection(AUTH,USER,KEY)

if os.path.exists(local_file):
    os.remove(local_file)
if os.path.exists(result_file):
    os.remove(result_file)

for object_size in object_sizes:
    num_samples = int(total_size / object_size)

    # 初始化传输文件
    test_bytes = [0xff for i in range(object_size*1024)]
    with open(local_file, "wb") as lf:
        lf.write(bytearray(test_bytes))

    # 在swift中新建容器
    try:
        conn.head_container(bucket_name)
        conn.delete_container(bucket_name)
        conn.put_container(bucket_name)
        print("delete and create a new bucket")
    except Exception as e:
        conn.put_container(bucket_name)
        print("create a new bucket")

    # 写/读
    print("=====TEST=====")
    print("object_size:",object_size,"KB")
    print("num_samples:",num_samples)
    run_test("write")
    run_test("read")

    # 删除读到本地的文件
    for i in range(num_samples):
        obj_name = '%s%08d' % (object_name_prefix, i)  #
        if os.path.exists(obj_name):
            os.remove(obj_name)
    # 删除该容器
    try:
        conn.delete_container(bucket_name)
    except Exception as e:
        print("delete container fail")


