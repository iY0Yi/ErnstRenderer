float hash11(float p){
	uvec2 n = uint(int(p)) * UI2;
	uint q = (n.x ^ n.y) * UI0;
	return float(q) * UIF;
}
