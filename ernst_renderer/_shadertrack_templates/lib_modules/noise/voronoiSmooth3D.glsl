// Smooth Voronoi
// https://iquilezles.org/www/articles/smoothvoronoi/smoothvoronoi.htm
float sminC3(float a, float b, float r) {
  float n = max(0., 1. - abs(a - b) / r);
  float o = (.25 - n * .1) * ((n * n) * (n * n));
  return min(a, b) - o * r;
}
float voronoiSmooth(vec3 p, float s) {
  vec3 i = floor(p);
  vec3 f = fract(p);

  float res = 8.;
  for(int j = -1; j <= 1; j++)
    for(int k = -1; k <= 1; k++)
      for(int l = -1; l <= 1; l++) {
        vec3 b = vec3(j, k, l);
        vec3 r = b - f + hash33(i + b);

        float d = length(r);
        res = sminC3(res, d, s);
      }
  return res;
}
