#pragma once

#include "Convert.hpp"
#include "Random.hpp"
#include "Constant.hpp"
#include "Vec2.hpp"
#include "OOCore.hpp"

namespace Math
{
#ifdef min
#undef min
#endif
	template<typename T>
	T min(T a, T b)
	{
		if(a < b)
			return a;
		else
			return b;
	}
#ifdef max
#undef max
#endif
	template<typename T>
	inline T max(T a, T b)
	{
		if(a > b)
			return a;
		else
			return b;
	}
#ifdef abs
#undef abs
#endif
	template<typename T>
	T abs(T a)
	{
		if(a < 0)
			return -T;
		else
			return a;
	}

	float sqrt(float a);

	float sin(float a);
	float cos(float a);
	float tan(float a);

	float asin(float a);
	float acos(float a);
	float atan2(float y, float x);
}


