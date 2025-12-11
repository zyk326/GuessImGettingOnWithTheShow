#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static mutex mtx;

void Main(int i)
{
	for (;;)
	{
		mtx.lock();
		std::cout << i << " is do" << std::endl;
		this_thread::sleep_for(chrono::milliseconds(100));
		mtx.unlock();
		this_thread::sleep_for(chrono::milliseconds(1));
	}
}

int main(int argc, char* argv[])
{
	{
		static shared_timed_mutex tmux;
	}
	getchar();
	return 0;
}