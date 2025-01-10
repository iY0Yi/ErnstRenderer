float bIntLin(float a, float b, float r){
  return max(max(a, b), (a + r + b)*sqrt(.5));
}

vec4 bIntLin(vec4 b, vec4 a, float r){
  float res = max(max(a.x, b.x), (a.x + r + b.x)*sqrt(.5));
  vec3 m = mix(b.yzw, a.yzw, clamp(a.x-res,0.,1.)*r);
  return vec4(res, m);
}
