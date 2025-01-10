float bIntStpS(float b, float a, float r, float n){
  a = -a;
  b = -b;
  float m = min(a, b);
  //avoid the expensive computation where not needed (produces discontinuity though)
  if ((a < r) && (b < r)) {
    vec2 p = vec2(a, b);
    float columnradius = r*sqrt(2.)/n/2.;
    columnradius = r*sqrt(2.)/(n*2.+sqrt(2.));
    p = (p + vec2(p.y, -p.x))*sqrt(.5);
    p.y += columnradius;
    p.x -= sqrt(2.)/2.*r;
    p.x += -columnradius*sqrt(2.)/2.;

    if (mod(n+1.,2.) == 1.) {
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius*2.) - columnradius;
    float result = -length(p) + columnradius;
    result = max(result, p.x);
    result = min(result, a);
    return -min(result, b);
  } else {
    return -m;
  }
}

vec4 bIntStpS(vec4 b, vec4 a, float r, float n){
  a.x = -a.x;
  b.x = -b.x;
  float m = min(a.x, b.x);
  if ((a.x < r) && (b.x < r)){
    vec2 p = vec2(a.x, b.x);
    float columnradius = r*sqrt(2.)/n/2.;
    columnradius = r*sqrt(2.)/((n-1.)*2.+sqrt(2.));
    p = (p + vec2(p.y, -p.x))*sqrt(.5);
    p.y += columnradius;
    p.x -= sqrt(2.)/2.*r;
    p.x += -columnradius*sqrt(2.)/2.;
    if (mod(n,2.) == 1.){
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius*2.) - columnradius;
    float res = -length(p) + columnradius;
    res = max(res, p.x);
    res = min(res, a.x);
    res = -min(res, b.x);
    vec3 mt = mix(b.yzw, a.yzw, clamp(abs(-b.x)+abs(res),0.,1.)*clamp(r,0.,1.));
    return vec4(res, mt);
  }else{
    float res = -m;
    return vec4(res, a.yzw);
  }
}
