#include "TestSuite.hpp"
#include <iostream>
#include <string>

using namespace std;

TestSuite& getSuite()
{
	static TestSuite t;
	return t;
}


TestClassBase::TestClassBase(std::string Class, std::string Function)
{
	ClassName = Class;
	FunctionName = Function;
	pTestRunner = &getSuite();
	pTestRunner->give(this);
}
std::string TestClassBase::getClass()
{
	return ClassName;
}
std::string TestClassBase::getFunction()
{
	return FunctionName;
}


void TestSuite::line()
{
	setGreen();
	cout << "[----------]\n";
	setWhite();
}
void TestSuite::run()
{
	setGreen();
	cout << "[ RUN      ]";
	setWhite();
}
void TestSuite::ok()
{
	setGreen();
	cout << "[       OK ]\n";
	setWhite();
}
void TestSuite::fail()
{
	setRed();
	cout << "[     FAIL ]";
	setWhite();
}
void TestSuite::test()
{
	setGreen();
	cout << "[   TEST   ]";
	setWhite();
}
void TestSuite::failSilent()
{
	cout << "            ";
}
TestSuite::TestSuite()
{
	totalTests = 0;
	testsFailed = 0;
	conditionsFailed = 0;
	hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
}
void TestSuite::runAllTests()
{

	for(auto mapIt = m_tests.cbegin(); mapIt != m_tests.cend(); ++mapIt)
	{
		line();
		test();
		setBlue();
		std::cout << " " << mapIt->first << "\n";
		line();

		const auto& tests = mapIt->second;

		for(auto it = tests.begin(); it != tests.end(); ++it)
		{
			m_passed = true;

			run();
			std::cout << " " << (**it).getFunction() << "\n";
			(**it).testBody();
			if(m_passed)
				ok();

		}
		line();
		cout << "\n";
	}
}
void TestSuite::give(TestClassBase* instance)
{
	auto t = instance->getClass();
	m_tests[t].push_back(instance);
	totalTests++;
}
void TestSuite::pause()
{
	std::cout << "\n\nPress Enter to continue...";
	std::cin.get();
}
void TestSuite::setWhite()
{
	SetConsoleTextAttribute(hConsole, 7);
}
void TestSuite::setGreen()
{
	SetConsoleTextAttribute(hConsole, 10);
}
void TestSuite::setRed()
{
	SetConsoleTextAttribute(hConsole, 12);
}
void TestSuite::setBlue()
{
	SetConsoleTextAttribute(hConsole, 11);
}
void TestSuite::results()
{
	std::cout << "\n\n";
	line();
	{
		setGreen();
		std::cout << "[   DONE   ]";
		setBlue();
		std::cout << " " << totalTests << " tests.\n";
	}
	{
		line();
		setGreen();
		std::cout << "[  PASSED  ] ";
		setWhite();
		std::cout << (totalTests - testsFailed) << " tests.\n";
	}
	if(testsFailed != 0)
	{
		line();
		setRed();
		std::cout << "[  FAILED  ] ";
		setWhite();
		std::cout << testsFailed << " tests and " << conditionsFailed << " conditions.\n";

	}
	line();


	setWhite();
}


