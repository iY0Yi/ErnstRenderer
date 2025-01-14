float sdCappedTorus(vec3 p, vec2 r, float per){
	p.x = abs(p.x);
	vec2 sc = vec2(sin(per),cos(per));
	float k = (sc.y*p.x>sc.x*p.z) ? dot(p.xz,sc) : length(p.xz);
	return sqrt(dot(p,p) + r.x*r.x - 2.*r.x*k) - r.y;
}