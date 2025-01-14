float sdRoundedBox(vec2 p, vec2 b, vec4 r){
  r.xy = (p.x>0.)?r.xy : r.zw;
  r.x  = (p.y>0.)?r.x  : r.y;
  vec2 q = abs(p)-b+r.x;
  return min(max(q.x,q.y),0.) + length(max(q,0.)) - r.x;
}