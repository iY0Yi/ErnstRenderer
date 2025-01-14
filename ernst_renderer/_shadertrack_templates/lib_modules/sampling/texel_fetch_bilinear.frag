vec4 lerp(float x, vec4 a, vec4 b) { return mix(a, b, x); }

vec4 texelFetchBilinear(sampler2D tex, vec2 t) {
#define SAM(a, b) texelFetch(iChannel0, ivec2(i + vec2(float(a), float(b))), 0)
  vec2 p = t - 0.5;
  vec2 f = fract(p);
  vec2 i = floor(p);

  return lerp(f.y, lerp(f.x, SAM(0, 0), SAM(1, 0)),
              lerp(f.x, SAM(0, 1), SAM(1, 1)));
}
