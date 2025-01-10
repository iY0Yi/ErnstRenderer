// Cheap Rotation by las:
// http://www.pouet.net/topic.php?which=7931&page=1
// ---------------------------------------------------------------------
#define R(p, a) p = cos(a) * p + sin(a) * vec2(p.y, -p.x)
vec3 rot(vec3 p, vec3 r) {
  R(p.xz, r.y);
  R(p.yx, r.z);
  R(p.zy, r.x);
  return p;
}
