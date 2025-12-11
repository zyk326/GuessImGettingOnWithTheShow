#include "XThreadPool.h"
#include <iostream>

using namespace std;

void XThreadPool::Init(int num)
{
	this->thread_num = num;
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
		//auto th = new thread(&XThreadPool::Run, this);
		auto th = make_shared<thread> (&XThreadPool::Run, this);
		threads_.push_back(th);
	}
}

void XThreadPool::AddTask(std::shared_ptr<XTask> task)
{
	unique_lock<mutex> lock(mtx_);
	tasks_.push_back(task);
	task->is_exit = [this] {return is_exit(); };
	lock.unlock();
	conv_.notify_one();
}

std::shared_ptr<XTask> XThreadPool::GetTask()
{
	unique_lock<mutex> lock(mtx_);
	if (tasks_.empty())
	{
		conv_.wait(lock);
	}
	if (is_exit())
	{
		return nullptr;
	}
	if (tasks_.empty())
	{
		return nullptr;
	}
	auto task = tasks_.front();
	tasks_.pop_front();
	return task;
}


void XThreadPool::Run()
{
	while (!is_exit())
	{
		auto task = GetTask();
		if (!task)
		{
			continue;
		}
		++task_num_;
		task->Run();
		--task_num_;
	}
}

void XThreadPool::Stop()
{
	is_exit_ = true;
	conv_.notify_all();
	for (auto th : threads_)
	{
		th->join();
	}
	unique_lock<mutex> lock(mtx_);
	threads_.clear();
	std::cout << "Stoped!" << endl;
}