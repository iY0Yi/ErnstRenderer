float bUniLin(float a, float b, float r){
  return min(min(a, b), (a - r + b)*sqrt(.5));
}

vec4 bUniLin(vec4 a, vec4 b, float r){
  float res = min(min(a.x, b.x), (a.x - r + b.x)*sqrt(.5));
  if(res==b.x) return b;
  return vec4(res, a.yzw);
}
