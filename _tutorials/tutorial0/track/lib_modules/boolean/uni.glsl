float bUni(float a, float b) {
  return a < b ? a : b;
}

vec4 bUni(vec4 a, vec4 b) {
  return a.w < b.w ? a : b;
}
