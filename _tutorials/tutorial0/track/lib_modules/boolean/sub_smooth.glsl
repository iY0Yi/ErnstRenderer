float bSubS(float a, float b, float r) {
  r *= 1.35;
  a = -a;
  float h = max(r - abs(a - b), 0.) / r;
  return max(a, b) + h * h * h * r * (1. / 6.);
}

vec4 bSubS(vec4 a, vec4 b, float r) {
  r *= 1.35;
  a.w = -a.w;
  float h = max(r - abs(a.w - b.w), 0.) / r;
  float d = max(a.w, b.w) + h * h * h * r * (1. / 6.);
  vec3 m = mix(b.rgb, a.rgb, clamp(abs(-b.w) + abs(d), 0., 1.) * clamp(r, 0., 1.));
  return vec4(m, d);
}
