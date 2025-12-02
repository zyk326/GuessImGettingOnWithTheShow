#include <thread>
#include <iostream>

using namespace std;

class TestThread
{
public:
	void Start()
	{
		th_ = thread([this]() {std::cout << name << std::endl; }); // []用来捕获外部变量
	}
	string name;
private:
	thread th_;
};

int main(int argc, char* argv[])
{
	thread th;
	th = thread([](int i) {std::cout << i << std::endl; }, 123);
	th.join();

	TestThread testth;
	testth.name = "testth";
	testth.Start();
	return 0;
}