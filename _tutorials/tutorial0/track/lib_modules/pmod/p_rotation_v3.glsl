vec3 pRot(inout vec3 p, vec3 r){
  #define r2d(v, a) v=cos(a)*v+sin(a)*vec2(v.y, -v.x)
  r2d(p.xz, r.y);
  r2d(p.yx, r.z);
  r2d(p.zy, r.x);
  return p;
}
