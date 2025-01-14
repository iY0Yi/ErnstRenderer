float bUniStp(float a, float b, float r, float n) {
  float s = r / (n + 1.);
  float u = b - r;
  return min(min(a, b), .5 * (u + a + abs((mod(u - a + s, 2. * s)) - s)));
}

vec4 bUniStp(vec4 a, vec4 b, float r, float n) {
  float s = r / (n + 1.);
  float u = b.w - r;
  float d = min(min(a.w, b.w), .5 * (u + a.w + abs((mod(u - a.w + s, 2. * s)) - s)));
  if(d >= b.w - .001) return b;
  return vec4(a.rgb, d);
}
