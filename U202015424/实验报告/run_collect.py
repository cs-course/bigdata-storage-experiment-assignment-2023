import subprocess
import itertools

object_sizes = [128, 256, 512, 1024]
num_clients = [1, 5, 10, 100]
num_samples = [100, 200, 400, 800]

parameters = []
for i in object_sizes:
    for j in num_clients:
        for k in num_samples:
            parameters.append([i, j, k])

for params in parameters:
    command = ["python3", "latency_collect.py"] + [str(i) for i in params]
    print(command)
    subprocess.run(command, check=True)
