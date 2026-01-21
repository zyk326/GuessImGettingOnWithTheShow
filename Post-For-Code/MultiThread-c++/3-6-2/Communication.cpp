#include "Communication.h"
#include <iostream>

using namespace std;

void Communication::SendMessage(string msg)
{
	unique_lock<mutex> lock(mtx_);
	msgs_.push_back(msg);
}

void Communication::Main()
{
	while (!is_exit()) 
	{
		unique_lock<mutex> lock(mtx_);
		if (msgs_.empty()) 
		{
			continue;
		}
		while (!msgs_.empty())
		{
			std::cout << "recv : " << msgs_.front() << std::endl;  // 这里的recv是receive的意思
			msgs_.pop_front();
		}
	}
}