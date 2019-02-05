#include "Marine.hpp"

Marine::Marine()
{
	health.armor = 0;
	health.health = 45;

	movement.air = false;
	movement.cliffwalk = false;
	movement.collisionRadius = 37;
	movement.speed = 32;

	weapon.damage = 6;
	weapon.cooldown = 0.8606;
	weapon.air = true;
	weapon.ground = true;
	weapon.aoeRadius = 0;
	weapon.remainingCooldown = 0;

	stimCooldown = 0;
}
Marine::~Marine()
{

}
bool Marine::actionHook(Actions action)
{
	switch (action)
	{
	case Actions::Stimpack:
		health.health -= 5;
		return true;
	}

	return false;
}