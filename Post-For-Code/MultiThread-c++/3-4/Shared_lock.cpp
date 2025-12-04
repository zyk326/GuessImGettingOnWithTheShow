#include <thread>
#include <iostream>
#include <shared_mutex>

using namespace std;

int main(int argc, char* argv[])
{
	{
		static shared_mutex mtx;
		{
			// ¹²ÏíËø
			shared_lock<shared_mutex> lock(mtx);
		}
		{
			// »¥³âËø
			unique_lock<shared_mutex> lock(mtx);
		}
	}
	return 0;
}