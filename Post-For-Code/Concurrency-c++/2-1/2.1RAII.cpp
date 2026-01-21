#include <iostream>
#include <thread>

struct func {
	int& state;
	func(int& s_) : state(s_){}
	void operator()() {
		for (int i = 0; i < 1000; ++i)
		{
			++state;
			std::cout << "In the thread: state = " << state << std::endl;
		}
	}
};

class thread_guard {
	std::thread& t;
public:
	thread_guard(std::thread& t_) : t(t_){}
	~thread_guard()
	{
		if (t.joinable())
		{
			t.join();
		}
	}
};

void do_some_thread_task()
{
	std::cout << "do some thread task" << std::endl;
}

int main()
{
	int some_local_state = 0;
	{
		func my_func(some_local_state);
		std::thread t(my_func);
		thread_guard g(t);

		do_some_thread_task();
	}
	std::cout << "In the Main thread: state = " << some_local_state << std::endl;
	return 0;
}