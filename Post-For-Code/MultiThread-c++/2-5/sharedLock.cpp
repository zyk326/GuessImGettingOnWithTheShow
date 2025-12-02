#include <thread>
#include <iostream>
#include <shared_mutex>
#include <mutex>

using namespace std;

static mutex mut;
static shared_mutex smux;

void ThreadRead(int i)
{
	for (;;)
	{
		smux.lock_shared();
		std::cout << i << " Read" << std::endl;
		this_thread::sleep_for(chrono::milliseconds(1000));
		smux.unlock_shared();
		this_thread::sleep_for(chrono::milliseconds(1));
	}
}

void ThreadWrite(int i)
{
	for (;;)
	{
		smux.lock_shared();
		this_thread::sleep_for(chrono::milliseconds(1000));
		std::cout << i << "Find write logic" << std::endl;
		smux.unlock_shared();
		mut.lock();
		this_thread::sleep_for(chrono::milliseconds(2000));
		std::cout << i << "Do write logic finished" << std::endl;
		mut.unlock();
		this_thread::sleep_for(chrono::milliseconds(1));
	}
}

int main(int argc, char* argv[])
{
	for (int i = 0; i < 3; i++)
	{
		thread th(ThreadRead, i + 1);
		th.detach();
	}
	for (int i = 0; i < 3; i++)
	{
		thread th(ThreadWrite, i + 1);
		th.detach();
	}
	getchar();
	return 0;
}