#pragma once
#include "XThread.h"
#include <string>
#include <list>
#include <mutex>

class Communication : public XThread
{
public:
	void SendMessage(std::string msg);
	void Stop() override;

private:
	void Main() override;
	std::list<std::string> msgs_;
	std::mutex mtx_;
	std::condition_variable cv_;
};

