std::experimental::future<FinalResult> process_data(std::vector<MyData>& vec) {
	size_t const chunk_size = /*some correct value*/ ;
	std::vector<std::experimental::future<ChunkResult>> results;
	for (auto begin = vec.begin(), end = vec.end; begin != end;) {
		size_t const remaining_size = end - begin;
		size_t const this_chunk_size = std::min(remaining_size, chunk_size);
		results.push_bask(spawn_async(process_chunk, begin, begin + this_chunk_size));
		begin += this_chunk_size;
	}
	return std::experimental::when_all(
		results.begin(), results.end()).then(  // 只有集合的所有内容都准备完成后，才会执行then
			[](std::future<std::vector<std::experimental::future<ChunkResult>> > ready_results) {
				std::vector<std::experimental::future<ChunkResult>> all_results = ready_results.get();
				std::vector<ChunkResult> v;
				v.reserve(all_results.size()); // 这里reserve之后，不会再重新分配内存，不会产生ChunkResult对象的移动
				for (auto& f : all_results) { v.push_back(f.get()); }
				return gather_results(v);
			}
	);
}