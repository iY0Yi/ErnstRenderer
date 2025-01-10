float bSubLin(float a, float b, float r){
  a *= -1.;
  return max(max(a, b), (a + r + b)*sqrt(.5));
}

vec4 bSubLin(vec4 a, vec4 b, float r){
  a.x *= -1.;
  float res = max(max(a.x, b.x), (a.x + r + b.x)*sqrt(.5));
  vec3 m = mix(b.yzw, a.yzw, clamp(a.x-res,0.,1.)*r);
  return vec4(res, m);
}
