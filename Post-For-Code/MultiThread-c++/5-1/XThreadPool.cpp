#include "XThreadPool.h"
#include <iostream>

using namespace std;

void XThreadPool::Init(int num)
{
	unique_lock<mutex> lock(mtx_);
	this->thread_num = num;
	cout << "Thread Pool Init " << num << endl;
}

void XThreadPool::Start()
{
	unique_lock<mutex> lock(mtx_);
	if (thread_num <= 0)
	{
		cout << "YOU NEED TO DO INITIALIZATION!" << endl;
		return;
	}
	if (!threads_.empty())
	{
		cout << "THREADS HAVE STARTED RUNNING!" << endl;
	}
	for (int i = 0; i < thread_num; i++)
	{
		auto th = new thread(&XThreadPool::Run, this);
		threads_.push_back(th);
	}
}

void XThreadPool::Run()
{
	cout << "THREAD ID: " << this_thread::get_id() << "START RUNNING!" << endl;
	cout << "THREAD ID: " << this_thread::get_id() << "END RUNNING!" << endl;
}