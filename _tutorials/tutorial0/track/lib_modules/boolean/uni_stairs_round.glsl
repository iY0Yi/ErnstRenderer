float bUniStpS(float a, float b, float r, float n) {
  if((a < r) && (b < r)) {
    vec2 p = vec2(a, b);
    float columnradius = r * sqrt(2.) / (n * 2. + sqrt(2.));
    p = (p + vec2(p.y, -p.x)) * sqrt(.5);
    p.x -= sqrt(2.) / 2. * r;
    p.x += columnradius * sqrt(2.);
    if(mod(n + 1., 2.) == 1.) {
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius * 2.) - columnradius;
    float d = length(p) - columnradius;
    d = min(d, p.x);
    d = min(d, a);
    return min(d, b);
  } else {
    return min(a, b);
  }
}

vec4 bUniStpS(vec4 a, vec4 b, float r, float n) {
  if((a.w < r) && (b.w < r)) {
    vec2 p = vec2(a.w, b.w);
    float columnradius = r * sqrt(2.) / (n * 2. + sqrt(2.));
    p = (p + vec2(p.y, -p.x)) * sqrt(.5);
    p.x -= sqrt(2.) / 2. * r;
    p.x += columnradius * sqrt(2.);
    if(mod(n + 1., 2.) == 1.) {
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius * 2.) - columnradius;
    float d = length(p) - columnradius;
    d = min(d, p.x);
    d = min(d, a.w);
    d = min(d, b.w);
    if(d >= b.w - .001) return b;
    return vec4(a.rgb, d);
  } else {
    float d = min(a.w, b.w);
    if(d == a.w) return a;
    if(d == b.w) return b;
  }
}
