float bSubS(float a,float b,float r){
  r*=1.35;
  a = -a;
  float h = max(r-abs(a-b), 0.)/r;
  return max(a, b) + h*h*h*r*(1./6.);
}

vec4 bSubS(vec4 a,vec4 b,float r){
  r*=1.35;
  a.x = -a.x;
  float h = max(r-abs(a.x-b.x), 0.)/r;
  float res = max(a.x, b.x) + h*h*h*r*(1./6.);
  vec3 m = mix(b.yzw, a.yzw, clamp(abs(-b.x)+abs(res),0.,1.)*clamp(r,0.,1.));
  return vec4(res, m);
}
