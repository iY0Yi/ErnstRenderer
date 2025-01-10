// "hg_sdf" by mercury:
// http://mercury.sexy/hg_sdf/
void pRepPolar(inout vec2 p, float repetitions) {
	float angle = 2.*PI/repetitions;
	float a = atan(p.y, p.x) + angle/2.;
	a = mod(a,angle) - angle/2.;
	p = vec2(cos(a), sin(a))*length(p);
}