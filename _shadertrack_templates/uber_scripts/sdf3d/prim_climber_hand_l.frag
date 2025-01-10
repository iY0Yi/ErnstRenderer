#if IS_EDITING_TRVS
TRVsID = iFrame;
#endif
vec4 frot0, frot1, frot2, frot3;
vec3 rootPos, rootRot;
if(TRVsID == 0) {
  frot0 = vec4(-.1, .0, -.2, -.1);
  frot1 = vec4(-.1, .3, -.2, .1);
  frot2 = vec4(-.3, .6, -.2, .1);
  frot3 = vec4(-.1, .7, .1, .25);
  rootPos = vec3(0, .01, 0), rootRot = vec3(-.1, -.25, .0);
}
if(TRVsID == 1) {
  frot0 = vec4(-.0, .0, -.25, -.25);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .05, -.05), rootRot = vec3(-.25, -.2, .15);
}
if(TRVsID == 2) {
  frot0 = vec4(.3, .0, -.2, -.7);
  frot1 = vec4(.5, .8, -.2, -.15);
  frot2 = vec4(.5, .8, -.2, .0);
  frot3 = vec4(.5, .8, -.2, .25);
  rootPos = vec3(0, -.005, .0), rootRot = vec3(-.3, 0, 0);
}
if(TRVsID == 3) {
  frot0 = vec4(-.2, .5, -.2, -.2);
  frot1 = vec4(.1, .5, -.2, .0);
  frot2 = vec4(-.0, .5, -.2, .1);
  frot3 = vec4(.1, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(-.2, 0, 0);
}
if(TRVsID == 4) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .9, -.2, -.15);
  frot2 = vec4(-.1, .9, -.2, .0);
  frot3 = vec4(.0, .7, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(0, 0, .0);
}
if(TRVsID == 5) {
  frot0 = vec4(-.2, .0, -.25, -.15);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.0, .65, .4, -.05);
  rootPos = vec3(0, .04, 0), rootRot = vec3(-.2, .0, .1);
}
if(TRVsID == 6) {
  frot0 = vec4(-.05, .0, -.25, -.2);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .55, .4, -.05);
  rootPos = vec3(0, .04, .01), rootRot = vec3(-.15, .0, .1);
}
if(TRVsID == 7) {
  frot0 = vec4(-.175, .0, -.25, -.2);
  frot1 = vec4(-.2, 1.05, .2, -.15);
  frot2 = vec4(-.2, 1.05, .2, -.17);
  frot3 = vec4(-.1, .65, .4, -.15);
  rootPos = vec3(0, .04, .01), rootRot = vec3(-.1, .0, .2);
}
if(TRVsID == 8) {
  frot0 = vec4(.1, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .04, 0), rootRot = vec3(-.2, .0, -.1);
}
if(TRVsID == 9) {
  frot0 = vec4(-.1, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.15, .2, -.15);
  frot2 = vec4(-.1, 1.15, .2, -.17);
  frot3 = vec4(.2, .6, .4, -.35);
  rootPos = vec3(0, .0, 0), rootRot = vec3(.0, .0, .1);
}
if(TRVsID == 10) {
  frot0 = vec4(-.25, .0, -.25, -.2);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .5, .4, -.05);
  rootPos = vec3(0, .0, 0), rootRot = vec3(-.2, .0, .1);
}
if(TRVsID == 11) {
  frot0 = vec4(-.0, .0, -.25, -.3);
  frot1 = vec4(-.1, 1.05, .2, -.15);
  frot2 = vec4(-.1, 1.05, .2, -.17);
  frot3 = vec4(.1, .425, .4, -.2);
  rootPos = vec3(0, .03, -.03), rootRot = vec3(-.21, .05, .0);
}
if(TRVsID == 12) {
  frot0 = vec4(.0, .25, -.2, -.2);
  frot1 = vec4(.2, .6, -.3, .1);
  frot2 = vec4(.0, .6, -.3, .1);
  frot3 = vec4(-.2, .5, -.2, .25);
  rootPos = vec3(0, .025, -.02), rootRot = vec3(.1, 0, -.2);
}
if(TRVsID == 13) {
  frot0 = vec4(-.0, .15, -.25, -.4);
  frot1 = vec4(.15, .9, .2, -.15);
  frot2 = vec4(.025, 1., .2, -.17);
  frot3 = vec4(.1, .6, .4, -.05);
  rootPos = vec3(0, .0, .0), rootRot = vec3(-.25, -.0, -.6);
}
if(TRVsID == 14) {
  frot0 = vec4(.0, .0, -.2, -.2);
  frot1 = vec4(.0, .5, -.2, -.15);
  frot2 = vec4(-.1, .5, -.2, .0);
  frot3 = vec4(.0, .5, -.2, .25);
  rootPos = vec3(0, .025, 0), rootRot = vec3(0, 0, 0);
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
trp.x *= -1.;
td = sdHand(trp * 2., frot0, frot1, frot2, frot3) * .5;
