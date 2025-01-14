// "Random number generator" by Toshiya Hachisuka:
// https://www.ci.i.u-tokyo.ac.jp/~hachisuka/tdf2015.pdf
vec4 seed;
float GPURnd(inout vec4 n) {
  // Based on the post http://gpgpu.org/forums/viewtopic.php?t=2591&sid=17051481b9f78fb49fba5b98a5e0f1f3
  // (The page no longer exists as of March 17th, 2015. Please let me know if you see why this code works.)
  const vec4 q = vec4(1225., 1585., 2457., 2098.);
  const vec4 r = vec4(1112., 367., 92., 265.);
  const vec4 a = vec4(3423., 2646., 1707., 1999.);
  const vec4 m = vec4(4194287., 4194277., 4194191., 4194167.);
  vec4 beta = floor(n/q);
  vec4 p = a*(n-beta*q)-beta*r;
  beta = (sign(-p)+vec4(1))*vec4(.5)*m;
  n = p+beta;
  return fract(dot(n/m,vec4(1,-1,1,-1)));
}
