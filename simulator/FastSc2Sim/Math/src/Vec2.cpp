#include "Vec2.hpp"
#include <iostream>
#include "Math.hpp"

namespace Math
{
	Vec2::Vec2()
	{
		x = 0.f;
		y = 0.f;
	}
	Vec2::Vec2(Vec2Short vec)
	{
		x = static_cast<float>(vec.x);
		y = static_cast<float>(vec.y);
	}
	Vec2::Vec2(float xi, float yi)
	{
		x = xi;
		y = yi;
	}


	bool Vec2::operator==(const Vec2& other) const
	{
		return (x == other.x) && (y == other.y);
	}
	Vec2 Vec2::operator+(const Vec2& other) const
	{
		return Vec2(this->x + other.x, this->y + other.y);
	}
	Vec2 Vec2::operator-(const Vec2& other) const
	{
		return Vec2(this->x - other.x, this->y - other.y);
	}
	Vec2 Vec2::operator*(const Vec2& other) const
	{
		return Vec2(this->x * other.x, this->y * other.y);
	}
	Vec2 Vec2::operator/(const Vec2& other) const
	{
		return Vec2(this->x / other.x, this->y / other.y);
	}



	Vec2& Vec2::operator+=(const Vec2& other)
	{
		x += other.x;
		y += other.y;
		return *this;
	}
	Vec2& Vec2::operator-=(const Vec2& other)
	{
		x -= other.x;
		y -= other.y;
		return *this;
	}
	Vec2& Vec2::operator*=(const Vec2& other)
	{
		x *= other.x;
		y *= other.y;
		return *this;
	}
	Vec2& Vec2::operator/=(const Vec2& other)
	{
		x /= other.x;
		y /= other.y;
		return *this;
	}



	Vec2 Vec2::operator+(float c) const
	{
		return Vec2(this->x + c, this->y + c);
	}
	Vec2 Vec2::operator-(float c) const
	{
		return Vec2(this->x - c, this->y - c);
	}
	Vec2 Vec2::operator*(float c) const
	{
		return Vec2(this->x * c, this->y * c);
	}
	Vec2 Vec2::operator/(float c) const
	{
		return Vec2(this->x / c, this->y / c);
	}



	Vec2& Vec2::operator+=(float c)
	{
		x += c;
		y += c;
		return *this;
	}
	Vec2& Vec2::operator-=(float c)
	{
		x -= c;
		y -= c;
		return *this;
	}
	Vec2& Vec2::operator*=(float c)
	{
		x *= c;
		y *= c;
		return *this;
	}
	Vec2& Vec2::operator/=(float c)
	{
		x /= c;
		y /= c;
		return *this;
	}



	Vec2 Vec2::inv() const
	{
		return Vec2(-x, -y);
	}
	Vec2 Vec2::to(const Vec2& other) const
	{
		return other - *this;
	}
	Vec2 Vec2::rotate(float radiansCCW) const
	{
		float cs = Math::cos(radiansCCW);
		float sn = Math::sin(radiansCCW);
		return Vec2(x * cs - y * sn, x * sn + y * cs);
	}
	float Vec2::len() const
	{
		return Math::sqrt(x*x + y * y);
	}
	Vec2 Vec2::unit() const
	{
		float l = len();
		return Vec2(x / l, y / l);
	}
	Vec2 Vec2::bounce(const Vec2& normal) const
	{
		Vec2 u = normal * ((*this).dot(normal) / normal.dot(normal));
		Vec2 w = *this - u;
		return w - u;
	}
	float Vec2::dot(const Vec2& other) const
	{
		return x * other.x + y * other.y;
	}
	float Vec2::toAngle() const
	{
		return Math::atan2(y, x);
	}
}

