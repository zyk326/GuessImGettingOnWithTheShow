#include "XTaskVideo.h"
#include <iostream>
#include <sstream>

using namespace std;

int XTaskVideo::Run()
{
	//ffmpeg - y - i test.mp4 - s 400x300 400.mp4 > log.txt 2 > &1
	stringstream ss;
	ss << "ffmpeg -y -i " << in_path << " ";
	if (wight > 0 && high > 0)
	{
		ss << "-s " << wight << "x" << high << " ";
	}
	ss << out_path << " ";
	ss << " >" << this_thread::get_id() << ".txt 2>&1";
	cout << ss.str().c_str() << endl;
	return system(ss.str().c_str());
}