#include "server.h"
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	xMessage xm;
	xm.Start();
	for (int i = 0; i < 10; i++)
	{
		stringstream ss;
		ss << "msg : " << i + 1;
		xm.SendMessage(ss.str());
		this_thread::sleep_for(chrono::milliseconds(500));
	}
	xm.Stop();
	return 0;
}