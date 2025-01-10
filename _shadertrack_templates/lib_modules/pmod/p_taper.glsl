void pTaper(inout vec2 p, float k){
	float ipy = mix(1./p.y, 1., k);
	p.x=p.x*ipy;
}