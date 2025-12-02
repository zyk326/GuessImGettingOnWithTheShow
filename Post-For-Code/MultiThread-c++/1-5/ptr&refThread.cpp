#include <thread>
#include <iostream>

using namespace std;

class PD {
public:
	PD() {};
	~PD() {};
	string name;
};

void ThreadMainRef(PD& pd)
{
	std::cout << "in threadmainPtr." << pd.name << std::endl;
}

void ThreadMainPtr(PD* pd) 
{
	std::cout << "in threadmainPtr." << pd->name << std::endl;
}

int main(int argc, char* argv[])
{
	{
		PD pd;
		pd.name = "PD name!";
		thread th;
		th = thread(ThreadMainPtr, &pd);
		th.join();
		pd.name = "PD Ptr name!";
		th = thread(ThreadMainRef, ref(pd));
		th.join();
	}

	return 0;
}