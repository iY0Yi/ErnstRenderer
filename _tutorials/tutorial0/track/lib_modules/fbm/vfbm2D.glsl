float vfbm(vec2 n, int rep, float pers) {
  float res = 0.;
  fbm_base(vnoise, n, rep, pers);
  return res;
}
