float bIntS(float a, float b, float r) {
  vec2 u = max(vec2(r + b, r + a), vec2(0));
  return min(-r, max(b, a)) + length(u);
}

vec4 bIntS(vec4 a, vec4 b, float r) {
  vec2 u = max(vec2(r + b.w, r + a.w), vec2(0));
  float d = min(-r, max(b.w, a.w)) + length(u);
  vec3 m = mix(a.rgb, b.rgb, clamp(a.w - d, 0., 1.) * r);
  return vec4(m, d);
}
