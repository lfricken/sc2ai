#include "Unit.hpp"

Unit::Unit()
{

}
Unit::~Unit()
{

}
void Unit::shot()
{
	weapon.remainingCooldown += weapon.cooldown;
}
bool Unit::canShoot()
{
	return weapon.remainingCooldown <= 0;
}
void Unit::actionMove(const Vec2& position)
{

}
void Unit::actionAttack(const Vec2& position)
{

}
bool Unit::action(Actions action)
{
	return actionHook(action);
}
bool Unit::actionHook(Actions action)
{
	return false;
}

void Unit::worldTick(float timeDelta)
{
	if (!canShoot)
	{
		weapon.remainingCooldown -= timeDelta;
	}

	worldTickHook(timeDelta);
}
void Unit::worldTickHook(float timeDelta)
{

}