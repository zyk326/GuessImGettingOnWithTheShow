#pragma once
#include "XThread.h"
#include <string>
#include <mutex>
#include <list>

class Communication : public XThread
{
public:
	void SendMessage(std::string msg);
private:
	void Main() override;

	std::list<std::string> msgs_;

	std::mutex mtx_;
};

