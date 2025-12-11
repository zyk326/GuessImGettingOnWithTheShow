#pragma once
#include <future>
#include <mutex>
#include <list>
#include <thread>
#include <atomic>
class XTask
{
public:
	virtual int Run() = 0;
};

class XThreadPool
{
public:
	void Init(int num);
	void Start();
	void Stop();
	void AddTask(std::shared_ptr<XTask> task);
	std::shared_ptr<XTask> GetTask();
	bool is_exit() { return is_exit_; }
	int GetTasks() { return task_num_count_; }
	~XThreadPool() { Stop(); }

private:
	void Run();
	int thread_num;
	std::mutex mtx_;
	std::vector<std::shared_ptr<std::thread> > threads_;
	std::list<std::shared_ptr<XTask> > tasks_;
	std::condition_variable conv_;
	bool is_exit_ = false;
	std::atomic<int> task_num_count_ = {0};
};

