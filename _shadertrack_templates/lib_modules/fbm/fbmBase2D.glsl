// fbm base for all noise
#define fbm_base(nname, n, rep, pers){\
	float total = 0.;\
	float frequency = 1.;\
	float amplitude = 1.;\
	float maxValue = 0.;\
	for(int i=0;i<rep;i++) {\
		total += nname(vec2(n.x * frequency, n.y * frequency)) * amplitude;\
		maxValue += amplitude;\
		amplitude *= pers;\
		frequency *= 2.;\
	}\
	res = total/maxValue;\
}
