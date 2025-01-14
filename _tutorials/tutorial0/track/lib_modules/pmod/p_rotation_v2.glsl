vec2 pRot(inout vec2 p, float a){
  p=cos(a)*p+sin(a)*vec2(p.y, -p.x);
  return p;
}
