float sdParallelogram(vec2 p, float wi, float he, float sk){
  vec2 e = vec2(sk,he);
  p = (p.y<0.)?-p:p;
  vec2  w = p - e; w.x -= clamp(w.x,-wi,wi);
  vec2  d = vec2(dot(w,w), -w.y);
  float s = p.x*e.y - p.y*e.x;
  p = (s<0.)?-p:p;
  vec2  v = p - vec2(wi,0); v -= e*clamp(dot(v,e)/dot(e,e),-1.,1.);
  d = min( d, vec2(dot(v,v), wi*he-abs(s)));
  return sqrt(d.x)*sign(-d.y);
}