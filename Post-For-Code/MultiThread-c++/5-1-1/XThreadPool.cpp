#include "XThreadPool.h"
#include <iostream>

using namespace std;

void XThreadPool::Init(int num) {
	this->thread_num = num;
}

void XThreadPool::Start()
{
	if (thread_num <= 0)
	{
		cout << "NEED INIT" << endl;
	}
	if (!threads_.empty())
	{
		cout << "THREAD LIST NOT EMPTY" << endl;
	}
	for (int i = 0; i < thread_num; i++)
	{
		auto th = new thread(&XThreadPool::Run, this);
		threads_.push_back(th);
	}
}

void XThreadPool::Run()
{
	cout << "START PROCESS RUN" << endl;  
	while (true)
	{
		auto task = GetTask();
		if (!task) continue;
		try {
			task->Run();
		}
		catch(...)
		{
			
		}
	}
	cout << "END PROCESS RUN" << endl;
}

void XThreadPool::AddTask(XTask* task)
{
	unique_lock<mutex> lock(mtx_);
	tasks_.push_back(task);
	lock.unlock();
	conv_.notify_one();
}

XTask* XThreadPool::GetTask()
{
	unique_lock<mutex> lock(mtx_);
	if (tasks_.empty())
	{
		conv_.wait(lock);
	}
	if (tasks_.empty())
	{
		return nullptr;
	}
	auto task = tasks_.front();
	tasks_.pop_front();
	return task;
}