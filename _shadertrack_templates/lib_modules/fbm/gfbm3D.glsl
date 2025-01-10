float gfbm(vec3 n, int rep, float pers) {
  float G = exp2(-.85);
  float amp = 1.;
  float noise = 0.;
  for(int i = 0; i < rep; ++i) {
    noise += amp * gnoise(n * pers, pers);
    pers *= 2.;
    amp *= G;
  }

  return noise;
}
