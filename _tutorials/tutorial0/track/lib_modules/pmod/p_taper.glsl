void pTaper(inout vec2 p, float k){
	p.x=p.x-sign(p.x)*p.y*k;
}