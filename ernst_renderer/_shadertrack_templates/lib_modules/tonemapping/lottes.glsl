// https://www.shadertoy.com/view/WdjSW3
float TonemapLottes(float x) {
  // Lottes 2016, "Advanced Techniques and Optimization of HDR Color Pipelines"
  const float a = 1.6;
  const float d = 0.977;
  const float hdrMax = 8.0;
  const float midIn = 0.18;
  const float midOut = 0.267;

  // Can be precomputed
  const float b =
      (-pow(midIn, a) + pow(hdrMax, a) * midOut) /
      ((pow(hdrMax, a * d) - pow(midIn, a * d)) * midOut);
  const float c =
      (pow(hdrMax, a * d) * pow(midIn, a) - pow(hdrMax, a) * pow(midIn, a * d) * midOut) /
      ((pow(hdrMax, a * d) - pow(midIn, a * d)) * midOut);

  return pow(x, a) / (pow(x, a * d) * b + c);
}
vec3 TonemapLottes(vec3 x) {
  x.r = TonemapLottes(x.r);
  x.g = TonemapLottes(x.g);
  x.b = TonemapLottes(x.b);
  return x;
}
