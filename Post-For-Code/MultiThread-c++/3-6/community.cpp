#include "server.h"
#include <iostream>

using namespace std;
using namespace this_thread;
void xMessage::SendMessage(std::string msg)
{
	unique_lock<mutex> lock(mux_);
	msgs_.push_back(msg);
}

void xMessage::main()
{
	while (!is_exit())
	{
		sleep_for(chrono::milliseconds(10));
		unique_lock<mutex> lock(mux_);
		if (msgs_.empty())
		{
			continue;
		}
		while (!msgs_.empty())
		{
			// 消息处理业务逻辑
			std::cout << "recv : " << msgs_.front() << std::endl;
			msgs_.pop_front();
		}
	}
}