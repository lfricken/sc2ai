


#include <iostream>


int main()
{
	int i;
	std::cout << "Works.";
	std::cin >> i;
	return 0;
}


#include <boost/python.hpp>

BOOST_PYTHON_MODULE(hello_ext)
{
	using namespace boost::python;
	def("greet", greet);
}



