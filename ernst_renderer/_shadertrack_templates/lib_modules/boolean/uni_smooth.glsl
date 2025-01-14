float bUniS(float a,float b,float r){
  r*=1.35;
  float h = max(r-abs(a-b), 0.)/r;
  return min(a, b) - h*h*h*r*(1./6.);
}

vec4 bUniS(vec4 a,vec4 b,float r){
  float h=clamp(.5+.5*(b.x-a.x)/r,0.,1.);
  float res = mix(b.x,a.x,h)-r*h*(1.-h);
  return vec4(res, mix(b.yzw,a.yzw,h));
}
