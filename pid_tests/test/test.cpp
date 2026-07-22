#include <iostream>
//#include <pid/pid.h>
#include <matplot/matplot.h>

int main(){
	//PID stnz = PID(0.0, 1.0, 1.0, 1.0)

	using namespace matplot;
	std::vector<double> x = linspace(0,10);
	std::vector<double> y = transform(x, [](auto x){return x>3;});
	//std::vector<double> z = transform(y, [](auto y){})

	plot(x,y,"k");

	return 0;
}