float bSub(float a, float b) {
  return max(-a, b);
}

vec4 bSub(vec4 a, vec4 b) {
  return (max(-a.w, b.w) == -a.w) ? vec4(a.rgb, -a.w) : b;
}
