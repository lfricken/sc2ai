#pragma once

#include <random>

/// <summary>
/// Handles probability.
/// </summary>
class Rand
{
public:
	/// <summary>
	/// Grab a random number in the range [minInclusive, maxExclusive)
	/// </summary>
	static int get(int minInclusive, int maxExclusive);
	/// <summary>
	/// Grab a random number in the range [minInclusive, maxExclusive)
	/// </summary>
	static float get(float minInclusive, float maxExclusive);
	/// <summary>
	/// Grab a random number in the range [minInclusive, maxExclusive)
	/// </summary>
	static double get(double minInclusive, double maxExclusive);
	/// <summary>
	/// Return true with the given odds, 0-1.
	/// </summary>
	static bool didSucceed(float successChance);
};
