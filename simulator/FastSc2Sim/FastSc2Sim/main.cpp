
#include <iostream>
#include <boost/python.hpp>


int main()
{
	int i;
	std::cout << "Works.";
	std::cin >> i;
	return 0;
}

char const* greet()
{
	return "hello, world";
}

BOOST_PYTHON_MODULE(hello_ext)
{
	using namespace boost::python;
	def("greet", greet);
}



