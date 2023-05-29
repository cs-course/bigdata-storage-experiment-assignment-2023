#!/bin/bash
# Locate s3bench
s3bench=~/Go/bin/s3bench
if [ -n "$GOPATH" ]; then
    s3bench=$GOPATH/bin/s3bench
fi
NumClient=(1 1 1 1)
NumSample=(100 100 100 100)
ObjectSize=(1048576 2097152 8388608) #1MB 2MB 16MB
# 循环执行S3bench
for i in "${!ObjectSize[@]}"; do
    # 从数组中获取参数
    num_client=${NumClient[$i]}
    num_sample=${NumSample[$i]}
    object_size=${ObjectSize[$i]}
    # 打印当前参数
    echo "Running s3bench with pars: $i NumClient=$num_client, NumSample=$num_sample, ObjectSize=$object_size"
    $s3bench \
    -accessKey=admin \
    -accessSecret=password\
    -bucket=loadgen \
    -endpoint=http://127.0.0.1:9000 \
    -numClients="$num_client" \
    -numSamples="$num_sample" \
    -objectNamePrefix=loadgen \
    -objectSize="$object_size" \
    -verbose=1 \
    > output_$i.txt # 将输出重定向到.csv文件
    # 等待一段时间，以便下一次执行
    sleep 1s
done