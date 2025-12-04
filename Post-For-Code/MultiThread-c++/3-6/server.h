#pragma once
#include "xthread.h"
#include <string>
#include <mutex>
#include <list>
class xMessage : public xThread
{
public:
	void SendMessage(std::string);
private:
	void main() override;

	// 消息缓冲队列
	std::list<std::string> msgs_;

	// 互斥访问消息队列
	std::mutex mux_;
};