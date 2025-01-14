
@BL_UNIFORMS
@BLU_GUI
@CANVAS_MODE
#define ERNST_RENDER_SCALE float(@BL_RESOLUTION_SCALE)
#define INV_ERNST_RENDER_SCALE (1. / ERNST_RENDER_SCALE)

#define PI acos(-1.)
#define TAU (PI * 2.)
#define AXIS_X vec3(1,0,0)
#define AXIS_Y vec3(0,1,0)
#define AXIS_Z vec3(0,0,1)
#define sat(x) clamp(x, 0., 1.)
#define sms(min, max, x) smoothstep(min, max, x)
#define sstep(min, max, x) smoothstep(min, max, x)
#define s2u(x) (x * .5 + .5)
#define u2s(x) ((x * 2.) - 1.)
#define sign1f(x) ((x > 0.) ? 1. : -1.)
#define sign2v(v) vec2(sign1f(v.x), sign1f(v.y))
#define linearstep(edge0, edge1, x) min(max((x - (edge0)) / ((edge1) - (edge0)), 0.), 1.)
#define dot2(v) dot(v,v)
// normalized atan.
float natan(float y, float x) {return atan(y, x) / acos(-1.) * .5 + .5;}
vec2 pow2(vec2 v, float power){return pow(v, vec2(power));}
vec3 pow3(vec3 v, float power){return pow(v, vec3(power));}
float sabs(float x,float k) {float a = (.5/k)*x*x+k*.5; float b = abs(x); return b<k ? a : b;}

// https://www.shadertoy.com/view/XdV3W3
vec2 bx_cos(vec2 a){return clamp(abs(mod(a,8.0)-4.0)-2.0,-1.0,1.0);}
vec2 bx_cossin(float a){return bx_cos(vec2(a,a-2.0));}

// "hash11()" - "hash44()"
// Creative Commons Attribution-ShareAlike 4.0 International Public License
// Created by David Hoskins. May 2018
// https://www.shadertoy.com/view/XdGfRR
#include ../lib_modules/random/hash_def.glsl
#include ../lib_modules/random/hash11.glsl
#include ../lib_modules/random/hash12.glsl
#include ../lib_modules/random/hash13.glsl
#include ../lib_modules/random/hash21.glsl
#include ../lib_modules/random/hash22.glsl
#include ../lib_modules/random/hash23.glsl
#include ../lib_modules/random/hash33.glsl
#include ../lib_modules/random/hash32.glsl
#include ../lib_modules/random/hash31.glsl
#include ../lib_modules/random/hash43.glsl

// FBMs
#include ../lib_modules/noise/gnoise2D.glsl
#include ../lib_modules/noise/gnoise3D.glsl
#include ../lib_modules/fbm/fbmBase2D.glsl
#include ../lib_modules/fbm/gfbm2D.glsl

// Data packer/unpacker
// albedo, diffuse, specular, shadow, normal, and depth are rendered in raymarching pass,
// and then, those results packed in one vec4 to use in post processing.
// here are some experiments:
// https://www.shadertoy.com/view/Ws3cRS
#include ../lib_modules/data/packS3.glsl
#include ../lib_modules/data/unpackS3.glsl
#include ../lib_modules/data/packU3.glsl
#include ../lib_modules/data/unpackU3.glsl
#include ../lib_modules/data/packU4.glsl
#include ../lib_modules/data/unpackU4.glsl

// Smoothstep alternatives
// ---------------------------------------------------------------------
float sigmoidstep(float edge0, float edge1, float x, float contrast, float mid) {
  // https://www.shadertoy.com/view/3ssSz2
  x = smoothstep(edge0, edge1, x);
  float scale_l = (1. / mid) * x;
  float scale_h = (1. / (1. - mid)) - (1. / (1. - mid)) * x;
  float lower = mid * (scale_l * scale_l);
  float upper = 1. - (1. - mid) * (scale_h * scale_h);
  float curve = x < mid ? lower : upper;
  return mix(x, curve, (contrast - 1.));
}

float smoothbistep(float edge0, float edge1, float x, float smoothness) {
  float l = abs(edge0 - edge1) * smoothness * .5;
  return (edge0 < edge1) ? max(smoothstep(edge1 - l, edge1, x), smoothstep(edge0 + l, edge0, x)) : min(smoothstep(edge1 - l, edge1, x), smoothstep(edge0 + l, edge0, x));
}

float gainstep(float edge0, float edge1, float x, float k) {
  x = clamp((x - edge0) / (edge1 - edge0), 0., 1.);
  float a = .5 * pow(2. * ((x < .5) ? x : 1. - x), k);
  return (x < .5) ? a : 1. - a;
}

float sigmoidbistep(float edge0, float edge1, float x, float smoothness, float contrast, float mid) {
  float l = abs(edge0 - edge1) * smoothness * .5;
  return (edge0 < edge1) ? max(sigmoidstep(edge1 - l, edge1, x, contrast, mid), sigmoidstep(edge0 + l, edge0, x, contrast, mid)) : min(sigmoidstep(edge1 - l, edge1, x, contrast, mid), sigmoidstep(edge0 + l, edge0, x, contrast, mid));
}

float smoothsign(float x, float smoothness) {
  x = smoothstep(-smoothness, smoothness, x);
  return x * 2. - 1.;
}

vec2 smoothsign(vec2 x, float smoothness) {
  x = smoothstep(-smoothness, smoothness, x);
  return x * 2. - 1.;
}

vec3 smoothsign(vec3 x, float smoothness) {
  x = smoothstep(-smoothness, smoothness, x);
  return x * 2. - 1.;
}

// hermitian completion to both sides of an edge. easy to tinkering a mask.
float bismoothstep(float edge, float grad, float sat, float x) {
  grad *= .5, sat *= .5;
  return smoothstep(edge - sat - grad, edge - sat, x) *
         smoothstep(edge + sat + grad, edge + sat, x);
}

// just multailly 2 smoothsteps, but useful for masking an range.
float wsmoothstep(float edge0, float edge1, float edge2, float edge3, float x) {
  return smoothstep(edge0, edge1, x) * smoothstep(edge3, edge2, x);
}

// https://en.wikipedia.org/wiki/Smoothstep
float smootherstep(float edge0, float edge1, float x) {
  // Scale, and clamp x to 0..1 range
  x = clamp((x - edge0) / (edge1 - edge0), 0., 1.);
  // Evaluate polynomial
  return x * x * x * (x * (x * 6. - 15.) + 10.);
}

struct FBO {
  vec3 albedo;
  vec3 normal;
  float diffuse;
  float specular;
  float shadow;
  float ao;
  float depth;
  vec3 result;
};
FBO fbo;
FBO fboPre;

struct Ray {
  vec3 origin;
  vec3 progress;
  vec3 direction;
};

struct Camera {
  vec3 position;
  float orthoDist;
  vec3 direction;
  float orthoScale;
  vec3 target;
  float fov;
  vec4 quaternion;
  vec3 pivot;
  vec3 up;
  bool is_perspective;
};

struct Light {
  vec3 direction;
  float intensity;
  vec3 color;
  float shadowStart;
  float shadowEnd;
  float shadowSoft;
};

#define MIN_DIST @BL_HIT_DIST
#define MAX_DIST @BL_END_DIST
#define ITERATION @BL_MAX_STEPS
#define MAT_VOID vec3(-1)
@BL_MATERIAL_ID_DEC
bool isMaterial(vec3 MAT) {
    const float MAT_EPS = 1e-5;
    vec3 diff = fbo.albedo-MAT;
    return dot(diff,diff)<MAT_EPS*MAT_EPS;
}
void getMaterialParams(vec3 MAT, inout float specular, inout float roughness){
	@BL_MATERIAL_PARAMS
}

@BL_WORLD_PARAMS

#include ../bl_modules/bl_inc_trvs.glslinc
#include ../bl_modules/bl_inc_init.glslinc
#include ../bl_modules/bl_inc_camera.glslinc

vec2 pRot2(inout vec2 p, float a){
  p=cos(a)*p+sin(a)*vec2(p.y, -p.x);
  return p;
}

// https://suricrasia.online/demoscene/functions/
vec3 erot(vec3 p, vec3 ax, float ro) {return mix(dot(ax, p)*ax, p, cos(ro)) + cross(ax,p)*sin(ro);}
vec3 erotX(vec3 p, float ro){return erot(p, vec3(1,0,0), ro);}
vec3 erotY(vec3 p, float ro){return erot(p, vec3(0,1,0), ro);}
vec3 erotZ(vec3 p, float ro){return erot(p, vec3(0,0,1), ro);}

vec3 gBalloonCenter = vec3(0);

// IK structs and functions
struct IKBone{
    vec3 tail;
    float len;
    vec4 quat;
};

struct IKArmature{
    IKBone[3] bon;
    vec3 pol;
};

void calcIK(inout IKArmature ika){

    vec3 C = ika.bon[2].tail-ika.bon[0].tail;
    float lenC = length(C);

    // projection quaternion (2d to 3d)
    vec4 prjQuat = getQuat(AXIS_Y, C);

    // rotate the pole into the 2d space
    vec3 pol = ika.pol-ika.bon[0].tail;
    pRotQuat(pol, prjQuat*invQuat);

    // add roll rotation
    prjQuat = mulQuat(prjQuat, getQuat(C, PI-atan(pol.x,pol.z)));

    // calc ik in projected 2d space
    // ref about 2d ik:"Foundation ActionScript 3.0 Animation" P.367
    float lenA = ika.bon[1].len,
          lenB = ika.bon[2].len;
          lenC = min(lenA+lenB, lenC);
    float lenA2 = lenA*lenA,
          lenB2 = lenB*lenB,
          lenC2 = lenC*lenC;
    float angB = acos((lenB2-lenA2-lenC2)/(-2.*lenA*lenC)),
          angC = acos((lenC2-lenA2-lenB2)/(-2.*lenA*lenB)),
          angD = PI*.5,
          angD_B = angD+angB,
          angE = angB+angC+PI;
    ika.bon[1].tail = vec3(0,sin(angD_B),cos(angD_B))*lenA;

    // convert 2d bon[1].tail into original 3d space
    pRotQuat(ika.bon[1].tail, prjQuat);
    ika.bon[1].tail+=ika.bon[0].tail;

    // store quaternions
    ika.bon[0].quat = mulQuat(getQuat(AXIS_X,angB), prjQuat);
    ika.bon[1].quat = mulQuat(getQuat(AXIS_X,angE), prjQuat);

}

void pIKRig(inout vec3 p, IKBone bon){
  p += bon.tail;
  pRotQuat(p, bon.quat*invQuat);
}

// Read data from pre-pass
// ---------------------------------------------------------------------
#define getBuf(tex, coord) texelFetch(tex, ivec2(coord), 0)
vec3 getAlbedo(sampler2D tex, vec2 coord) { return unpackU4(getBuf(tex, coord).x).rgb; }
float getAO(sampler2D tex, vec2 coord) { return s2u(unpackS3(getBuf(tex, coord).y).b); }
float getShadow(sampler2D tex, vec2 coord) { return unpackU4(getBuf(tex, coord).x).a; }
float getDiffuse(sampler2D tex, vec2 coord) { float res = unpackS3(getBuf(tex, coord).y).r; return s2u(res);}
float getSpecular(sampler2D tex, vec2 coord) { return sat(unpackS3(getBuf(tex, coord).y).g); }
float getCloudData(sampler2D tex, vec2 coord) { return unpackS3(getBuf(tex, coord).y).g; }
float getDepth(sampler2D tex, vec2 coord) { return getBuf(tex, coord).w; }
vec3 getNormal(sampler2D tex, vec2 coord) { return normalize(unpackS3(getBuf(tex, coord).z)); }

void initFBO() {
  fbo = FBO(vec3(0), vec3(0), 0., 0., 0., 0., 0., vec3(0));
  fboPre = FBO(vec3(0), vec3(0), 0., 0., 0., 0., 0., vec3(0));
}

vec4 packFBO() {
  return vec4(
      packU4(vec4(fbo.albedo, fbo.shadow)),
      packS3(vec3(u2s(fbo.diffuse), fbo.specular, u2s(fbo.ao))),
      packS3(fbo.normal),
      fbo.depth
      );
}

void unpackFBO(inout FBO fbo, sampler2D tex, vec2 coord) {
  fbo.albedo = getAlbedo(tex, coord);
  fbo.shadow = getShadow(tex, coord);
  fbo.diffuse = getDiffuse(tex, coord);
  fbo.specular = getSpecular(tex, coord);
  fbo.ao = getAO(tex, coord);
	fbo.normal = getNormal(tex, coord);
  fbo.depth = getDepth(tex, coord);
}

#include ../lib_modules/noise/voronoiSmooth3D.glsl

// Voronoi displacement for Clouds
float vrn1 = 0.;
float vrn2 = 0.;
float vrn3 = 0.;
float vrn4 = 0.;
float vrn5 = 0.;
void calcVrn(vec3 p) {
  vrn1 = voronoiSmooth(p * .1, .1);
  float freq = .3;
  float smoothness = .01;
  vrn2 = (1. - voronoiSmooth(p * freq, smoothness * .5)) * .6;
  vrn3 = (1. - voronoiSmooth(p * freq * 2., smoothness * .5)) * .25;
  vrn4 = (1. - voronoiSmooth(p * freq * 4., smoothness * .5)) * .15;
  vrn5 = (1. - voronoiSmooth(p * freq * 16., smoothness * .5)) * .035;
}

// "SphericalFibonacci" by EvilRyu:
// https://www.shadertoy.com/view/dsjXDm
const float gNum = 16.;
// from http://gec.di.uminho.pt/psantos/Publications_ficheiros/SF_CGF2013.pdf
// unoptimized version
// j: index of the point to generate
vec3 sphericalFibonacci(float j){
    float phi = 2. * PI * j * (2. / (3. - sqrt(5.)));
    float theta = acos(1. - 2. * j / gNum);
    return vec3(sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta));
}

// https://iquilezles.org/articles/intersectors
vec2 iBox(vec3 ro, vec3 rd, vec3 size){
    vec3 m = 1./rd;
    vec3 n = m*ro;
    vec3 k = abs(m)*size;
    vec3 t1 = -n-k;
    vec3 t2 = -n+k;
    float tN = max(max(t1.x,t1.y),t1.z);
    float tF = min(min(t2.x,t2.y),t2.z);
    if(tN>tF||tF<0.) return vec2(-1);
    return vec2(tN,tF);
}

int getDigits(float f, int digc, int index) {
    f = f * pow(10., float(digc + index*digc));
    return int(f) % int(pow(10., float(digc)));
}

bool inRange(float v, float min, float max) {
    return v > min && v < max;
}

bool inRange(int v, int min, int max) {
    return v > min && v < max;
}

float vmax(vec3 v){
    return max(v.x, max(v.y,v.z));
}

#define CELL_SIZE vec3(10)
vec3 gCurrentCell = vec3(0);
vec3 getCell(vec3 p){
    return vec3(floor(p/CELL_SIZE)*CELL_SIZE);
}
