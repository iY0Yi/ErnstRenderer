// "Limited Repetition SDF" by iq:
// https://www.shadertoy.com/view/3syGzz
void pRepLim(inout float p, float s, float repetitions){
	repetitions -= 1.;
	float offset = 1.-step(.5, mod(repetitions, 2.));
	p += s*.5*offset;
	float r = round(p/s);
	float half_rep = ceil(repetitions/2.);
	r = clamp(r, -half_rep, repetitions-half_rep);
	p-=s*r;
}