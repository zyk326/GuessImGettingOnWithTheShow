#include "XThreadPool.h"
#include <iostream>

using namespace std;

class MyTask : public XTask
{
public:
	void Run()
	{
		cout << "MyTask Run! - " << name << endl;
		for (int i = 0; i < 10; i++)
		{
			if (is_exit()) break;
			cout << "." << flush;
			this_thread::sleep_for(chrono::milliseconds(500));
		}
	}
	string name = "";
};

int main(int argc, char* argv[])
{
	XThreadPool xtp;
	xtp.Init(10);
	xtp.Start();

	MyTask mt;
	mt.name = "zyk";

	xtp.AddTask(&mt);

	this_thread::sleep_for(chrono::milliseconds(1000));
	xtp.Stop();
	getchar();
	return 0;
}