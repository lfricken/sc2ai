#pragma once
#include "Unit.hpp"
class Marine : Unit
{
public:
	Marine();
	virtual ~Marine();

	virtual bool actionHook(Actions action);
protected:
	float stimCooldown;
};

