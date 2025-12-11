#pragma once
#include <list>
#include <thread>
#include <mutex>
#include <vector>
#include <functional>
#include <atomic>
#include <future>

class XTask
{
public:
	virtual int Run() = 0;

	std::function<bool()> is_exit = nullptr; // 函数指针

	auto GetValue()
	{
		return p_.get_future().get();
	}

	void SetValue(int v)
	{
		p_.set_value(v);
	}
private:
	std::promise<int> p_;
};

class XThreadPool
{
public:
	void Init(int num);

	void Start();

	//void AddTask(XTask* task);
	void AddTask(std::shared_ptr<XTask> task);

	//XTask* GetTask();
	std::shared_ptr<XTask> GetTask();

	void Stop();

	bool is_exit() { return is_exit_; }

	int task_num() { return task_num_; };

private:
	void Run();
	int thread_num = 0;
	//std::vector<std::thread*> threads_; 
	std::vector<std::shared_ptr<std::thread> > threads_; // 线程智能指针版本
	std::mutex mtx_;
	//std::list<XTask*> tasks_;
	std::list<std::shared_ptr<XTask>> tasks_; // 存放智能指针版本
	std::condition_variable conv_;
	bool is_exit_ = false;
	std::atomic<int> task_num_ = {0};
};

