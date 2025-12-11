#include "XThreadPool.h"

using namespace std;

int main(int argc, char* argv[])
{
	XThreadPool xt;
	xt.Init(14);
	xt.Start();
	getchar();
	return 0;
}