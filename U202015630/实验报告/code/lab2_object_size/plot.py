import matplotlib.pyplot as plt

object_sizes = []
write_throughputs = []
read_throughputs = []
write_average_latency=[]
read_average_latency=[]




if __name__=="__main__":
    with open("./result.out", 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            object_sizes.append(float(lines[i].split()[-2]))
            write_throughputs.append(float(lines[i + 2].split()[-2]))
            write_average_latency.append(float(lines[i + 3].split()[-2]))
            read_throughputs.append(float(lines[i + 6].split()[-2]))
            read_average_latency.append(float(lines[i + 7].split()[-2]))
            i += 8

    # plt.plot(object_sizes, write_throughputs,marker='o', label="write throughputs")
    # plt.plot(object_sizes, read_throughputs, marker='x',label="read throughputs")
    # plt.legend()
    #
    # plt.xlabel('object sizes / KB')
    # plt.ylabel('total throughputs / KB/s')
    # plt.title('Object Size vs Write Total Throughput and Read Total Throughput')
    # plt.savefig('./object_sizes---throughputs.png')

    plt.plot(object_sizes, write_average_latency,marker='o', label="write average latency")
    plt.plot(object_sizes, read_average_latency, marker='x',label="read average latency")
    plt.legend()

    plt.xlabel('object sizes / KB')
    plt.ylabel('average latency / s')
    plt.title('Object Size vs Average Latency')
    plt.savefig('./object_sizes---average_latency.png')