#include "XThread.h"
#include <thread>

using namespace std;

void XThread::Start()
{
	XThread::is_exit_ = false;
	th_ = thread(&XThread::Main, this);
}

void XThread::Stop()
{
	XThread::is_exit_ = true;
	Wait();
}

void XThread::Wait()
{
	if (th_.joinable()) {
		th_.join();
	}
}

bool XThread::is_exit()
{
	return is_exit_;
}