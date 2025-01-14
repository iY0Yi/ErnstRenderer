vec2 hash21(uint q){
	uvec2 n = q * UI2;
	n = (n.x ^ n.y) * UI2;
	return vec2(n) * UIF;
}
