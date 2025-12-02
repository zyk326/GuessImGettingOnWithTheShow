#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static mutex mut;


void Main()
{
	//else
	for (;;)
	{
		if (!mut.try_lock())
		{
			std::cout << "." << flush;
			this_thread::sleep_for(chrono::milliseconds(100));
			continue;
		}
		std::cout << "============================" << std::endl;
		std::cout << "yes" << std::endl;
		std::cout << "============================" << std::endl;
		mut.unlock();
		this_thread::sleep_for(chrono::milliseconds(2000));
	}
}

int main(int argc, char* argv[])
{
	for (int i = 0; i < 10; i++)
	{
		thread th(Main);
		th.detach();
	}
	getchar();
	return 0;
}

