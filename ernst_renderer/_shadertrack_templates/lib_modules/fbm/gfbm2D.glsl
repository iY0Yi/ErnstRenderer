float gfbm(vec2 n, int rep, float pers) {
  float res = 0.;
  fbm_base(gnoise, n, rep, pers);
  return res;
}
