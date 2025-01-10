float bUniStp(float a, float b, float r, float n){
  float s = r/(n+1.);
  float u = b-r;
  return min(min(a,b), .5 * (u + a + abs ((mod (u - a + s, 2. * s)) - s)));
}

vec4 bUniStp(vec4 a, vec4 b, float r, float n){
  float s = r/(n+1.);
  float u = b.x-r;
  float res = min(min(a.x,b.x), .5 * (u + a.x + abs ((mod (u - a.x + s, 2. * s)) - s)));
  if(res>=b.x-.001) return b;
  return vec4(res, a.yzw);
}
