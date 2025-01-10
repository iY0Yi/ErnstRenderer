vec3 hash32(vec2 p){
	vec3 p3 = fract(vec3(p.xyx) * vec3(.1031, .1030, .0973));
	p3 += dot(p3, p3.yxz+33.33);
	return fract((p3.xxy+p3.yzz)*p3.zyx);
}
