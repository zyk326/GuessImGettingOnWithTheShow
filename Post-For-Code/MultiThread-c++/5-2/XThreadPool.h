#pragma once
#include <mutex>
#include <thread>
#include <vector>
#include <list>

class XTask
{
public:
	virtual void Run() = 0;
};

class XThreadPool
{
public:
	void Init(int num);
	void Start();
	void AddTask(XTask* task);
	XTask* GetTask();
private:
	void Run();
	int thread_num = 0;
	std::mutex mtx_;
	std::vector<std::thread*> threads_;
	std::list<XTask*> tasks_;
	std::condition_variable conv_;
};

