import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from boto3.session import Session
import botocore
from tqdm import tqdm
import throttle

# 准备密钥
aws_access_key_id = 'admin'
aws_secret_access_key = 'password'

# 本地S3服务地址
local_s3 = 'http://10.21.190.174:9000'
# 建立会话
session = Session(aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  )
# 连接到服务
s3 = session.resource('s3', endpoint_url=local_s3)
# 创建bucket
for bucket in s3.buckets.all():
    print('bucket name:%s' % bucket.name)
bucket_name = "loadgen"
if s3.Bucket(bucket_name) not in s3.buckets.all():
    s3.create_bucket(Bucket=bucket_name)
# 检查该bucket下是否有对象
bucket = s3.Bucket(bucket_name)
for obj in bucket.objects.all():
    print('obj name:%s' % obj.key)

# 初始化本地数据文件
SIZE="4K"
local_file = "_test_"+SIZE+".bin"
test_bytes = [0xFF for i in range(1024 * 4)]  # 填充至所需大小

with open(local_file, "wb") as lf:
    lf.write(bytearray(test_bytes))

# 发起请求和计算系统停留时间
def request_timing(s3res, i):  # 使用独立 session.resource 以保证线程安全
    obj_name = "testObj%08d" % (i,)  # 所建对象名
    # temp_file = '.tempfile'
    service_time = 0  # 系统滞留时间
    start = time.time()
    s3res.Object(bucket_name, obj_name).upload_file(local_file)  # 将本地文件上传为对象
    # 或
    # bucket.put_object(Key=obj_name, Body=open(local_file, 'rb'))
    # 下载obj
    # s3res.Object(bucket_name, obj_name).download_file(temp_file)
    end = time.time()
    system_time = end - start
    return system_time * 1000  # 换算为毫秒


# 按照请求到达率限制来执行和跟踪请求
def arrival_rate_max(s3res, i):  # 不进行限速
    return request_timing(s3res, i)


@throttle.wrap(0.1, 2)  # 100ms 内不超过 2 个请求，下同……
def arrival_rate_2(s3res, i):
    return request_timing(s3res, i)


@throttle.wrap(0.1, 4)
def arrival_rate_4(s3res, i):
    return request_timing(s3res, i)


@throttle.wrap(0.1, 8)
def arrival_rate_8(s3res, i):
    return request_timing(s3res, i)


# 发起请求
latency = []
# failed_requests = []

with tqdm(desc="Accessing S3", total=100) as pbar:  # 进度条设置，合计执行 100 项上传任务 (见 submit 部分)，进度也设置为 100 步
    with ThreadPoolExecutor(max_workers=1) as executor:  # 通过 max_workers 设置并发线程数
        futures = [
            executor.submit(
                arrival_rate_max,
                session.resource('s3', endpoint_url=local_s3), i) for i in range(100)
            # 为保证线程安全，应给每个任务申请一个新 resource
        ]
        for future in as_completed(futures):
            # if future.exception():
            #     failed_requests.append(futures[future])
            # else:
            latency.append(future.result())   # 正确完成的请求，采集延迟
            pbar.update(1)

# 清理

try:
    # 删除bucket下所有object
    bucket.objects.filter().delete()

    # 删除bucket下某个object
    # bucket.objects.filter(Prefix=obj_name).delete()
    bucket.delete()
except botocore.exceptions.ClientError as e:
    print('error in bucket removal')

with open("latency"+SIZE+".csv", "w+") as tracefile:
    tracefile.write("latency\n")
    tracefile.writelines([str(l) + '\n' for l in latency])
