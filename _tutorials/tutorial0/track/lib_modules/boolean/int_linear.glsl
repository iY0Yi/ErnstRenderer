float bIntLin(float a, float b, float r) {
  return max(max(a, b), (a + r + b) * sqrt(.5));
}

vec4 bIntLin(vec4 b, vec4 a, float r) {
  float d = max(max(a.w, b.w), (a.w + r + b.w) * sqrt(.5));
  vec3 m = mix(b.rgb, a.rgb, clamp(a.w - d, 0., 1.) * r);
  return vec4(m, d);
}
