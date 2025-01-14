float bUniStpS(float a, float b, float r, float n){
  if ((a < r) && (b < r)){
    vec2 p = vec2(a, b);
    float columnradius = r*sqrt(2.)/(n*2.+sqrt(2.));
    p = (p + vec2(p.y, -p.x))*sqrt(.5);
    p.x -= sqrt(2.)/2.*r;
    p.x += columnradius*sqrt(2.);
    if (mod(n+1.,2.) == 1.){
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius*2.) - columnradius;
    float result = length(p) - columnradius;
    result = min(result, p.x);
    result = min(result, a);
    return min(result, b);
  }else{
    return min(a, b);
  }
}

vec4 bUniStpS(vec4 a, vec4 b, float r, float n){
  if ((a.x < r) && (b.x < r)){
    vec2 p = vec2(a.x, b.x);
    float columnradius = r*sqrt(2.)/(n*2.+sqrt(2.));
    p = (p + vec2(p.y, -p.x))*sqrt(.5);
    p.x -= sqrt(2.)/2.*r;
    p.x += columnradius*sqrt(2.);
    if (mod(n+1.,2.) == 1.){
      p.y += columnradius;
    }
    p.y = mod(p.y + columnradius, columnradius*2.) - columnradius;
    float res = length(p) - columnradius;
    res = min(res, p.x);
    res = min(res, a.x);
    res = min(res, b.x);
    if(res>=b.x-.001) return b;
    return vec4(res, a.yzw);
  }else{
    float res = min(a.x, b.x);
    if(res==a.x) return a;
    if(res==b.x) return b;
  }
}
