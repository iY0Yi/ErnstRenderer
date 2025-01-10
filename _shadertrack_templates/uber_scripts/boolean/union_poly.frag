// "polyAbs" by iq:
// https://www.shadertoy.com/view/3sVBRG
float polyAbs(float x, float m, float n){
	x = abs(x);
	if( x>m ) return x;
	float a = 2.0*n - m;
	float b = 2.0*m - 3.0*n;
	float t = x/m;
	return (a*t + b)*t*t + n;
}

float fOpUnionPoly(float a, float b, float m, float n){
	return (a+b-polyAbs(a-b, m, n))*.5;
}

vec4 v4OpUnionPoly(vec4 a, vec4 b, float m, float n){
	float res = (a.x+b.x-polyAbs(a.x-b.x, m, n))*.5;
	return vec4(res, mix(a.yzw, b.yzw, sat(exp(-res))));
}
