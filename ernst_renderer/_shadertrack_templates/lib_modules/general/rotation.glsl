#define R(p, a) p *= mat2(cos(a),sin(a),-sin(a),cos(a))
vec3 rot(vec3 p, vec3 r) {
  R(p.xz, r.y); R(p.yx, r.z); R(p.zy, r.x);
  return p;
}
