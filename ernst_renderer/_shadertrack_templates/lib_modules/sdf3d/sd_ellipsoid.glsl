float sdEllipsoid(vec3 p, vec3 r){
	float k0 = length(p/r);
  float k1 = length(p/(r*r));
  return k0*(k0-1.)/k1;
} 