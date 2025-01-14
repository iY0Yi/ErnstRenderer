float bUniS(float a, float b, float r) {
  r *= 1.35;
  float h = max(r - abs(a - b), 0.) / r;
  return min(a, b) - h * h * h * r * (1. / 6.);
}

vec4 bUniS(vec4 a, vec4 b, float r) {
  // float h = clamp(.5 + .5 * (b.w - a.w) / r, 0., 1.);
  float h = smoothstep(0., 1., .5 + .5 * (b.w - a.w) / r);
  float d = mix(b.w, a.w, h) - r * h * (1. - h);
  return vec4(pow_mix(b.rgb, a.rgb, h), d);
}
