#include "XThreadPool.h"
#include "XTaskVideo.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
	XThreadPool xtp;
	xtp.Init(10);
	xtp.Start();
	for (;;)
	{
		this_thread::sleep_for(chrono::milliseconds(200));
		auto xtv = make_shared<XTaskVideo>();
		cout << "==========================================" << endl;
		cout << "ENTER COMMAND(v e l)" << endl;
		string cmd;
		cin >> cmd;
		if (cmd == "e") {
			break;
		}
		else if (cmd == "l") {
			cout << xtv->GetValue();
			continue;
		}
		cout << "INPUT IN_PATH:";
		cin >> xtv->in_path;
		cout << "INPUT OUT_PATH:";
		cin >> xtv->out_path;
		cout << "INPUT WIGHT:";
		cin >> xtv->wight;
		cout << "INPUT HIGH:";
		cin >> xtv->high;
		xtp.AddTask(xtv);
	}

	return 0;
}