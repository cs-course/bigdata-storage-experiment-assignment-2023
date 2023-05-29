package main

import (
	"cuckoo/cuckoo"
	"fmt"
	"math/rand"
	"runtime"
	"time"
)

func main() {
	// 初始化参数
	kickOver := 0
	falsePositives := 0
	fn := 0
	numItems := 1000
	testSize := 1000000
	cf, _ := cuckoo.New(128, 8, 16)
	myMap := make(map[string]int)
	// 添加随机数据到Cuckoo Filter
	cf.Info()
	start := time.Now()
	for i := 0; i < numItems; i++ {
		//cf.PrintFilter()

		item := make([]byte, 8)
		rand.Read(item)
		err := cf.Add(item)
		if err != nil {
			fmt.Printf("Insertion failed after %d iterations: %v\n", i+1, err)
			kickOver++
		}
		myMap[string(item)] = 1
		cfret, _ := cf.Contain(item)
		if !cfret && myMap[string(item)] == 1 {
			fn++
		}

	}
	end := time.Now()

	var sum time.Duration
	// 测试假阳率
	for i := 0; i < testSize; i++ {
		item := make([]byte, 8)
		rand.Read(item)
		start := time.Now()
		cfret, _ := cf.Contain(item)
		end := time.Now()
		sum += end.Sub(start)
		if cfret && myMap[string(item)] == 0 {
			falsePositives++
		}
	}
	av_delay := float64(sum) / float64(testSize) / float64(time.Microsecond)

	fmt.Printf("随即写入: %d in %v\n循环超限:%d 循环超限率: %.2f%%\n", numItems, end.Sub(start),
		kickOver, float64(kickOver)/float64(numItems)*100)
	fmt.Printf("误报数量：%d\n", falsePositives)
	fmt.Printf("误报率：%.4f%%\n", float64(falsePositives)/float64(testSize)*100)
	fmt.Printf("平均延迟: %.4fus\n", av_delay)
	//fmt.Printf("假阴性: %d\n", fn)

	// 获取内存使用情况
	var m runtime.MemStats
	runtime.ReadMemStats(&m)

	// 输出内存占用情况
	fmt.Printf("Alloc = %v MiB\n", bToMb(m.Alloc))
	fmt.Printf("TotalAlloc = %v MiB\n", bToMb(m.TotalAlloc))
	fmt.Printf("Sys = %v MiB\n", bToMb(m.Sys))
	fmt.Printf("NumGC = %v\n", m.NumGC)
}

func bToMb(b uint64) uint64 {
	return b / 1024 / 1024
}
