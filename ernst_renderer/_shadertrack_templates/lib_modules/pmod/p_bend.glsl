//Based on "bend" by las:
//https://www.pouet.net/topic.php?which=7931&page=5
void pBend(inout vec2 p, float k){
	float r = 1./k;
	if(abs(k)<1e-1)return;
	float sgn = sign(k);
	vec2 d = vec2(-p.x, (r-p.y))*sgn;
	float a = -atan(d.x, d.y);
	vec2 b = vec2(sin(a), cos(a));
	p = sgn*vec2(-b.y*d.x-b.x*d.y, b.x*d.x-b.y*d.y)+vec2(a*r,r);
}