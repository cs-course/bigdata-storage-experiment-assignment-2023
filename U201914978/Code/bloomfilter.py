import hashlib
import data


class BloomFilter:
    def __init__(self, filter_size, seed_list):
        self.filter_size = filter_size
        self.seed_list = seed_list
        self.bits = [0] * filter_size

    def storage(self, data):
        """
        将data通过hash存入bits
        :param data: 传入的属性值
        :return: 无
        """
        for i in range(len(self.seed_list)):
            hash_i = hashlib.sha256(self.seed_list[i].encode('utf8'))
            hash_i.update(data.encode('utf8'))
            idx = int(hash_i.hexdigest(), 16)
            idx = idx % self.filter_size
            self.bits[idx] = 1

    def contain(self, data):
        """
        判断data是否在bits中
        :param data: 传入的单属性值
        :return: 是，则true
        """
        for i in range(len(self.seed_list)):
            hash_j = hashlib.sha256(self.seed_list[i].encode('utf8'))
            hash_j.update(data.encode('utf8'))
            idx = int(hash_j.hexdigest(), 16)
            idx = idx % self.filter_size
            if self.bits[idx] == 0:
                return False
        return True


if __name__ == '__main__':
    # 本实验假设元素的属性值有3个
    filter_size = 10000000
    hash_num = 3
    data_length = 3
    data_size = 500000

    ds = data.DataSetter(data_length, data_size, hash_num)
    bf1 = BloomFilter(filter_size, ds.seed_list)
    bf2 = BloomFilter(filter_size, ds.seed_list)
    bf3 = BloomFilter(filter_size, ds.seed_list)

    cnt = 0
    for data in ds.data_list:   # 三个属性值通过三个bf存储进不同bits
        if bf1.contain(data[0]) and bf2.contain(data[1]) and bf3.contain(data[2]):
            cnt = cnt + 1
        bf1.storage(data[0])
        bf2.storage(data[1])
        bf3.storage(data[2])

    print(cnt)
    print(data_size)
