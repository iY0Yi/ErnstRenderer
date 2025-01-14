vec4 hash42(vec2 p){
	uvec4 q = uvec4(ivec4(p.xyxy)) * UI4;
	q = (q.x ^ q.y ^ q.z ^ q.w)*UI4;
	return vec4(q) * UIF;
}
