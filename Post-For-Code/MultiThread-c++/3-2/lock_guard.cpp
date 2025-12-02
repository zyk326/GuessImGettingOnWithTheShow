#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static mutex gmux;

void Main(int i)
{
	gmux.lock();
	{
		lock_guard<mutex> lock(gmux, adopt_lock);
	}
	{
		lock_guard<mutex> lock(gmux);
		std::cout << i << " begin Main" << std::endl;
	}
	for (;;)
	{
		{
			lock_guard<mutex> lock(gmux);
			std::cout << i << " do thread" << std::endl;
		}
		this_thread::sleep_for(chrono::milliseconds(500));
	}

}

int main(int argc, char* argv[])
{
	for (int i = 0; i < 3; i++)
	{
		thread th(Main, i + 1);
		th.detach();
	}
	getchar();
	return 0;
}