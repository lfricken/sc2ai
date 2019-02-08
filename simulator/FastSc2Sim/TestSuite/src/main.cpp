#include "TestSuite.hpp"

template <typename T>
T get() { return 0; };
template < >
float get<float>() { return 1.5; };
template < >
int get<int>() { return 2; };
template < >
double get<double>() { return 2.666666666; };
template < >
String get<String>() { return "lol"; };

int main()
{
	getSuite().runAllTests();
	getSuite().results();

	Print << "\n\nTwenty Random Numbers [0-9]:";
	for(int i = 0; i < 20; i++)
		Print << "\n" << Rand::get(0, 10);

	getSuite().pause();
	return 0;
}



