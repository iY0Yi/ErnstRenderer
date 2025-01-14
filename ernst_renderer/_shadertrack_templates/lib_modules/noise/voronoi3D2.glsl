vec2 voronoi(vec3 p) {
  vec3 i = floor(p);
  vec3 f = fract(p);

  vec2 res = vec2(100.);
  for(int j = -1; j <= 1; j++)
    for(int k = -1; k <= 1; k++)
      for(int l = -1; l <= 1; l++) {
        vec3 b = vec3(j, k, l);
        vec3 r = b - f + hash33(i + b);
        float d = dot(r, r);

        if(d < res.x)
          res = vec2(d, res.x);
        else if(d < res.y)
          res.y = d;
      }

  return res;
}
