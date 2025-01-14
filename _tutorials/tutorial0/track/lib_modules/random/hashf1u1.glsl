float hash11(uint q){
	uvec2 n = q * UI2;
	q = (n.x ^ n.y) * UI0;
	return float(q) * UIF;
}
