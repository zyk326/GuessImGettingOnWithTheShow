#include <thread>
#include <iostream>

using namespace std;

class MyThread
{
public:
	virtual void Start()
	{
		is_exit_ = true;
		th_ = thread(&MyThread::Main, this);
	}
	virtual void Stop()
	{
		is_exit_ = false;
		Wait();
	}
	virtual void Wait()
	{
		if (th_.joinable())
		{
			th_.join();
		}
	}
	bool is_exit() { return is_exit_; }
private:
	virtual void Main() = 0;
	thread th_;
	bool is_exit_ = false;
};

class TestThread : public MyThread
{
public:
	void Main()
	{
		std::cout << "in Main" << std::endl;
		while (is_exit())
		{
			std::cout << "." << flush;
			this_thread::sleep_for(chrono::milliseconds(50));
		}
		std::cout << std::endl << "out Main" << std::endl;
	}
};

int main(int argc, char* argv[])
{
	TestThread testth;
	testth.Start();
	this_thread::sleep_for(chrono::seconds(5));
	testth.Stop();
	getchar();
	return 0;
}