#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

static mutex mut;

void Main(int i)
{
	
		unique_lock<mutex> lock(mut);
		std::cout << i << " have been locked" << endl;
		mut.unlock();
		std::cout << i << " have been unlocked now" << endl; // 可以被临时解锁
		mut.lock();
		std::cout << i << " have been locked again" << endl;
	
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