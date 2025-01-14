float voronoi(vec3 st, float scl, float speed, inout vec3 id) {
  float res = 1. * scl;
  st = u2s(st) * scl;
  vec3 ist = floor(st);
  vec3 fst = fract(st);
  for(float z = -1.; z <= 1.; z += 1.) {
    for(float y = -1.; y <= 1.; y += 1.) {
      for(float x = -1.; x <= 1.; x += 1.) {
        vec3 gridOffset = vec3(x, y, z);
        vec3 rnd = hash33(ist + gridOffset + speed * .5);
        float d = distance(st, ist + gridOffset + rnd);
        if(d < res) {
          res = d;
          id = rnd;
        }
      }
    }
  }
  return res;
}
