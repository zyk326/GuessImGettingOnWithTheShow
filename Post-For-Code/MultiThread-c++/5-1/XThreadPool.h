#pragma once
#include <thread>
#include <mutex>
#include <vector>

class XThreadPool
{
public:
	void Init(int num);
	
	void Start();
private:
	void Run();
	int thread_num = 0;
	std::mutex mtx_;
	std::vector<std::thread*> threads_;
};

