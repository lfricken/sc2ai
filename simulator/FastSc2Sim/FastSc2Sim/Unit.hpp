#pragma once

#include "Vec2.hpp"
#include "Actions.hpp"

using namespace Math;

struct Weapon
{
	
	bool air;
	bool ground;
	uint8_t damage;
	uint8_t aoeRadius; // Tenths of units in of the radius of a circle for damage.
	float cooldown; // Cooldown of weapon.
	float remainingCooldown; // Once this value is zero or negative, we can shoot again.
};

struct Health
{
	uint8_t armor;
	short health;
	// eventually do regen shields?
};

struct Movement
{
	uint8_t speed; // Tenths of units per second.
	uint8_t collisionRadius; // Tenths of units in radius circle.
	bool cliffwalk;
	bool air;
};

class Unit
{
public:
	Unit();
	virtual ~Unit();

	Weapon weapon;
	Health health;
	Movement movement;

	//Called on a unit that just shot its weapon.
	virtual void shot();

	//True if this unit can shoot now.
	virtual bool canShoot();

	virtual void actionMove(const Vec2& position);
	virtual void actionAttack(const Vec2& position);

	bool action(Actions action);

	void worldTick(float timeDelta);
protected:
	virtual bool actionHook(Actions action);
	virtual void worldTickHook(float timeDelta);
};

