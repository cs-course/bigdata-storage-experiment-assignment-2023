import random


class DataSetter:
    def __init__(self, data_length, data_size, seed_size):
        self.data_length = data_length
        self.datasize = data_size
        self.seed_size = seed_size
        self.data_list = []
        self.seed_list = []
        for i in range(data_size):
            x = random.uniform(0, 99999)
            y = random.uniform(0, 99999)
            z = random.uniform(0, 99999)

            listadd = [str(x), str(y), str(z)]
            self.data_list.append(listadd)

        for i in range(seed_size):
            n = random.randint(0, 4096)
            self.seed_list.append(str(n))
