#include <Thread>
#include <iostream>

using namespace std;

void ThreadMain()
{
	std::cout << "sub thread start!" << std::endl;
	for (int i = 0; i < 10; i++)
	{
		std::cout << "now times is:" << i << endl;
		this_thread::sleep_for(chrono::seconds(1));
	}
}

int main(int argc, char* argv[])
{
	std::cout << "main thread start" << endl;

	std::thread th(ThreadMain);

	std::cout << "wait sub thread release" << endl;
	th.join();
	std::cout << "finish sub thread release" << endl;
	return 0;
}