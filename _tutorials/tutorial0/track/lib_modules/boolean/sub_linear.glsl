float bSubLin(float a, float b, float r) {
  a *= -1.;
  return max(max(a, b), (a + r + b) * sqrt(.5));
}

vec4 bSubLin(vec4 a, vec4 b, float r) {
  a.w *= -1.;
  float d = max(max(a.w, b.w), (a.w + r + b.w) * sqrt(.5));
  vec3 m = mix(b.rgb, a.rgb, clamp(a.w - d, 0., 1.) * r);
  return vec4(m, d);
}
