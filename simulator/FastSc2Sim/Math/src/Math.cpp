#include "Math.hpp"
#include <cmath>

namespace Math
{
	float sqrt(float a)
	{
		return std::sqrtf(a);
	}

	float sin(float a)
	{
		return std::sin(a);
	}
	float cos(float a)
	{
		return std::cos(a);
	}
	float tan(float a)
	{
		return std::tan(a);
	}
	float asin(float a)
	{
		return std::asin(a);
	}
	float acos(float a)
	{
		return std::acos(a);
	}
	float atan2(float y, float x)
	{
		return std::atan2(y, x);
	}
}
