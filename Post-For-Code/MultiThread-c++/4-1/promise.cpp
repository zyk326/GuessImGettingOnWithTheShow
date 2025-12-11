//#include <iostream>
//#include <thread>
//#include <future>
//#include <string>
//
//using namespace std;
//
//void TestFuture(promise<string> p)
//{
//	this_thread::sleep_for(chrono::milliseconds(2000));
//	cout << "begin set value" << endl;
//	p.set_value("TestFuture value");
//	this_thread::sleep_for(chrono::milliseconds(2000));
//	cout << "end TestFuture" << endl;
//}
//
//int main(int argc, char* argv[])
//{
//	// 异步传输变量存储
//	promise<string> p;
//
//	// 用来获取线程异步值
//	auto future = p.get_future();
//
//	auto th = thread(TestFuture, move(p));
//
//	cout << "start get()" << endl;
//	cout << "future get() = " << future.get() << endl;
//	cout << "end get()" << endl;
//
//	th.join();
//
//	getchar();
//	return 0;
//}

#include <iostream>
#include <thread>
#include <string>
#include <future>

using namespace std;

void TestFuture(promise<string> p)
{
	p.set_value("ok");
}

int main(int argc, char* argv[])
{
	promise<string> p;

	auto future = p.get_future();

	auto th = thread(TestFuture, move(p));

	cout << future.get() << endl;

	th.join();

	getchar();
	return 0;
}