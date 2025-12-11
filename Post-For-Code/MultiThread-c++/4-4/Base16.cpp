#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <chrono>

using namespace std;
using namespace chrono;

static const char base16[] = "0123456789abcdef";

void Base16Encode(const unsigned char* data, int size, unsigned char* out)
{
	for (int i = 0; i < size; i++)
	{
		unsigned char p = data[i];
		char a = base16[p >> 4];
		char b = base16[p & 0x0F];
		out[i * 2] = a;
		out[i * 2 + 1] = b;
	}
}

int main(int argc, char* argv[])
{
	string str = "你好，我是郑友康";
	unsigned char ret[1024] = { 0 };
	Base16Encode((unsigned char*)str.data(), str.size(), ret);
	cout << ret << endl;

	// 测试单线程编码效率
	{
		vector<unsigned char> in_char;
		in_char.resize(1024 * 1024 * 100);
		//in_char.resize(1024);
		for (int i = 0; i < in_char.size(); i++)
		{
			in_char[i] = i % 256;
		}

		vector<unsigned char> out_char;
		out_char.resize(in_char.size() * 2);
		auto time_start = system_clock::now();
		Base16Encode(in_char.data(), in_char.size(), out_char.data());
		auto time_end = system_clock::now();
		//cout << out_char.data() << endl;
		cout << in_char.size() << " - spend time : " << duration_cast<milliseconds>(time_end - time_start).count() << " ms" << endl;
	}

	return 0;
}