float sdConeSection(vec3 p, float h, float r1, float r2){
	vec2 q = vec2(length(p.xz), p.y);
	vec2 k1 = vec2(r2,h);
	vec2 k2 = vec2(r2-r1,2.*h);
	vec2 ca = vec2(q.x-min(q.x,(q.y < 0.)?r1:r2), abs(q.y)-h);
	vec2 cb = q - k1 + k2*clamp(dot(k1-q,k2)/dot(k2,k2), 0., 1.);
	float s = (cb.x < 0. && ca.y < 0.) ? -1. : 1.;
	return s*sqrt(min(dot(ca,ca),dot(cb,cb)));
}