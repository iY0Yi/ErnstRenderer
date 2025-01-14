//"Bicubic - comparison" by iq. https://shadertoy.com/view/XsSXDy
vec4 BS_A = vec4(3.0, -6.0, 0.0, 4.0) / 6.0;
vec4 BS_B = vec4(-1.0, 6.0, -12.0, 8.0) / 6.0;
vec4 RE_A = vec4(21.0, -36.0, 0.0, 16.0) / 18.0;
vec4 RE_B = vec4(-7.0, 36.0, -60.0, 32.0) / 18.0;
vec4 CR_A = vec4(3.0, -5.0, 0.0, 2.0) / 2.0;
vec4 CR_B = vec4(-1.0, 5.0, -8.0, 4.0) / 2.0;

vec4 powers(float x) { return vec4(x * x * x, x * x, x, 1.0); }

/*
#define ca BS_A
#define cb BS_B
//*/
//*
#define ca RE_A
#define cb RE_B
//*/
/*
#define ca CR_A
#define cb CR_B
//*/

vec4 spline(float x, vec4 c0, vec4 c1, vec4 c2, vec4 c3) {
  return c0 * dot(cb, powers(x + 1.0)) +
         c1 * dot(ca, powers(x)) +
         c2 * dot(ca, powers(1.0 - x)) +
         c3 * dot(cb, powers(2.0 - x));
}

vec4 texelFetchBicubic(sampler2D tex, vec2 t) {
#define SAM(a, b) texelFetch(iChannel0, ivec2(i + vec2(float(a), float(b))), 0)
  vec2 p = t - 0.5;
  vec2 f = fract(p);
  vec2 i = floor(p);
  return spline(f.y, spline(f.x, SAM(-1, -1), SAM(0, -1), SAM(1, -1), SAM(2, -1)),
                spline(f.x, SAM(-1, 0), SAM(0, 0), SAM(1, 0), SAM(2, 0)),
                spline(f.x, SAM(-1, 1), SAM(0, 1), SAM(1, 1), SAM(2, 1)),
                spline(f.x, SAM(-1, 2), SAM(0, 2), SAM(1, 2), SAM(2, 2)));
}
