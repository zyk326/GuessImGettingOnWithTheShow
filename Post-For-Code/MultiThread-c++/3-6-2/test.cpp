#include "Communication.h"
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	Communication ca;
	ca.Start();
	for (int i = 0; i < 10; i++)
	{
		stringstream ss;
		ss << "this is " << i + 1;
		ca.SendMessage(ss.str());
		this_thread::sleep_for(chrono::milliseconds(500));
	}
	ca.Stop();
	return 0;
}