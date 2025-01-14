float bSubStp(float b, float a, float r, float n) {
  a *= -1.;
  float s = r / (n + 1.);
  float u = b - r;
  return -min(min(a, b), .5 * (u + a + abs((mod(u - a + s, 2. * s)) - s)));
}

vec4 bSubStp(vec4 b, vec4 a, float r, float n) {
  a.w *= -1.;
  float s = r / (n + 1.);
  float u = b.w - r;
  float d = min(min(a.w, b.w), .5 * (u + a.w + abs((mod(u - a.w + s, 2. * s)) - s)));
  if(d >= b.w) return vec4(b.rgb, -b.w);
  return vec4(a.rgb, -d);
}
