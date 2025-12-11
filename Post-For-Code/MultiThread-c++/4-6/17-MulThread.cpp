#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <execution>

using namespace std;

static const char dir[] = "0123456789abcdef";

void Base16Encode(const unsigned char* data, int size, unsigned char* out)
{
	for (int i = 0; i < size; i++)
	{
		const char p = data[i];
		char a = dir[p >> 4];
		char b = dir[p & 0x0F];
		out[i * 2] = a;
		out[i * 2 + 1] = b;
	}
}

void Base16EncodeThread(const vector<unsigned char>& data, vector<unsigned char>& out)
{
	int th_count = thread::hardware_concurrency();
	int size = data.size() / th_count;
	if (data.size() < th_count)
	{
		th_count = 1;
		size = data.size();
	}

	vector<thread> ths;
	ths.resize(th_count);

	for (int i = 0; i < th_count; i++)
	{
		int offset = size * i;
		int count = size;
		if (th_count > 1 && i == th_count - 1)
		{
			count += data.size() % size;
		}
		ths[i] = thread(Base16Encode, data.data() + offset, count, out.data());
	}

	for (auto& th : ths)
	{
		th.join();
	}
}

int main(int argc, char* argv[])
{
	{
		// single thread
		vector<unsigned char> in_char;
		in_char.resize(1024 * 1024 * 1000);
		vector<unsigned char> out_char;
		out_char.resize(in_char.size() * 2);

		auto time_start = chrono::system_clock::now();
		Base16Encode(in_char.data(), in_char.size(), out_char.data());
		auto time_end = chrono::system_clock::now();
		cout << "single thread speed time : " << chrono::duration_cast<chrono::milliseconds>(time_end - time_start).count() << "ms" << endl;
	}

	{
		// multi thread
		vector<unsigned char> in_char;
		in_char.resize(1024 * 1024 * 1000);
		vector<unsigned char> out_char;
		out_char.resize(in_char.size() * 2);

		auto time_start = chrono::system_clock::now();
		Base16EncodeThread(in_char, out_char);
		auto time_end = chrono::system_clock::now();
		cout << "multi thread speed time : " << chrono::duration_cast<chrono::milliseconds>(time_end - time_start).count() << "ms" << endl;
	}

	{
		vector<unsigned char> in_char;
		in_char.resize(1024 * 1024 * 1000);
		vector<unsigned char> out_char;
		out_char.resize(in_char.size() * 2);

		// C++17
		auto time_start = chrono::system_clock::now();
		std::for_each(std::execution::par, in_char.begin(), in_char.end(),
			[&](auto &d) {
				int idx = &d - in_char.data();
				char a = dir[d >> 4];
				char b = dir[d & 0x0F];
				out_char[idx * 2] = a;
				out_char[idx * 2 + 1] = b;
			}
			);
		auto time_end = chrono::system_clock::now();
		cout << "C++17 multi thread speed time : " << chrono::duration_cast<chrono::milliseconds>(time_end - time_start).count() << "ms" << endl;
	}
	return 0;
}