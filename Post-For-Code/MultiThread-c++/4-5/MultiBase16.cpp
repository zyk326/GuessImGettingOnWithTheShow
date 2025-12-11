#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>

using namespace std;
using namespace chrono;

static const char dir[] = "0123456789abcdef";

void Base16Encode(const unsigned char* data, int size, unsigned char* out)
{
	for (int i = 0; i < size; i++)
	{
		unsigned char p = data[i];
		char a = dir[p >> 4];
		char b = dir[p & 0x0F];
		out[i * 2] = a;
		out[i * 2 + 1] = b;
	}
}

void Base16EncodeThread(vector<unsigned char>& data, vector<unsigned char>& out)
{
	int size = data.size();
	int th_count = thread::hardware_concurrency(); // 系统支持的核心数
	// 切片数据
	int slice_count = size / th_count;
	if (size < th_count) // 数据量小于线程数的情况：之切一片
	{
		th_count = 1;
		slice_count = size;
	}

	vector<thread> ths;
	ths.resize(th_count);

	// 任务分配给线程
	for (int i = 0; i < th_count; i++)
	{
		int offset = i * slice_count;
		int count = slice_count;
		
		//最有一个线程
		if (th_count > 1 && i == th_count - 1)
		{
			count = slice_count + size % slice_count;
		}
		cout << "offset : " << offset << " count : " << count << endl; 
		ths[i] = thread(Base16Encode, data.data() + offset, count, out.data());
	}

	for (auto &th : ths)
	{
		th.join();
	}
}

int main(int argc, char argv[])
{
	string str = "你好，我是郑友康";
	unsigned char result[1024] = { 0 };
	Base16Encode((unsigned char*)str.data(), str.size(), result);
	cout << result << endl;


	//单线程效率测试
	{
		vector<unsigned char> in_char;
		in_char.resize(1024 * 1024 * 2000);
		vector<unsigned char> out_char;
		out_char.resize(in_char.size() * 2);
		auto time_start = system_clock::now();
		Base16Encode(in_char.data(), in_char.size(), out_char.data());
		auto time_end = system_clock::now();
		cout << in_char.size() << " - 花费 - " << duration_cast<milliseconds>(time_end - time_start).count() << "ms" << endl;
	}

	//多线程效率测试
	{
		vector<unsigned char> in_char;
		in_char.resize(1024 * 1024 * 2000);
		vector<unsigned char> out_char;
		out_char.resize(in_char.size() * 2);
		auto time_start = system_clock::now();
		Base16EncodeThread(in_char, out_char);
		auto time_end = system_clock::now();
		cout << in_char.size() << " - 多线程花费 - " << duration_cast<milliseconds>(time_end - time_start).count() << "ms" << endl;
	}

	return 0;
}