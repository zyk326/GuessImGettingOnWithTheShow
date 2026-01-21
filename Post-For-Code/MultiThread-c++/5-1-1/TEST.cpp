#include "XThreadPool.h"
#include <iostream>

using namespace std;

class MyTask : public XTask
{
public:
	int Run()
	{
		cout << "MyTask " << name << endl;
		return 0;
	}
	string name = "";
};

int main(int argc, char* argv[])
{
	XThreadPool xt;
	xt.Init(10);
	xt.Start();

	MyTask mt;
	mt.name = "zyk";

	xt.AddTask(&mt);

	getchar();
	return 0;
}