#include <thread>
#include <iostream>
#include <mutex>

using namespace std;

static mutex mut;

// RAII  resource acquisition is initialization

class Mutex
{
public:
	Mutex(mutex& mut) : mut_(mut)
	{
		mut.lock();
	}
	~Mutex()
	{
		mut.unlock();
	}
private:
	mutex& mut_;  // 必须用引用，得在源锁上操作，而不是副本
};

void Main(int i)
{  
	Mutex mux(mut);  // 把锁的释放
	if (i == 1) 
	{
		std::cout << "i == 1" << std::endl;
		return;
	}
	else if (i == 2)
	{
		std::cout << "i == 1" << std::endl;
		return;
	}
}

int main(int argc, char* argv[])
{
	Main(1);
	Main(2);
	return 0;
}