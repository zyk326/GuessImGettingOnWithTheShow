#include "XThreadPool.h"
#include <iostream>

using namespace std;

class MyTask : public XTask
{
public:
	int Run()
	{
		cout << "MyTask Run! - " << name << endl;
		for (int i = 0; i < 20; i++)
		{
			if (is_exit()) break;
			cout << "." << flush;
			this_thread::sleep_for(chrono::milliseconds(500));
		}
		return 100;
	}
	string name = "";
};

int main(int argc, char* argv[])
{
	XThreadPool xtp;
	xtp.Init(10);
	xtp.Start();

	//MyTask mt;
	//mt.name = "zyk";

	//xtp.AddTask(&mt);

	//MyTask mt1;
	//mt1.name = "ysx";

	//xtp.AddTask(&mt1);

	auto mt3 = make_shared<MyTask>();
	mt3->name = "zyk";
	xtp.AddTask(mt3);

	auto mt4 = make_shared<MyTask>();
	mt4->name = "ysx";
	xtp.AddTask(mt4);
	cout << mt4->GetValue() << endl;

	this_thread::sleep_for(chrono::milliseconds(2000));
	cout << "TASK NUM IS : " << xtp.task_num() << endl;

	xtp.Stop();

	cout << "TASK NUM IS : " << xtp.task_num() << endl;

	getchar();
	return 0;
}