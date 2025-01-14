
mat2 rot2d(float a) {
  return mat2(cos(a), sin(a), -sin(a), cos(a));
}

float sdFinger(vec3 p, vec2 baseSize, vec4 frot) {
  float min_mix = .001;
  float base_mix = baseSize.x * 2.7;
  const float MAX_ROT = PI * .5;
  frot *= MAX_ROT;

  // anchor points
  vec3 p0 = p;
  p0.yx *= rot2d(-frot.w);
  p0.yz *= rot2d(-frot.x);

  vec3 p1 = p0 - vec3(0, baseSize.y * 1.166 * 2., 0);
  p1.yz *= rot2d(-frot.y);

  vec3 p2 = p1 - vec3(0, baseSize.y * 2., 0);
  p2.yz *= rot2d(-frot.z);

  float dRoot = sdEllipsoid(p0 - vec3(0, baseSize.y * .6, 0), baseSize.xyx * vec2(1., 1.1).xyx);
  float dFin0 = sdEllipsoid(p0 - vec3(0, baseSize.y * 1.166, 0), baseSize.xyx * vec2(1., 1.15).xyx);
  dFin0 = bUniS(dFin0, dRoot, .05);
  float dFin1 = sdEllipsoid(p1 + vec3(0, -baseSize.y * 1.15, 0), baseSize.xyx * vec2(.9, 1.1).xyx);
  float dFin2 = sdEllipsoid(p2 + vec3(0, -baseSize.x * 1.5, 0), baseSize.xxx * 1.15);

  // combine all
  float d = bUniS(dFin0, dFin1, base_mix * .9 + min_mix);
  d = bUniS(d, dFin2, base_mix * 1.05 + min_mix);

  return d;
}

float sdPalm(vec3 p) {
  float d = sdEllipsoid(p, vec2(0.17, .1).xxy);
  d = bSubS(sdEllipsoid(p + vec3(-.1, 0, .17), vec2(0.17, .1).xxy), d, .1);
  return d;
}

float sdHand(vec3 p, vec4 frot0, vec4 frot1, vec4 frot2, vec4 frot3) {
  float bdr = .6;
  float bd = length(p - vec3(0, .25, 0));
  if (bd > 2.*bdr) return bd-bdr;

  p.y -= .27;
  p.x -= .09;
  vec2 baseSize = vec2(.175, .25);
  float winkleStart = 2.;

  // anchor points
  vec3 p0 = p;
  p0 += vec3(-.0, .13, .05);
  pRot(p0, vec3(-.75, -1.5, .75));

  vec3 p1 = p;
  p1 += vec3(0, 0, 0);
  pRot(p1, vec3(0, 0, .25));

  vec3 p2 = p;
  p2 += vec3(.1, -.015, 0);
  pRot(p2, vec3(0, 0, 0));

  vec3 p3 = p;
  p3 += vec3(.19, 0, 0);
  pRot(p3, vec3(0, 0, -.25));

  // combine all
  float d = sdPalm(p + vec3(.09, .1, 0));
  vec2 scale = vec2(.9, 1.);
  d = bUniS(d, sdFinger(p0, vec2(0.039, .06) * scale, frot0 * .9), .001 + .25 * smoothstep(.2, .0, length(p0)));
  d = bUniS(d, sdFinger(p1, vec2(0.036, .07) * scale, frot1 * .75), .001 + .065 * smoothstep(.2, .1, length(p1)));
  d = bUniS(d, sdFinger(p2, vec2(0.036, .07) * scale, frot2 * .8), .001 + .065 * smoothstep(.2, .1, length(p2)));
  d = bUniS(d, sdFinger(p3, vec2(0.0325, .0625) * scale, frot3 * .8), .001 + .06 * smoothstep(.2, .1, length(p3)));

  return d;
}
