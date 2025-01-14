vec3 pow_mix(vec3 colA, vec3 colB, float h){
  float baseg = 16.;
  float f = sabs(h-.5,.5)*2.;
  vec3 gamma=vec3(baseg)-f*(baseg-1.)+4.2;
  colA=pow(colA, 1./gamma);
  colB=pow(colB, 1./gamma);
  return pow(mix(colA, colB, h), gamma*(.5+f*.5));
}