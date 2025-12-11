#pragma once
#include "XThreadPool.h"
class XTaskVideo :public XTask
{
public:
	int Run();
	std::string in_path;
	std::string out_path;
	int wight;
	int height;
};

