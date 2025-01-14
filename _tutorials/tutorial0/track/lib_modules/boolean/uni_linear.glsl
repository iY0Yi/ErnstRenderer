float bUniLin(float a, float b, float r) {
  return min(min(a, b), (a - r + b) * sqrt(.5));
}

vec4 bUniLin(vec4 a, vec4 b, float r) {
  float d = min(min(a.w, b.w), (a.w - r + b.w) * sqrt(.5));
  if(d == b.w) return b;
  return vec4(a.rgb, d);
}
