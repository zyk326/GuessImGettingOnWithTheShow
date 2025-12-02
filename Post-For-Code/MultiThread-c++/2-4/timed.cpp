#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static timed_mutex tmux; //  Ù”⁄mutexø‚

//void Main(int i)
//{
//	for (;;)
//	{
//		if (!tmux.try_lock_for(chrono::milliseconds(500)))
//		{
//			std::cout << "try " << i <<" lock [TIME OUT]" << endl;
//			continue;
//		}
//		std::cout << i << "[in]" << endl;
//		this_thread::sleep_for(chrono::milliseconds(100));
//		this_thread::sleep_for(chrono::milliseconds(2000));
//		tmux.unlock();
//		this_thread::sleep_for(chrono::milliseconds(1));
//	}
//}

//int main(int argc, char* argv)
//{
//	for (int i = 0; i < 3; i++)
//	{
//		thread th(Main, i + 1);
//		th.detach();
//	}
//	getchar();
//	return 0;
//}