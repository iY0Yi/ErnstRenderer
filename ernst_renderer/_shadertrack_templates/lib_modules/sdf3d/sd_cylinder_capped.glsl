float sdCappedCylinder(vec3 p, vec2 h){
	vec2 d = abs(vec2(length(p.xz),p.y)) - h;
	return ((min(max(d.x,d.y),0.) + length(max(d,0.))));
}