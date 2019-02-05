#pragma once

#include "Constant.hpp"
namespace Math
{
	/// <summary>
	/// Convert from degrees to radians.
	/// </summary>
	template<typename T>
	T toRad(T value)
	{
		return (Math::Tau*static_cast<float>(value)) / Math::Degrees;
	}

	/// <summary>
	/// Convert from radians to degrees.
	/// </summary>
	template<typename T>
	T toDeg(T value)
	{
		return (Math::Degrees*static_cast<float>(value)) / Math::Tau;
	}

	/// <summary>
	/// Normalize radians between 0 and Tau.
	/// </summary>
	template<typename T>
	T normalizeRad(T value)
	{
		while(value > Math::Tau)
			value -= Math::Tau;

		while(value < 0.f)
			value += Math::Tau;

		return value;
	}
}

