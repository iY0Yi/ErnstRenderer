#if IS_EDITING_TRVS
TRVsID = iFrame;
#endif
vec4 frot0, frot1, frot2, frot3;
vec3 rootPos, rootRot;
if(TRVsID == 0) {
  frot0 = vec4(-.0, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .425, .4, -.05);
  rootPos = vec3(0, .02, 0), rootRot = vec3(-.21, .1, .1);
}
if(TRVsID == 1) {
  frot0 = vec4(-.0, .0, -.25, -.25);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .02, -.01), rootRot = vec3(-.25, -.2, .03);
}
if(TRVsID == 2) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, 1.2, -.2, -.15);
  frot2 = vec4(-.1, 1.2, -.2, .0);
  frot3 = vec4(.0, 1.2, -.2, .25);
  rootPos = vec3(0, .0, 0), rootRot = vec3(.1, 0, 0);
}
if(TRVsID == 3) {
  frot0 = vec4(-.15, .0, -.25, -.35);
  frot1 = vec4(.0, 1.25, .2, -.15);
  frot2 = vec4(.0, 1.25, .2, -.17);
  frot3 = vec4(.1, .85, .4, -.05);
  rootPos = vec3(0, .04, -.0025), rootRot = vec3(-.15, 0, -.1);
}
if(TRVsID == 4) {
  frot0 = vec4(.1, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .04, 0), rootRot = vec3(-.21, .1, .1);
}
if(TRVsID == 5) {
  frot0 = vec4(.0, .0, -.25, -.2);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(-.1, .6, .4, -.05);
  rootPos = vec3(0, .04, 0), rootRot = vec3(-.2, .0, -.1);
}
if(TRVsID == 6) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .5, -.2, -.15);
  frot2 = vec4(-.1, .5, -.2, .0);
  frot3 = vec4(.0, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(0, 0, 0);
}
if(TRVsID == 7) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .5, -.2, -.15);
  frot2 = vec4(-.1, .5, -.2, .0);
  frot3 = vec4(.0, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(0, 0, .2);
}
if(TRVsID == 8) {
  frot0 = vec4(-.175, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, .85, .2, -.17);
  frot3 = vec4(-.2, .5, .4, -.25);
  rootPos = vec3(0, .04, 0), rootRot = vec3(-.2, .0, .2);
}
if(TRVsID == 9) {
  frot0 = vec4(.1, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .04, 0), rootRot = vec3(-.2, .0, .1);
}
if(TRVsID == 10) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .5, -.2, -.15);
  frot2 = vec4(-.1, .5, -.2, .0);
  frot3 = vec4(.0, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(0, 0, 0);
}
if(TRVsID == 11) {
  frot0 = vec4(-.0, .0, -.25, -.25);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, -.005, -.005), rootRot = vec3(-.21, -.1, -.075);
}
if(TRVsID == 12) {
  frot0 = vec4(-.0, .0, -.25, -.25);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .02, -.01), rootRot = vec3(-.25, -.2, .03);
}
if(TRVsID == 13) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .25, -.2, -.15);
  frot2 = vec4(-.1, .25, -.2, .0);
  frot3 = vec4(.0, .25, -.2, .25);
  rootPos = vec3(0, .035, 0), rootRot = vec3(-.45, 0, 0);
}
if(TRVsID == 14) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .5, -.2, -.15);
  frot2 = vec4(-.1, .5, -.2, .0);
  frot3 = vec4(.0, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(-.5, 0, 0.);
}
if(TRVsID == 15) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .5, -.2, -.15);
  frot2 = vec4(-.1, .5, -.2, .0);
  frot3 = vec4(.0, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(0, 0, 0);
}
trp -= rootPos;
trp = rot(trp, rootRot* PI * .5);
td = sdHand(trp * 2., frot0, frot1, frot2, frot3) * .5;
