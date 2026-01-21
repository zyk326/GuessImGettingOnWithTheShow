#include <iostream>
#include <thread>
#include <future>
#include <map>

using payload_type = std::string;

class connection {
public:
	std::map<int, std::promise<payload_type>> promises;

	std::future<payload_type> get_future(int id) {
		std::promise<payload_type> promise;
		std::future<payload_type> future = promise.get_future();
		promises[id] = std::move(promise);
		return future;
	}

	void send(const payload_type& data, int id) {
		std::cout << "simulate sending signal : " << data << " id is : " << id << std::endl;
		if (promises.count(id) > 0) {
			promises[id].set_value(data);
		}
		else {
			std::cerr << "no promise found for id : " << id << std::endl;
		}
	}
};


//int main()
//{
//	connection cnn;
//	std::future<payload_type> future1 = cnn.get_future(1);
//	std::future<payload_type> future2 = cnn.get_future(2);
//	std::thread sender1([&cnn]() {cnn.send("Hello ", 1); });
//	std::thread sender2([&cnn]() {cnn.send("World", 2); });
//	sender1.join();
//	sender2.join();
//	std::cout << "get data1: " << future1.get() << std::endl;
//	cnn.promises.erase(cnn.promises.find(1));
//	std::cout << "get data2: " << future2.get() << std::endl;
//	cnn.promises.erase(cnn.promises.find(2));
//}

void task(std::promise<void> promise) {
	try {
		throw std::exception("foo");
	}
	catch (const std::exception& e) {
		promise.set_exception(std::current_exception());
		// 这里是把正在传播的异常封装成std::exception_ptr，存进shared state
		// 这个e会出作用域就销毁，无法跨域安全携带给外部；
	}
}

//int main() {
//	std::promise<void> promise;
//	std::future<void> future = promise.get_future();
//	std::thread th(task, std::move(promise));
//	th.join();
//	try {
//		future.get();
//	}
//	catch (const std::exception& e) {
//		std::cout << "catch err: " << e.what() << std::endl;
//	}
//	return 0;
//}

//#include <condition_variable>
//#include <mutex>
//#include <chrono>
//
//std::condition_variable cv;
//bool done;
//std::mutex m;
//
//bool wait_loop() {
//	auto const timeout = std::chrono::steady_clock::now() + std::chrono::milliseconds(500);
//	std::unique_lock<std::mutex> lk(m);
//	while(!done){
//		if (cv.wait_until(lk, timeout) == std::cv_status::timeout) {
//			break;
//		}
//	}
//	return done;
//}

#include <condition_variable>
#include <mutex>
#include <chrono>
#include <iostream>

std::condition_variable cv;
std::mutex m;
bool done = false;

bool wait_loop() {
	auto const timeout = std::chrono::steady_clock::now() + std::chrono::milliseconds(1500);
	std::unique_lock<std::mutex> lk(m);
	while (!done) {
		puts("while......");
		if (cv.wait_until(lk, timeout) == std::cv_status::timeout) {
			break;
		}
	}
	if (done) {
		std::cout << "\nt0:get the message of appending variable value!" << std::endl;
	}
	else {
		std::cout << "\nt0:timeout exit!" << std::endl;
	}
	return done;
}

int main() {
	std::thread t0(wait_loop);
	//wait_loop();
	std::cout << "-------------" << std::endl;
	std::thread t1([&]() {
		std::cout << "\nt1:Setting done to true in another thread" << std::endl;
		done = true;
		cv.notify_one();
		});
	t0.join();
	t1.join();
	return 0;
}