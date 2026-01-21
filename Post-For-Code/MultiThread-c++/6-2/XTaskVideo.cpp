#include "XTaskVideo.h"
#include <sstream>
#include <iostream>

using namespace std;

//ffmpeg - y - i test.mp4 - s 400x300 400.mp4 > log.txt 2 > &1
int XTaskVideo::Run()
{
	stringstream ss;
	ss << "ffmpeg -y -i " << in_path << " -s " << wight << "x" << height << " " << out_path << " > log.txt 2>&1";
	cout << ss.str().c_str() << endl;
	return system(ss.str().c_str());
}