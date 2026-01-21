#include <vector>
#include <numeric>
#include <thread>
#include <iostream>

template<typename Iterator, typename T>
struct accumulate_block {
	void operator()(Iterator start, Iterator end, T& init) {
		init = std::accumulate(start, end, init);
	}
};

template<typename Iterator, typename T>
int parallel_accumulate(Iterator begin, Iterator end, T init)
{
	unsigned long const sum_elements = std::distance(begin, end);
	unsigned long const min_block = 25;
	unsigned long const minb_threads = (sum_elements + min_block - 1) / min_block;
	unsigned long const hardware_threads = std::thread::hardware_concurrency();
	unsigned long const num_threads = std::min(minb_threads, hardware_threads == 0 ? 2 : hardware_threads);
	std::vector<T> result(num_threads);
	unsigned long const real_num_block = sum_elements / num_threads;

	std::vector<std::thread> threads(num_threads - 1);

	Iterator start_it = begin;
	for (unsigned long i = 0; i < (num_threads - 1); ++i)
	{
		Iterator end_it = start_it;
		std::advance(end_it, real_num_block);
		threads[i] = std::thread(accumulate_block<Iterator, T>(), start_it, end_it, std::ref(result[i]));
		start_it = end_it;
	}

	accumulate_block<Iterator, T>()(start_it, end, result[num_threads - 1]);

	for (auto& th : threads) {
		th.join();
	}
	return std::accumulate(result.begin(), result.end(), init);
}

int main() {
	std::vector<int> numbers(1000, 1);

	int result = parallel_accumulate(numbers.begin(), numbers.end(), 0);

	std::cout << result << std::endl;
	return 0;
}
