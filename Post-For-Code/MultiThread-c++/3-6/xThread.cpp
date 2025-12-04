#include "xthread.h"
#include <thread>

using namespace std;

void xThread::Start()
{
	is_exit_ = false;
	th_ = thread(&xThread::main, this);
}

void xThread::Stop()
{
	is_exit_ = true;
	Wait();
}

void xThread::Wait()
{
	if (th_.joinable())
	{
		th_.join();
	}
}

bool xThread::is_exit() // 这里需要明确是哪个位置下的函数，加入xThread
{
	return is_exit_;
}