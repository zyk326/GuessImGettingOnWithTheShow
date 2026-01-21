#include <iostream>
#include <string>
#include <future>
#include <thread>

using namespace std;

string TestTask(int idx)
{
	cout << "begin task pack - " << idx << endl;
	this_thread::sleep_for(chrono::milliseconds(2000));
	return "Test Task had finished!";
}

int main(int argc, char* argv[])
{
	packaged_task<string(int)> task(TestTask);
	auto result = task.get_future();

	//task(100);
	thread th(move(task), 101);

	for (int i = 0; i < 30; i++)
	{
		if (result.wait_for(chrono::milliseconds(100)) != future_status::ready)
		{
			continue;
		}
		// 这里假定有逻辑语句，给了continue的意义
	}
	if (result.wait_for(chrono::milliseconds(100)) == future_status::timeout)
	{
		cout << "timeout!" << endl;
	}
	else
	{
		cout << "task result is : " << result.get() << endl;
	}
	th.join();
	return 0;
}