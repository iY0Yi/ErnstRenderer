#include bl_modules/bl_inc_common.glslinc

// Color modifiers
// ---------------------------------------------------------------------
#include lib_modules/colorgrading/sigmoid_contrast.glsl
#include lib_modules/tonemapping/lottes.glsl
vec3 rgb2hsv(vec3 c) {
  vec4 K = vec4(0,-1./3.,2./3.,-1);
  vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
  vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
  float d = q.x - min(q.w, q.y);
  float e = 1e-10;
  return vec3(abs(q.z + (q.w - q.y) / (6. * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1,2./3.,1./3.,3);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6. - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0., 1.), c.y);
}

vec3 modHSV(vec3 rgb, float h, float s, float v) {
  vec3 hsv = rgb2hsv(rgb);
  hsv.x += h;
  hsv.y += s;
  hsv.z += v;
  hsv.yz = sat(hsv.yz);
  return hsv2rgb(hsv);
}

// Curvature
// ---------------------------------------------------------------------
// "Screen Space Curvature Shader" by Evan Wallace:
// http://madebyevan.com/shaders/curvature/
vec2 calcCurvature(vec3 n, vec2 fragCoord, vec2 f) {
  vec3 dx = getNormal(fragCoord + vec2(-1, 0)) - getNormal(fragCoord + vec2(+1, 0));
  vec3 dy = getNormal(fragCoord + vec2(0, -1)) - getNormal(fragCoord + vec2(0, +1));
  vec3 difx = cross(n + dx, n - dx);
  vec3 dify = cross(n + dy, n - dy);
  float dif = difx.y - dify.x;
  return clamp(vec2(dif, -dif) * f, 0., 1.);
}

// Edges
// ---------------------------------------------------------------------
float calcEdge(vec3 nlm1, vec3 nlm2) {
  vec2 difN = abs(nlm1.xy - nlm2.xy);
  float base = .5;
  return smoothstep(base + .025, base, difN.x + difN.y);
}

float getOutline(vec2 coord) {
#define NM(x) getNormal(x)
  vec2 coords = coord;
  vec2 rcoord = coord;
#ifdef HD
  rcoord += prGridIds * iResolution.xy;
#endif
  vec3 offset = vec3(1, -1, 0) * .5;
  float edge = 1.;
  edge *= calcEdge(NM(clampCoord(coords + offset.xx)), NM(clampCoord(coords + offset.yy)));
  edge *= calcEdge(NM(clampCoord(coords + offset.xy)), NM(clampCoord(coords + offset.yx)));
  edge *= calcEdge(NM(clampCoord(coords + offset.zy)), NM(clampCoord(coords + offset.zx)));
  edge *= calcEdge(NM(clampCoord(coords + offset.yz)), NM(clampCoord(coords + offset.xz)));
  return edge;
}

// ref: (in japanese)
// https://imagingsolution.net/imaging/canny-edge-detector/
#define shatick 1.
// Detect edge.
vec4 sobel(vec2 fragCoord, vec2 dir, bool isDiffuse) {
  float np, zp, pp, nz, pz, nn, zn, pn;
  if (isDiffuse){
    np = getDiffuse(clampCoord(fragCoord + (vec2(-1, +1) + dir) * shatick));
    zp = getDiffuse(clampCoord(fragCoord + (vec2(0, +1) + dir) * shatick));
    pp = getDiffuse(clampCoord(fragCoord + (vec2(+1, +1) + dir) * shatick));
    nz = getDiffuse(clampCoord(fragCoord + (vec2(-1, 0) + dir) * shatick));
    pz = getDiffuse(clampCoord(fragCoord + (vec2(+1, 0) + dir) * shatick));
    nn = getDiffuse(clampCoord(fragCoord + (vec2(-1, -1) + dir) * shatick));
    zn = getDiffuse(clampCoord(fragCoord + (vec2(0, -1) + dir) * shatick));
    pn = getDiffuse(clampCoord(fragCoord + (vec2(+1, -1) + dir) * shatick));
  }else{
    np = getShadow(clampCoord(fragCoord + (vec2(-1, +1) + dir) * shatick));
    zp = getShadow(clampCoord(fragCoord + (vec2(0, +1) + dir) * shatick));
    pp = getShadow(clampCoord(fragCoord + (vec2(+1, +1) + dir) * shatick));
    nz = getShadow(clampCoord(fragCoord + (vec2(-1, 0) + dir) * shatick));
    pz = getShadow(clampCoord(fragCoord + (vec2(+1, 0) + dir) * shatick));
    nn = getShadow(clampCoord(fragCoord + (vec2(-1, -1) + dir) * shatick));
    zn = getShadow(clampCoord(fragCoord + (vec2(0, -1) + dir) * shatick));
    pn = getShadow(clampCoord(fragCoord + (vec2(+1, -1) + dir) * shatick));
  }
#if 0
	float gx = (np * -1. + nz * -2. + nn * -1. + pp * 1. + pz * 2. + pn * 1.);
	float gy = (np * -1. + zp * -2. + pp * -1. + nn * 1. + zn * 2. + pn * 1.);
#else
  // https://www.shadertoy.com/view/Wds3Rl
  float gx = (np * -3. + nz * -10. + nn * -3. + pp * 3. + pz * 10. + pn * 3.);
  float gy = (np * -3. + zp * -10. + pp * -3. + nn * 3. + zn * 10. + pn * 3.);
#endif
  vec2 G = vec2(gx, gy);
  float grad = length(G);
  float angle = atan2(G.y, G.x);
  return vec4(G, grad, angle);
}

// Make edge thinner.
vec2 hysteresisThr(vec2 fragCoord, float mn, float mx, bool isDiffuse) {
  vec4 edge = sobel(fragCoord, vec2(0), isDiffuse);
  vec2 dir = vec2(cos(-edge.w), sin(-edge.w));
  vec4 edgep = sobel(fragCoord, dir, isDiffuse);
  vec4 edgen = sobel(fragCoord, -dir, isDiffuse);
  if(edge.z < edgep.z || edge.z < edgen.z) edge.z = 0.;
  return vec2((edge.z > mn) ? edge.z : 0., (edge.z > mx) ? edge.z : 0.);
}

float cannyEdge(vec2 fragCoord, float mn, float mx, bool isDiffuse) {
  vec2 np = hysteresisThr(fragCoord + vec2(-1, +1), mn, mx, isDiffuse);
  vec2 zp = hysteresisThr(fragCoord + vec2(0, +1), mn, mx, isDiffuse);
  vec2 pp = hysteresisThr(fragCoord + vec2(+1, +1), mn, mx, isDiffuse);
  vec2 nz = hysteresisThr(fragCoord + vec2(-1, 0), mn, mx, isDiffuse);
  vec2 zz = hysteresisThr(fragCoord + vec2(0, 0), mn, mx, isDiffuse);
  vec2 pz = hysteresisThr(fragCoord + vec2(+1, 0), mn, mx, isDiffuse);
  vec2 nn = hysteresisThr(fragCoord + vec2(-1, -1), mn, mx, isDiffuse);
  vec2 zn = hysteresisThr(fragCoord + vec2(0, -1), mn, mx, isDiffuse);
  vec2 pn = hysteresisThr(fragCoord + vec2(+1, -1), mn, mx, isDiffuse);
  return 1.-min(1., step(1e-3, zz.x * 8.) * smoothstep(.0, .1, np.y + zp.y + pp.y + nz.y + pz.y + nn.y + zn.y + pn.y) * 8.);
}

// Dithering
// ---------------------------------------------------------------------
float dithering(float v, vec2 coord) {
  if(renDat.depth > .999) return 1.;
  v = TonemapLottes(v);
  v = pow(v, .4545);
  v = pow(v, 1.);
  vec2 p = coord;
  p = mod(p.xx + vec2(p.y, -p.y), vec2(.1));
  float res = 0.;
  vec2 coords = coord;
  float angle = dot(getNormal(coord), vec3(0, 0, 1));
  float rand_ditherVal = gfbm((coords * 1.), 1, .5);
  const float paletteDist = .5;
  res = v + (rand_ditherVal - .5) * paletteDist;
  res = sat(floor(res * 7.) / 6.);
  return res;
}

float dottyDithering(float shadow, vec2 fragCoord, bool needOffset) {
  vec2 coord = fragCoord;
  vec2 rcoord = coord;
#ifdef HD
  rcoord += prGridIds * iResolution.xy;
#endif
  if(needOffset) R(rcoord, PI * .28);
  rcoord = mod(rcoord * .3, 1.);
  float res = 0.;
  shadow = 1. - shadow;
  res = smoothstep(shadow, 1., pow(length(rcoord - .5), 1.));
  res = smoothstep(.0, .3, pow(res, .5));
  return res;
}

// Hatching
// ---------------------------------------------------------------------
float hatching(float shading, vec2 coord, float tickness, float angle) {
  vec2 rcoord = coord;
#ifdef HD
  rcoord += prGridIds * iResolution.xy;
#endif

  vec2 v = coord.xy;
  vec3 n = normalize(getNormal(coord));
  // n.x += u2s(gnoise(coord * .5)) * .075;
  // n.y += u2s(gnoise(coord.yx * .5)) * .075;
  n = normalize(n);

  const float div = 36.;
  float a = s2u(dot(n, normalize(vec3(1, 1, 0))));
  a = floor(a * div) / div;
  R(v, PI * .25 * (a));
  R(v, angle);

  v.y = mod(v.y + float(int(floor(a * div)) % 2), tickness) - .5 * tickness;
  v.y *= shading;
  float line = mix(abs(v.y), 1., shading);
  line = smoothstep(.85, 1., line);
  return line;
}

float getHatching(float shading, vec2 coord) {
  float ln = 1.;
  const float tickness = 3.5;
  const float power = .25;

  const float mul = 1.;
  ln *= pow(hatching(shading, coord, tickness, PI * .125), power);
  ln *= pow(hatching(shading, coord, tickness, PI * -.125), power);
  ln = smoothstep(.0, .9, ln);
  return ln;
}

#include lib_modules/shading/orennayar.glsl
#include lib_modules/shading/blinnphong.glsl
// ---------------------------------------------------------------------
void mainImage( out vec4 fragColor, in vec2 fragCoord ){
  fragCoord /= ERNST_RENDER_SCALE;

  vec2 uv = fragCoord.xy / iResolution.xy;
  vec2 cuv = uv;
  float ml = (min(iResolution.x, iResolution.y) == iResolution.x) ? 1. : iResolution.y / iResolution.x;
  cuv = (cuv * 2. - 1.) * ml;
  cuv.x *= iResolution.x / iResolution.y;
  init();
  camera(cuv);
  unpackRenderData(fragCoord);

  vec2 rcoord = fragCoord;
#ifdef HD
  rcoord += prGridIds * iResolution.xy;
#endif
	vec3 dbg = vec3(0);
  vec3 col = vec3(0.9608, 0.9216, 0.8431);

  vec2 distortedCoord = fragCoord;
  distortedCoord += u2s(gfbm((fragCoord * .025), 1, .5)) * 6.;
  distortedCoord += u2s(gfbm((fragCoord.yx * .05), 1, .5)) * 6.;
  distortedCoord = clampCoord(distortedCoord);
  vec3 albedo = getAlbedo(distortedCoord);
  if(bool(step(.05, distance(albedo, renDat.albedo)))) {
    albedo = albedo * renDat.albedo;
    albedo = modHSV(albedo, 0., .025, -.05);
  }

  float dMeter = renDat.depth * MAX_DIST;
  float dMeterToZero = length(cam0.position);
  float dMeterMaxFogRange = MAX_DIST - dMeterToZero;
  float dMeterFog = max(0., dMeter - dMeterToZero);
  float fogDamp = dMeterFog / dMeterMaxFogRange;
  fogDamp = pow(fogDamp, .5);
  const float FOG_DENSITY = .8;

  float outlineFog = smoothstep(.1,.9,gfbm(rcoord * .3, 3, .5)*fogDamp*.75);
#define lighten .1 + .9 *

	// Hatching
	float hatchsha, hatchind;
	float roughness = 1.;
	hatchsha = sat(u2s(renDat.diffuse));
	hatchind = sat(u2s(renDat.diffuse) * -1.);

	// hatchsha = orenNayarDiffuse(lit0.direction, ray.direction, renDat.normal, roughness) * 1.7;
	// float hatchind = orenNayarDiffuse(-lit0.direction, ray.direction, renDat.normal, roughness);
	hatchsha *= getShadow(fragCoord);
	hatchsha += pow(hatchind, 1.) * 1.2;
	hatchsha += pow(getAO(fragCoord), .25) * 1.2;
	hatchsha = sat(TonemapLottes(hatchsha));

	hatchsha = mix(hatchsha, gfbm(rcoord * .01, 3, .5), .04 + pow(linearstep(.8, 1., hatchsha), 1.) * .065);
	hatchsha = pow(hatchsha, 1.275);
	vec2 curvature = calcCurvature(renDat.normal, fragCoord, vec2(.5, 2.));
	float dented = smoothstep(3.5, 0., curvature.y);
	float bumped = smoothstep(0., 1., curvature.x);
	hatchsha += 1. - linearstep(.1, .7, getShadow(fragCoord));
	hatchsha = sat(hatchsha);
	col *= lighten sat(getHatching(hatchsha, fragCoord) + outlineFog);
	// dbg = vec3(getHatching(hatchsha, fragCoord));

	// Outlines
	// col *= lighten sat(getOutline(fragCoord) + outlineFog);
	// col *= lighten sat(max(cannyEdge(fragCoord, 12., 18., false), 1. - smoothstep(.1, .3, sat(u2s(renDat.diffuse)))) + outlineFog);

	// Additional edge drawing for winkles
	bool needWrinkleLine = false;
	needWrinkleLine = needWrinkleLine && dithering(gfbm(fragCoord.yx * .1, 2, .5), fragCoord) > .5;
	distortedCoord = fragCoord;
	distortedCoord.x += u2s(gfbm((fragCoord.xx * .05), 2, .5)) * 8.;
	distortedCoord.y += u2s(gfbm((fragCoord.yx * .05), 2, .5)) * 8.;
	distortedCoord = clampCoord(distortedCoord);
	// if(needWrinkleLine) col *= cannyEdge(distortedCoord, 2., 2.5, true);

	// Calc base shading and indirect
	float shading = sat(u2s(renDat.diffuse));
	shading *= renDat.shadow + pow(renDat.ao, 1.5) * .5;
	shading = smoothstep(0., 1.5, shading);
	shading = TonemapLottes(shading);
	float indirect = sat(u2s(renDat.diffuse) * -1.);

	// Base dithering
	float dithsha = sat(u2s(renDat.diffuse)) * 1.5;
	dithsha *= renDat.shadow + renDat.ao * .5 + indirect * .5;
	dithsha += .125;
	dithsha = TonemapLottes(dithsha);
	col *= lighten linearstep(.0, .9, dithering(dithsha, fragCoord));
	// Dithering for indirect
	float dithindirect = 1. - (indirect + pow(renDat.ao, .5) * .3);
	dithindirect = linearstep(.0, 1., dithindirect);
	// col *= lighten linearstep(.0, .85, dithering(dithindirect, fragCoord));

	// Dithering for AO in lighter area
	float dithao = pow(renDat.ao, .5);
	dithao = linearstep(-.1, .8, dithao);
	dithao += 1. - renDat.shadow;
	// col *= lighten linearstep(.0, .9, dithering(dithao, fragCoord));

	dithao = pow(renDat.ao, .5);
	dithao = smoothstep(.0, 1., dithao);
	dithao += renDat.shadow;
	dithao += smoothstep(0., 1., curvature.x) * .25;
	dithao += .025;
	dithao = TonemapLottes(dithao);
	// col *= lighten linearstep(.0, .99, dithering(dithao, fragCoord));

	// Dithering for dented curvature
	float dithdented = pow(dented, 1.);
	dithdented = linearstep(.0, 1., dithdented);
	dithdented += renDat.shadow;
	// col *= lighten linearstep(.0, .9, dithering(dithdented, fragCoord));

	// Shadow
	float shadow = sat(renDat.shadow + .7);
	col *= lighten sat(dottyDithering(shadow, fragCoord, true) + outlineFog);
	col *= renDat.shadow * .7 + pow(renDat.ao, 1.) * .25+.05;

	// Draw Ridge.
	float dithridge = abs(u2s(renDat.diffuse));
	// dithridge = pow(dithridge, .);
	dithridge = linearstep(.0, 1., dithridge);
	// col *= lighten sat(getHatching(smoothstep(-.9, .9, dithridge+.2), fragCoord) + outlineFog);

	// Draw Ridge on self shadow edge.
	dithridge = abs(u2s(renDat.diffuse)+.0);
	dithridge = linearstep(.0, .3, dithridge)+.65;
	dithridge += 1.-smoothstep(.0, .1, renDat.shadow);
	dithridge = sat(dithridge);
	// col *= lighten sat(getHatching(dithridge, fragCoord) + outlineFog);

	vec3 hsv = rgb2hsv(albedo);
	float threshold = smoothstep(.5, .9, shading);
	// hsv.y += threshold * .1;
	// hsv.z *= threshold * .025 + .975;
	albedo = hsv2rgb(hsv);


  float dithlight, dithlight2;
	dithlight = smoothstep(.95, 1., sat(u2s(renDat.diffuse)) * renDat.shadow + pow(renDat.ao, 1.5) * .5);
	dithlight2 = smoothstep(.85, .9, sat(u2s(renDat.diffuse)) * renDat.shadow + pow(renDat.ao, 1.5) * .5);
	// albedo += (1. - dithering(1. - dithlight, fragCoord)) * .0125;
	// albedo += (1. - dithering(1. - dithlight2, fragCoord)) * .0125;

  distortedCoord = fragCoord * .00125 + 4.;
  distortedCoord = clampCoord(distortedCoord);
  float tint = gfbm(distortedCoord, 2, .5);
  albedo = modHSV(albedo, 0., smoothstep(.3, .7, tint) * .05, -tint * .05);
  albedo = modHSV(albedo, 0., -(1. - renDat.shadow) * .05, 0.);

  col *= albedo;

  float spec = renDat.specular;
  col += dithering(smoothstep(.0, 1., spec), fragCoord) * renDat.shadow * (1.-outlineFog);

  col = mix(sat(col), FOG_COL, fogDamp * FOG_DENSITY);

  col *= dithering(.75 + .25 * smoothstep(.0, 1., gfbm(fragCoord.yx * .02, 2, .5)), fragCoord);
  col *= sms(.5, .501, (gnoise((fragCoord * .18)) + gnoise((fragCoord * .15)) + .3));
  col += 1. - sms(.5, .501, ((1. - gnoise(fragCoord * .1) * gnoise(fragCoord * .1)) + .7));

  col = clamp(col, 0., 1.);
  col = TonemapLottes(col);
  col = pow3(col, .45);
  fragColor = vec4(col, 1.);
  // fragColor = vec4(vec3(1,0,0), 1.);
}
