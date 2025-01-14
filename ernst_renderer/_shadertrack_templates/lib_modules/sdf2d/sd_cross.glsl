float sdCross(vec2 p, vec2 b, float r){
  p = abs(p); p = (p.y>p.x) ? p.yx : p.xy;
  vec2  q = p - b;
  float k = max(q.y,q.x);
  vec2  w = (k>0.) ? q : vec2(b.y-p.x,-k);
  return sign(k)*length(max(w,0.)) + r;
}