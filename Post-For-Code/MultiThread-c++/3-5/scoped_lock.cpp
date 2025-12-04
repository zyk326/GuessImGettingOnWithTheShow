#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static mutex mtx1;
static mutex mtx2;

void Main1()
{
	this_thread::sleep_for(chrono::milliseconds(100));
	std::cout << "Main 1 prepare for mtx1 lock" << std::endl;
	//mtx1.lock();
	std::cout << "Main 1 prepare for mtx2 lock" << std::endl;
	//mtx2.lock();
	scoped_lock(mtx1, mtx2); // 这个的意思是说，mtx1和mtx2同时锁住，离开作用区释放锁
	std::cout << "It is Main1" << std::endl;
	this_thread::sleep_for(chrono::milliseconds(1000));
	//mtx1.unlock();
	//mtx2.unlock();
}

void Main2()
{
	std::cout << "Main 2 prepare for mtx2 lock" << std::endl;
	mtx2.lock();
	this_thread::sleep_for(chrono::milliseconds(500));
	std::cout << "Main 2 prepare for mtx1 lock" << std::endl;
	mtx1.lock();
	std::cout << "It is Main2" << std::endl;
	this_thread::sleep_for(chrono::milliseconds(1500));
	mtx2.unlock();
	mtx1.unlock();
}

int main(int argc, char* argv[])
{
	{
		thread th1(Main1);
		th1.detach();
	}
	{
		thread th2(Main2);
		th2.detach();
	}
	getchar();
	return 0;
}