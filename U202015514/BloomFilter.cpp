#include <iostream>
#include <bitset>
#include <string>
#include <fstream>
#include <time.h>
using namespace std;

//BKDR¹þÏ£
struct HashBKDR
{
	size_t operator()(const string& s)
	{
		size_t value = 0;
		for (auto e : s)
		{
			value += e;
			value *= 131;
		}

		return value;
	}
};

//AP¹þÏ£
struct HashAP
{
	size_t operator()(const string& s)
	{
		register size_t hash = 0;
		size_t ch;
		for (long i = 0; i < s.size(); i++)
		{
			ch = s[i];
			if ((i & 1) == 0)
			{
				hash ^= ((hash << 7) ^ ch ^ (hash >> 3));
			}
			else
			{
				hash ^= (~(hash << 11) ^ ch ^ (hash >> 5));
			}
		}

		return hash;
	}
};

//DJB¹þÏ£
struct HashDJB
{
	size_t operator()(const string& s)
	{
		register size_t hash = 5381;
		for (auto e : s)
		{
			hash += (hash << 5) + e;
		}

		return hash;
	}
};

template<size_t N, class K = string, class Hash1 = HashBKDR, class Hash2 = HashAP, class Hash3 = HashDJB>
class BloomFilter
{
public:
	void Set(const K& key1, const K& key2)
	{
		size_t i1 = Hash1()(key1) % N;
		size_t i2 = Hash2()(key1) % N;
		size_t i3 = Hash3()(key1) % N;
		size_t i4 = (Hash1()(key2) * i2) % N;
		size_t i5 = (Hash2()(key2) * i3) % N;
		size_t i6 = (Hash3()(key2) * i1) % N;
		/*cout << i1 << " " << i2 << " " << i3 << ';';
		cout << i4 << " " << i5 << " " << i6 << ';' << endl;*/
		bitset1.set(i1);
		bitset1.set(i2);
		bitset1.set(i3);
		bitset2.set(i4);
		bitset2.set(i5);
		bitset2.set(i6);
	}
	bool Tests(const K& key1, const K& key2)
	{
		size_t i1 = Hash1()(key1) % N;
		if (bitset1.test(i1) == 0)
		{
			return false;
		}
		size_t i2 = Hash2()(key1) % N;
		if (bitset1.test(i2) == 0)
		{
			return false;
		}
		size_t i3 = Hash3()(key1) % N;
		if (bitset1.test(i3) == 0)
		{
			return false;
		}
		size_t i4 = (Hash1()(key2)*i2) % N;
		if (bitset2.test(i4) == 0)
		{
			return false;
		}
		size_t i5 = (Hash2()(key2)*i3) % N;
		if (bitset2.test(i5) == 0)
		{
			return false;
		}
		size_t i6 = (Hash3()(key2)*i1) % N;
		if (bitset2.test(i6) == 0)
		{
			return false;
		}
		return true;
	}
private:
	bitset<N> bitset1;
	bitset<N> bitset2;
};

void TestBloom_test()
{
	BloomFilter<50000> bf;
	string str1;
	string str2;
	ifstream infile;
	clock_t start, finish;
	int i = 0;
	int count=0;
	infile.open("test_data.txt");
	start = clock();
	while (str1 != "ZimbabweOpenUniversity")
	{
		infile >> str1 >> str2;

		if (bf.Tests(str1, str2))
		{
			count++;
		}
		bf.Set(str1, str2);
		i++;
	}
	finish = clock();
	double t = (double)(finish - start) / CLOCKS_PER_SEC;
	cout << count << '/' << i<<endl;
	cout << t;
	infile.close();
}
int main()
{
	TestBloom_test();
	return 0;
}