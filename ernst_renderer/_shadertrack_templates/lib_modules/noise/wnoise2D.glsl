// Just a copy from https://www.shadertoy.com/view/tldSRj
// your needs. This one is here just as example and should not
// be used in production.
//vec2 g( vec2 n ) { return sin(n.x*n.y*vec2(12,17)+vec2(1,2)); }
vec2 g( vec2 n ) { return sin(n.x*n.y+vec2(0,1.571)); } // if you want the gradients to lay on a circle
float wnoise(vec2 st){
	st *= .6; // adjust scale
	const float kF = 3.1415927;  // make 6 to see worms

	vec2 i = floor(st);
	vec2 f = fract(st);
	f = f*f*(3.0-2.0*f);
	return s2u(mix(mix(sin(kF*dot(st,g(i+vec2(0,0)))),
				   sin(kF*dot(st,g(i+vec2(1,0)))),f.x),
			   mix(sin(kF*dot(st,g(i+vec2(0,1)))),
				   sin(kF*dot(st,g(i+vec2(1,1)))),f.x),f.y));
}
