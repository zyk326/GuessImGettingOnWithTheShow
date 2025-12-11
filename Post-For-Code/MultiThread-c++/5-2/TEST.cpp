#include "XThreadPool.h"
#include <iostream>

using namespace std;

class MyTask : public XTask
{
public:
	void Run()
	{
		cout << "MyTask DOING! - " << name << endl;
	}
	string name = "";
};

int main(int argc, int argv[])
{
	XThreadPool xtp;
	xtp.Init(10);
	xtp.Start();

	MyTask mt;
	mt.name = "zyk";
	xtp.AddTask(&mt);

	getchar();
	return 0;
}