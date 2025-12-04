#pragma once
#include "XThread.h"
#include <string>
#include <list>
#include <mutex>

class Message : public XThread
{
public:
	void SendMessage(std::string msg);

private:
	void Main() override;

	std::list<std::string> msgs_;

	std::mutex mtx_;
};