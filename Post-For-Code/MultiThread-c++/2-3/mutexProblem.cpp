#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static mutex mut;

void Main(int i)
{
	for (;;)
	{
		mut.lock();
		std::cout << i << "[in]" << std::endl;
		this_thread::sleep_for(chrono::milliseconds(1000));
		mut.unlock();
		this_thread::sleep_for(chrono::milliseconds(1)); // 在unlock之后立刻接lock会导致操作系统难以判断unlock，导致同一线程多次lock状态
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