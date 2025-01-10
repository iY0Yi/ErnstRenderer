float wfbm(vec2 n, int rep, float pers) {
  float res = 0.;
  fbm_base(wnoise, n, rep, pers);
  return res;
}
