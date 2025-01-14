float vorofbm(vec2 n, int rep, float pers) {
  float res = 0.;
  fbm_base(voronoi, n, rep, pers);
  return res;
}
