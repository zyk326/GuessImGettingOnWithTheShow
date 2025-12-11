#include "Communication.h"
#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	Communication communication;
	communication.Start();
	for (int i = 0; i < 10; i++)
	{
		stringstream ss;
		ss << "send msg " << i + 1;
		communication.SendMessage(ss.str());
		this_thread::sleep_for(chrono::milliseconds(500));
	}
	communication.Stop();
	cout << "Server stoped!" << endl;
	return 0;
}