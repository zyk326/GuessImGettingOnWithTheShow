#pragma once
#include <thread>

class XThread
{
public:
	virtual void Start();
	virtual void Stop();
	virtual void Wait();
	bool is_exit();
protected:
	bool is_exit_ = false;  // 表示线程尚未退出
private:
	std::thread th_;
	virtual void Main() = 0;
};

