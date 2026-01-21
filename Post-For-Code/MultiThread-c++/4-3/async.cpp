// 创建异步线程，可以异步获取结果 
#include <future>
#include <iostream>
#include <string>

using namespace std;

string TestAsync(int index)
{
	cout << index << " - TestAsync - " << this_thread::get_id() << endl;
	this_thread::sleep_for(chrono::milliseconds(2000));
	return "return TestAsync string";
}

int main(int argc, char* argv[])
{
	cout << "  - Main - " << this_thread::get_id() << endl;
	// 这种启动异步不创建线程
	auto future = async(launch::deferred, TestAsync, 1);
	this_thread::sleep_for(chrono::milliseconds(100));
	cout << "before get future" << endl;
	cout << future.get() << endl;
	cout << "finish get future" << endl;
	
	// 这种启动异步创建线程
	auto future2 = async(TestAsync, 2);
	this_thread::sleep_for(chrono::milliseconds(100));
	cout << "before get future" << endl;
	cout << future2.get() << endl;
	cout << "finish get future" << endl;
	return 0;
}