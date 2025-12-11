#pragma once
#include <thread>

class XThread
{
public:
	virtual void Start();
	virtual void Stop();
	virtual void Wait();
	bool is_exit();

private:
	virtual void Main() = 0;
	bool is_exit_ = false;
	std::thread th_;
};