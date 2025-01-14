float bInt(float a, float b) {
  return max(a, b);
}

vec4 bInt(vec4 a, vec4 b) {
  return (max(a.w, b.w) == a.w) ? a : b;
}
