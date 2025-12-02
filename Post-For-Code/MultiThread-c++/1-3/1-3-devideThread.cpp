#include <thread>
#include <iostream>

using namespace std;

bool is_thread = true;

void ThreadMain()
{

	for (int i = 0; i < 10; i++) 
	{
		if (!is_thread) break;
		this_thread::sleep_for(chrono::seconds(1));
		std::cout << "now i is:" << i << endl;
	}
}

int main(int argc, char* argv[])
{
	{
		std::thread th(ThreadMain);
		std::cout << "main thread is going!" << std::endl;
		std::cout << "need to over subthread after 5s!" << std::endl;
		this_thread::sleep_for(chrono::seconds(5));
		is_thread = false;
		th.join(); // 将子线程加入主线程生命周期
	}
	std::cout << "main thread still going!" << std::endl;
	return 0;
}