// Custom Boolean Example: UnionSink
float fOpUnionSink(float a, float b, float r, float n) {
	vec2 p = vec2(a, b);
	float rad = r*sqrt(2.)/(2.+sqrt(2.));
	p.x -= sqrt(2.)/2.*r;
	p.x += rad*sqrt(2.0);
	p.y -= rad;
	float d = length(p+vec2(0,n)) - rad;
	d = bUniS(d, b, p.x);
	d = min(d, a);
	return d;
}

vec4 v4OpUnionSink(vec4 a, vec4 b, float r, float n) {
	vec2 p = vec2(a.x, b.x);
	float rad = r*sqrt(2.)/(2.+sqrt(2.));
	p.x -= sqrt(2.)/2.*r;
	p.x += rad*sqrt(2.0);
	p.y -= rad;
	float d = length(p+vec2(0,n)) - rad;
	d = bUniS(d, b.x, p.x);
	d = min(d, a.x);
	return vec4(d, (d==a.x)?a.yzw:b.yzw);
}