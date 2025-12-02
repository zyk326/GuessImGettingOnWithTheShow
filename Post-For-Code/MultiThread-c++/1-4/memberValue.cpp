#include <thread>
#include <iostream>

using namespace std;

class CL {
public:
	CL() { std::cout << "Create CL;" << std::endl; }
	CL(const CL& C) { std::cout << "Copy CL;" << std::endl; } // 构造函数拷贝要加const
	~CL() { std::cout << "Del CL;" << std::endl; }
	string name;
};

void ThreadMain(int a, float b, string c, CL d)
{
	this_thread::sleep_for(chrono::seconds(1));
	std::cout << "thread had in." << std::endl;
	std::cout << a << b << c << d.name << std::endl;
}

int main(int argc, char* argv[])
{
	thread th;
	{
		float a = 13.2f;
		CL c;
		c.name = "Cname";
		th = thread(ThreadMain, 1, a, "this is a string;", c);
	}
	th.join();
	return 0;
}