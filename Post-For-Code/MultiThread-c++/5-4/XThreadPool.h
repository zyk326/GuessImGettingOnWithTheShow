#pragma once
#include <list>
#include <thread>
#include <mutex>
#include <vector>
#include <functional>
#include <atomic>

class XTask
{
public:
	virtual void Run() = 0;

	std::function<bool()> is_exit = nullptr; // º¯ÊýÖ¸Õë
};

class XThreadPool
{
public:
	void Init(int num);

	void Start();

	void AddTask(XTask* task);

	XTask* GetTask();

	void Stop();

	bool is_exit() { return is_exit_; }

	int task_num() { return task_num_; };

private:
	void Run();
	int thread_num = 0;
	std::vector<std::thread*> threads_;
	std::mutex mtx_;
	std::list<XTask*> tasks_;
	std::condition_variable conv_;
	bool is_exit_ = false;
	std::atomic<int> task_num_ = {0};
};

