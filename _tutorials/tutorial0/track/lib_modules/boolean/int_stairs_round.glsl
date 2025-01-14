float bIntStpS(float b, float a, float r, float n) {
  a = -a;
  b = -b;
  // avoid the expensive computation where not needed (produces discontinuity though)
  if((a < r) && (b < r)) {
    vec2 p = vec2(a, b);
    float columnradius = r * sqrt(2.) / n / 2.;
    columnradius = r * sqrt(2.) / (n * 2. + sqrt(2.));
    p = (p + vec2(p.y, -p.x)) * sqrt(.5);
    p.y += columnradius;
    p.x -= sqrt(2.) / 2. * r;
    p.x += -columnradius * sqrt(2.) / 2.;

    if(mod(n + 1., 2.) == 1.) {
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius * 2.) - columnradius;
    float d = -length(p) + columnradius;
    d = max(d, p.x);
    d = min(d, a);
    return -min(d, b);
  } else {
    return -min(a, b);
  }
}

vec4 bIntStpS(vec4 b, vec4 a, float r, float n) {
  a.w = -a.w;
  b.w = -b.w;
  if((a.w < r) && (b.w < r)) {
    vec2 p = vec2(a.w, b.w);
    float columnradius = r * sqrt(2.) / n / 2.;
    columnradius = r * sqrt(2.) / ((n - 1.) * 2. + sqrt(2.));
    p = (p + vec2(p.y, -p.x)) * sqrt(.5);
    p.y += columnradius;
    p.x -= sqrt(2.) / 2. * r;
    p.x += -columnradius * sqrt(2.) / 2.;
    if(mod(n, 2.) == 1.) {
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius * 2.) - columnradius;
    float d = -length(p) + columnradius;
    d = max(d, p.x);
    d = min(d, a.w);
    d = -min(d, b.w);
    vec3 m = mix(b.rgb, a.rgb, clamp(abs(-b.w) + abs(d), 0., 1.) * clamp(r, 0., 1.));
    return vec4(m, d);
  } else {
    return vec4(a.rgb, -min(a.w, b.w));
  }
}
