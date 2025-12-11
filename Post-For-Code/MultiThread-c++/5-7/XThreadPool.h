#pragma once
#include <future>
#include <vector>
#include <thread>
#include <list>
#include <atomic>
#include <functional>


class XTask
{
public:
	virtual int Run() = 0;
	std::function<bool()> is_exit = nullptr;
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
	void Stop();
	void AddTask(std::shared_ptr<XTask> task); // 智能指针需要导入future
	std::shared_ptr<XTask> GetTask();
	bool is_exit() { return is_exit_; }
	int Task_num_count() { return task_num_count_; }
	~XThreadPool() { Stop(); }
private:
	void Run();
	std::vector<std::shared_ptr<std::thread> > threads_;
	int thread_num = 0;
	std::mutex mtx_;
	std::list<std::shared_ptr<XTask>> tasks_;
	std::condition_variable conv_;
	bool is_exit_ = false;
	std::atomic<int> task_num_count_ = {0};
};

