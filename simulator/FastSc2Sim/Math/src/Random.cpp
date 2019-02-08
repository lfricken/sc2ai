#include "Random.hpp"

#include <time.h>
#include <random>

struct RandVars
{
	RandVars(int unused)
	{
		gen.seed(static_cast<int>(time(nullptr)));
	}
	std::default_random_engine gen;

	std::uniform_int_distribution<int> ints;
	std::uniform_real_distribution<float> floats;
	std::uniform_real_distribution<double> doubles;
};


RandVars& vars()
{
	static RandVars variables(0);
	return variables;
}


int Rand::get(int minInclusive, int maxExclusive)
{
	std::uniform_int_distribution<int>::param_type range(minInclusive, maxExclusive - 1);
	vars().ints.param(range);
	return vars().ints(vars().gen);
}
float Rand::get(float minInclusive, float maxExclusive)
{
	std::uniform_real_distribution<float>::param_type range(minInclusive, maxExclusive);
	vars().floats.param(range);
	return vars().floats(vars().gen);
}
double Rand::get(double minInclusive, double maxExclusive)
{
	std::uniform_real_distribution<double>::param_type range(minInclusive, maxExclusive);
	vars().doubles.param(range);
	return vars().doubles(vars().gen);
}
bool Rand::didSucceed(float successChance)
{
	float dieRoll = Rand::get(0.f, 1.f);
	return dieRoll < successChance;
}
