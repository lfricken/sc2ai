#pragma once
#include <iostream>

namespace Math
{
	class Vec2
	{
	public:
		Vec2();
		Vec2(float xi, float yi);

		float x;
		float y;

		/// <summary>
		/// Compares components pairwise.
		/// </summary>
		bool operator==(const Vec2& other) const;

		Vec2 operator+(const Vec2& other) const;
		Vec2 operator-(const Vec2& other) const;
		Vec2 operator*(const Vec2& other) const;
		Vec2 operator/(const Vec2& other) const;

		Vec2& operator+=(const Vec2& other);
		Vec2& operator-=(const Vec2& other);
		Vec2& operator*=(const Vec2& other);
		Vec2& operator/=(const Vec2& other);

		/// <summary>
		/// Applies constant to each component.
		/// </summary>
		Vec2 operator+(float c) const;
		Vec2 operator-(float c) const;
		Vec2 operator*(float c) const;
		Vec2 operator/(float c) const;

		Vec2& operator+=(float c);
		Vec2& operator-=(float c);
		Vec2& operator*=(float c);
		Vec2& operator/=(float c);


		/// <summary>
		/// Returns this vector inversed.
		/// </summary>
		Vec2 inv() const;
		/// <summary>
		/// Returns the vector that starts at this vector and ends at another.
		/// </summary>
		Vec2 to(const Vec2& other) const;
		/// <summary>
		/// Return this vector rotated. CCW radians.
		/// </summary>
		Vec2 rotate(float radiansCCW) const;
		/// <summary>
		/// Return length of this vector.
		/// </summary>
		float len() const;
		/// <summary>
		/// Return unit vector of this vector.
		/// </summary>
		Vec2 unit() const;
		/// <summary>
		/// Return this ray as if it was bounced off of a surface normal vector.
		/// </summary>
		Vec2 bounce(const Vec2& normal) const;
		/// <summary>
		/// Return the dot product of this vector and another.
		/// </summary>
		float dot(const Vec2& other) const;
		/// <summary>
		/// Return the angle this vector produces with respect to the positive x axis. CCW radians.
		/// </summary>
		float toAngle() const;

		/// <summary>
		/// Print this vector as "(x, y)".
		/// </summary>
		inline friend std::ostream& operator<<(std::ostream &os, const Vec2& vec)
		{
			return os << "(" << vec.x << ", " << vec.y << ")";
		}
	};
}
