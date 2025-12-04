#include "Message.h"
#include <string>
#include <iostream>

using namespace std;
using namespace this_thread;

void Message::SendMessage(string msg)
{
	unique_lock<mutex> lock(mtx_);
	msgs_.push_back(msg); // 写入队列的时候上锁
}


void Message::Main()
{
	while (!is_exit())
	{
		sleep_for(chrono::milliseconds(10));
		unique_lock<mutex> lock(mtx_); // 析构时自动解锁
		if (msgs_.empty()) 
		{
			continue;
		}
		while (!msgs_.empty())
		{
			std::cout << "recv : " << msgs_.front() << std::endl;
			msgs_.pop_front();
		}
	}
}