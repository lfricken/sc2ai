#pragma once

#include <memory>
#include <vector>
#include <map>
#include <iostream>
#include <string>

template<typename T>
using sp = std::shared_ptr < T > ;

template<typename T>
using wp = std::weak_ptr < T > ;

template<typename T>
using List = std::vector < T > ;

template<typename T, typename R>
using Map = std::map < T, R > ;

template<typename T, typename R>
using Pair = std::pair < T, R > ;

class String : public std::string
{
public:
	String()
	{

	}
	String(const char* init)
	{
		this->assign(init);
	}
	template<typename T>
	String(T num)
	{
		from(num);
	}
	int toInt()
	{
		return std::stoi(*this);
	}
	float toFloat()
	{
		return std::stof(*this);
	}
	double toDouble()
	{
		return std::stod(*this);
	}
	template<typename T>
	void from(T num)
	{
		this->assign(std::to_string(num));
		trimZeros();
	}

	String(const std::string& other)
	{
		*this = other.c_str();
	}
	operator std::string() const
	{
		return static_cast<std::string>(*this);
	}
private:
	void trimZeros()
	{
		//if it has a decimal place try removing 0s
		if(this->find('.') != std::string::npos)
		{
			for(int x = length() - 1; x >= 0; --x) // count backward
			{
				if((*this)[x] != '0' && (*this)[x] != '.')
				{
					(*this).resize(x + 1); // shrink to appropriate size (x is counting backward)
					break;
				}
			}
		}
	}
};


class print
{
public:
	template<typename T>
	std::ostream& operator<<(T o)
	{
		std::cout << o;
		return std::cout;
	}
} extern Print;
class input
{
public:
	template<typename T>
	std::istream& operator>>(T& o)
	{
		std::cin >> o;
		return std::cin;
	}
} extern Input;



