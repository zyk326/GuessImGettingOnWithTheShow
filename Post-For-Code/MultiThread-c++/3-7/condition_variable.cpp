#include <iostream>
#include <thread>
#include <mutex>
#include <list>
#include <string>
#include <sstream>

using namespace std;

list<string> msgs_;
mutex mtx;
condition_variable cv;

void ThreadRead(int num)
{
	for (;;)
	{
		cout << "read msg" << endl;
		unique_lock<mutex> lock(mtx);
		cv.wait(lock); // 解锁，阻塞，等待信号
		// 获取信号后锁定
		while (!msgs_.empty())
		{
			cout << num << " read " << msgs_.front() << endl;
			msgs_.pop_front();
		}
	}
}

void ThreadWrite()
{
	for (int i = 0;; i++)
	{
		stringstream ss;
		ss << "write msg " << i;
		unique_lock<mutex> lock(mtx);
		msgs_.push_back(ss.str());
		lock.unlock();		// 先解锁
		//cv.notify_one();	// 然后通知一个，发送信号
		cv.notify_all();
		this_thread::sleep_for(chrono::milliseconds(1000));
	}
}

int main(int argc, char* argv[])
{
	thread thW(ThreadWrite);
	thW.detach();
	for (int i = 0; i < 3; i++)
	{
		thread thR(ThreadRead, i + 1);
		thR.detach();
	}
	getchar();
	return 0;
}