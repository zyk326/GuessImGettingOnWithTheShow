#include "Communication.h"
#include <string>
#include <iostream>

using namespace std;

void Communication::Stop()
{
	is_exit_ = true;
	cv_.notify_all();
	Wait();
}

void Communication::SendMessage(string msg)
{
	unique_lock<mutex> lock(mtx_);
	msgs_.push_back(msg);
	lock.unlock();
	cv_.notify_one();
}

void Communication::Main()
{
	while (!is_exit())
	{
		unique_lock<mutex> lock(mtx_);
		cv_.wait(lock, [this] 
		{
			cout << "cv in wait" << endl;
			if (is_exit()) return true;
			return !msgs_.empty(); 
		});
		while (!msgs_.empty())
		{
			cout << "recv : " << msgs_.front() << endl;
			msgs_.pop_front();
		}
	}
}