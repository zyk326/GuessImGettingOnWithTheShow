#include "XThreadPool.h"
#include <iostream>

using namespace std;

void XThreadPool::Init(int num)
{
	this->thread_num = num;
	cout << "INIT FINISHED - thread_num is : " << thread_num << endl;
}

void XThreadPool::Start()
{
	if (thread_num <= 0)
	{
		return;
	}
	if (!threads_.empty())
	{
		return;
	}
	for (int i = 0; i < thread_num; i++)
	{
		auto th = new thread(&XThreadPool::Run, this);
		threads_.push_back(th);
	}
}

void XThreadPool::Run()
{
	while (true)
	{
		auto task = GetTask();
		if (!task) continue;
		try
		{
			cout << "TASK GOT! - RUN" << endl;
			task->Run();
		}
		catch (...)
		{

		}
	}
}

void XThreadPool::AddTask(XTask* task)
{
	unique_lock<mutex> lock(mtx_);
	tasks_.push_back(task);
	cout << "TASK ADD FINISHED!" << endl;
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
	cout << "TASK GOT! - GetTask" << endl;
	tasks_.pop_front();
	return task;
}