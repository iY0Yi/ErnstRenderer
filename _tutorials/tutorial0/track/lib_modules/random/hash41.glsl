vec4 hash41(float p){
	uvec4 q = uvec4(ivec4(p)) * UI4;
	q = (q.x ^ q.y ^ q.z ^ q.w)*UI4;
	return vec4(q) * UIF;
}
