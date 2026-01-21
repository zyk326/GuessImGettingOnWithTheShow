#pragma once
#include "XThreadPool.h"

class XTaskVideo : public XTask
{
public:
	std::string in_path;
	std::string out_path;
	int wight;
	int high;
private:
	int Run();
};

