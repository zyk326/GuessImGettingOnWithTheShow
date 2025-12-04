#include "Message.h"
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	Message message;
	message.Start(); // 这是一个主线程与子线程通信的示例，具体而言，主线程开启十个信息发送，子线程调用Main（回调函数）来打印并出队信息。
	for (int i = 0; i < 10; i++)
	{
		stringstream ss;
		ss << "recv : " << i + 1;
		message.SendMessage(ss.str());
		this_thread::sleep_for(chrono::milliseconds(500));
	}
	message.Stop();
	return 0;
}