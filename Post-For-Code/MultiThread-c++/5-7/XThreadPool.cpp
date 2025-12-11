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
		auto th = make_shared<thread>(thread(&XThreadPool::Run, this)) ;
		threads_.push_back(th);
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
}

void XThreadPool::AddTask(std::shared_ptr<XTask> task) // 智能指针需要导入future
{
	unique_lock<mutex> lock(mtx_);
	tasks_.push_back(task);
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
		++task_num_count_;
		try {
			cout << "TASK START! - " << this_thread::get_id() << endl;
			int re = task->Run();
			task->SetValue(re);
			cout << "TASK FINISHED! - " << this_thread::get_id() << endl;
		}catch(...){

		}
		--task_num_count_;
	}
}