#include "XThreadPool.h"
#include <iostream>

using namespace std;

void XThreadPool::Init(int num) {
	is_exit_ = false;
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
		auto th = make_shared<thread> (thread(&XThreadPool::Run, this));
		threads_.push_back(th);
	}
}
void XThreadPool::Stop()
{
	is_exit_ = true;
	for (auto th : threads_)
	{
		th->join();
	}
	unique_lock<mutex> lock(mtx_);
	threads_.clear();
}
void XThreadPool::AddTask(std::shared_ptr<XTask> task)
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
		try {
			++task_num_count_;
			task->Run();
			--task_num_count_;
			cout << "finished!" << endl;
		}
		catch (...) {

		}
	}
}