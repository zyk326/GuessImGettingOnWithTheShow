#pragma once
#include <thread>

class xThread
{
public:
	// 启动线程
	virtual void Start();
	// 停止线程，并等待
	virtual void Stop();
	// 阻塞线程
	virtual void Wait();
	bool is_exit();
private:
	virtual void main() = 0;
	std::thread th_; // 这里需要加入std命名空间
	bool is_exit_ = false;
};