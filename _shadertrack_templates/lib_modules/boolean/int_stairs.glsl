float bIntStp(float a, float b, float r, float n){
  a *=-1.;
  b *=-1.;
  float s = r/(n+1.);
  float u = b-r;
  return -min(min(a,b), .5 * (u + a + abs ((mod (u - a + s, 2. * s)) - s)));
}

vec4 bIntStp(vec4 a, vec4 b, float r, float n){
  a.x *=-1.;
  b.x *=-1.;
  float s = r/(n+1.);
  float u = b.x-r;
  float res = min(min(a.x,b.x), .5 * (u + a.x + abs ((mod (u - a.x + s, 2. * s)) - s)));
  if(res>=b.x) return b*vec4(-1,1,1,1);
  return vec4(res, a.yzw)*vec4(-1,1,1,1);
}
