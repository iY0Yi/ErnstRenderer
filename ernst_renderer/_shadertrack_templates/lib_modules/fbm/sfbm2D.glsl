float sfbm(vec2 n, int rep, float pers) {
  float res = 0.;
  fbm_base(snoise, n, rep, pers);
  return res;
}
