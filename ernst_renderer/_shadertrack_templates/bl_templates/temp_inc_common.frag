
@BL_UNIFORMS
@BLU_GUI
@CANVAS_MODE
#define ERNST_RENDER_SCALE float(@BL_RESOLUTION_SCALE)
#define INV_ERNST_RENDER_SCALE (1. / ERNST_RENDER_SCALE)

#define PI acos(-1.)
#define TAU (PI * 2.)
#define sat(x) clamp(x, 0., 1.)
#define sms(min, max, x) smoothstep(min, max, x)
#define s2u(x) (x * .5 + .5)
#define u2s(x) ((x * 2.) - 1.)
#define sign1f(x) ((x > 0.) ? 1. : -1.)
#define sign2v(v) vec2(sign1f(v.x), sign1f(v.y))
#define linearstep(edge0, edge1, x) min(max((x - (edge0)) / ((edge1) - (edge0)), 0.), 1.)
// https://stackoverflow.com/questions/26070410/robust-atany-x-on-glsl-for-converting-xy-coordinate-to-angle
#define atan2(y, x) ((abs(x) > abs(y)) ? PI * .5 - atan(x, y) : atan(y, x))
// normalized atan.
float natan(float y, float x) {return atan2(y, x) / acos(-1.) * .5 + .5;}
vec2 pow2(vec2 v, float power){return pow(v, vec2(power));}
vec3 pow3(vec3 v, float power){return pow(v, vec3(power));}
float sabs(float x,float k) {float a = (.5/k)*x*x+k*.5; float b = abs(x); return b<k ? a : b;}

// "hash11()" - "hash44()"
// "Hash without Sine" by Dave_Hoskins:
// https://www.shadertoy.com/view/4djSRW
#include ../lib_modules/random/hash11.glsl
#include ../lib_modules/random/hash12.glsl
#include ../lib_modules/random/hash13.glsl
#include ../lib_modules/random/hash21.glsl
#include ../lib_modules/random/hash22.glsl
#include ../lib_modules/random/hash33.glsl
#include ../lib_modules/random/hash32.glsl
#include ../lib_modules/random/hash31.glsl
#include ../lib_modules/random/hash43.glsl

// FBMs
#include ../lib_modules/noise/gnoise2D.glsl
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

struct RenderData {
  vec3 albedo;
  vec3 normal;
  float diffuse;
  float specular;
  float shadow;
  float ao;
  float depth;
  vec3 result;
};
RenderData lastDat;
RenderData renDat;

struct Ray {
  vec3 origin;
  vec3 progress;
  vec3 direction;
};

struct Camera {
  vec3 position;
  vec3 direction;
  vec3 target;
  vec3 pivot;
  vec4 quaternion;
  bool is_perspective;
  float fov;
  float orthoDist;
  float orthoScale;
  vec3 up;
};

struct Light {
  vec3 direction;
  vec3 color;
  float intensity;
  float shadowStart;
  float shadowEnd;
  float shadowSoft;
};

#define MAT_VOID vec3(-1)
@BL_MATERIAL_ID_DEC
bool isMaterial(vec3 MAT) { return distance(renDat.albedo, MAT) < .005; }
void getMaterialParams(vec3 MAT, inout float specular, inout float roughness){
	@BL_MATERIAL_PARAMS
}

@BL_WORLD_PARAMS

#define MIN_DIST @BL_HIT_DIST
#define MAX_DIST @BL_END_DIST
#define ITERATION @BL_MAX_STEPS

#include ../bl_modules/bl_inc_init.glslinc
#include ../bl_modules/bl_inc_camera.glslinc


// https://suricrasia.online/demoscene/functions/
vec3 erot(vec3 p, vec3 ax, float ro) {return mix(dot(ax, p)*ax, p, cos(ro)) + cross(ax,p)*sin(ro);}
vec3 erotX(vec3 p, float ro){return erot(p, vec3(1,0,0), ro);}
vec3 erotY(vec3 p, float ro){return erot(p, vec3(0,1,0), ro);}
vec3 erotZ(vec3 p, float ro){return erot(p, vec3(0,0,1), ro);}

// Structs for IK
struct IKBone{ vec3 tail; float len; float yaw; float pitch;};
struct IKArmature{IKBone[3] bon; vec3 pol;};

float signed_angle(vec3 vector_u, vec3 vector_v, vec3 normal){
    // Normal specifies orientation
    float angle = acos(dot(vector_u, vector_v));
    vec3 sgnv = (cross(vector_u, vector_v));
    if(acos(dot(sgnv, normal)) < 1.) angle = -angle;
    return angle;
}

// https://blender.stackexchange.com/a/19755
float getPoleAngle(IKBone ikBone, vec3 poleLoc){
    vec3 poleNormal = normalize(cross(ikBone.tail, poleLoc));
    vec3 projectedPoleAxis = normalize(cross(poleNormal, ikBone.tail));
    vec3 xAxis = erotY(vec3(-1,0,0), ikBone.yaw);
    return PI*.5+PI-signed_angle(xAxis, projectedPoleAxis, ikBone.tail);
}

// Ref:"Foundation ActionScript 3.0 Animation" P.367
// Ref: https://www.alanzucconi.com/2020/09/14/inverse-kinematics-in-3d/
void calcIK(inout IKArmature ika){
  float yaw = atan((ika.bon[2].tail.x),ika.bon[2].tail.z)+PI;
  if(mod(atan((ika.bon[2].tail.y),(ika.bon[2].tail.x)),PI)-mod(atan((ika.pol.y),(ika.pol.x)),PI)>0. && ika.bon[2].tail.x<0. && ika.bon[2].tail.y<0.)yaw+=PI;
  if(mod(atan((ika.bon[2].tail.y),(ika.bon[2].tail.x)),PI)-mod(atan((ika.pol.y),(ika.pol.x)),PI)<0. && ika.bon[2].tail.x>0. && ika.bon[2].tail.y<0.)yaw+=PI;

  ika.bon[2].tail = erotY(ika.bon[2].tail,-yaw);
  // length of edges.
  float eA = ika.bon[1].len,
        eB = ika.bon[2].len,
        eC = min(eA+eB, length(ika.bon[2].tail));
  // angles.
  float aB = acos((eB*eB-eA*eA-eC*eC)/(-2.*eA*eC)), // low of cosines
        aC = acos((eC*eC-eA*eA-eB*eB)/(-2.*eA*eB)), // low of cosines
        aD = atan(ika.bon[2].tail.z, ika.bon[2].tail.y),
        aE = aD+aB+PI+aC;
  float aDB = -(aD+aB)+PI*.5;
  // solved joint position on "YZ" 2d plane.
  ika.bon[1].tail = vec3(0,cos(aD+aB),sin(aD+aB))*eA;
  // inverse rotation to make it into original 3d space.
  ika.bon[1].tail = erotY(ika.bon[1].tail,yaw);
  ika.bon[2].tail = erotY(ika.bon[2].tail,yaw);
  // store angles into bone sturucts.
  ika.bon[0].pitch = aD+aB, ika.bon[1].pitch = aE;
  ika.bon[0].yaw = ika.bon[1].yaw = ika.bon[2].yaw = yaw;


}

void pIKRig(inout vec3 p, IKBone b){
  p += b.tail;
  p = erotY(p, -b.yaw);
  p = erotX(p, -b.pitch);
}


// Read data from pre-pass
// ---------------------------------------------------------------------
#define getBuf(coord) texelFetch(iChannel0, ivec2(coord), 0)
// #define getBuf(coord) texture(iChannel0, coord/iResolution.xy)
vec3 getAlbedo(vec2 coord) { return unpackU4(getBuf(coord).x).rgb; }
float getAO(vec2 coord) { return s2u(unpackS3(getBuf(coord).y).b); }
float getShadow(vec2 coord) { return unpackU4(getBuf(coord).x).a; }
float getDiffuse(vec2 coord) { float res = unpackS3(getBuf(coord).y).r; return s2u(res);}
float getSpecular(vec2 coord) { return sat(unpackS3(getBuf(coord).y).g); }
float getCloudData(vec2 coord) { return unpackS3(getBuf(coord).y).g; }
float getDepth(vec2 coord) { return getBuf(coord).w; }
vec3 getNormal(vec2 coord) { return normalize(unpackS3(getBuf(coord).z)); }

void unpackRenderData(vec2 coord) {
  renDat.albedo = getAlbedo(coord);
  renDat.shadow = getShadow(coord);
  renDat.diffuse = getDiffuse(coord);
  renDat.specular = getSpecular(coord);
  renDat.ao = getAO(coord);
	renDat.normal = getNormal(coord);
  renDat.depth = getDepth(coord);
}

void unpackLastData(vec2 coord) {
  lastDat.albedo = getAlbedo(coord);
  lastDat.shadow = getShadow(coord);
  lastDat.diffuse = getDiffuse(coord);
  lastDat.specular = getSpecular(coord);
  lastDat.ao = getAO(coord);
	lastDat.normal = getNormal(coord);
  lastDat.depth = getDepth(coord);
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
