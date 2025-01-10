// https://www.shadertoy.com/view/llSyRD
float TonemapCompressRangeNorm(float x) {
  return 1.0f - exp(-x);
}
float TonemapCompressRangeFloat(float x, float t) {
  return (x < t) ? x : t + TonemapCompressRangeNorm((x - t) / (1.0f - t)) * (1.0f - t);
}
vec3 TonemapCompressRangeFloat3(vec3 x, float t) {
  x.r = TonemapCompressRangeFloat(x.r, t);
  x.g = TonemapCompressRangeFloat(x.g, t);
  x.b = TonemapCompressRangeFloat(x.b, t);
  return x;
}
vec3 tonemapPMalin(vec3 x) {
  return TonemapCompressRangeFloat3(x, 0.6);
}
