#define ISO_X 1
#define ISO_Y 2
#define ISO_Z 3
vec3 debugIso(int axis, float cut, float baseSize){
	#define COL_HIT vec3(1)
	#define COL_LINE_POS vec3(.3)
	#define COL_LINE_NEG vec3(.125)
	#define COL_POS vec3(.5)
	#define COL_NEG vec3(.075)
	if(axis == ISO_X)      cut = (ray.origin.x - cut) / -ray.direction.x;
	else if(axis == ISO_Y) cut = (ray.origin.y - cut) / -ray.direction.y;
	else if(axis == ISO_Z) cut = (ray.origin.z - cut) / -ray.direction.z;
	vec3 p = ray.origin + ray.direction * cut;
	float d = sdScene(p).x;

	float iso = abs(u2s(fract(d * baseSize)));
	float isoPrec = abs(u2s(fract(d * baseSize * 10.)));
	float measure = smoothstep(1., .95, iso);
	measure *= smoothstep(1., .7, isoPrec);

	vec3 res = mix(COL_NEG, COL_POS, s2u(sign(d*5.)));
	if(sign(d)>0.)
		res = mix(res, COL_LINE_POS, 1.-measure);
	else
		res = mix(res, COL_LINE_NEG, 1.-measure);
	res = mix(res, COL_HIT, 1.-smoothstep(.0, .05, abs(d)));
	return res;
}
