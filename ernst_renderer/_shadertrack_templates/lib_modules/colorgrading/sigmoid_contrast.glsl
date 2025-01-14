// borrowed from this shadertoy.
// https://www.shadertoy.com/view/3ssSz2
float sigmoidContrast(float color, float contrast, float mid) {
  contrast = contrast < 1.0 ? 0.5 + contrast * 0.5 : contrast;
  float scale_l = 1.0 / mid;
  float scale_h = 1.0 / (1.0 - mid);
  float lower = mid * pow(scale_l * color, contrast);
  float upper = 1.0 - (1.0 - mid) * pow(scale_h - scale_h * color, contrast);
  return color < mid ? lower : upper;
}
