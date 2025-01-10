float voronoi(vec2 st, float scl, float speed, inout vec2 id) {
  float res = 1. * scl;
  st = u2s(st) * scl;
  vec2 ist = floor(st);
  vec2 fst = fract(st);
  for(float y = -1.; y <= 1.; y += 1.) {
    for(float x = -1.; x <= 1.; x += 1.) {
      vec2 gridOffset = vec2(x, y);
      vec2 rnd = hash22(ist + gridOffset + speed * .5);
      float d = distance(st, ist + gridOffset + rnd);
      if(d < res) {
        res = d;
        id = rnd;
      }
    }
  }
  return res;
}
