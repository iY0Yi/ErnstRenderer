float sdPieCylinder(vec3 p, float r, float h, float per){
	per = mod(per, PI);
	vec2 c = vec2(sin(per),cos(per));
	p.xz=c.y*p.xz+c.x*vec2(p.z,-p.x); // rotation
	p.x = abs(p.x);
	float l = length(p.xz) - r;
	float m = length(p.xz-c*clamp(dot(p.xz,c),0., r));
	float x = max(l,m*sign(c.y*p.x-c.x*p.z));
	float y = abs(p.y) - h;
	return ((min(max(x,y),0.) + length(max(vec2(x,y),0.))));
}