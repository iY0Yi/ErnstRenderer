float sdBox( vec3 p, vec3 b){
  p = abs(p) - b;
  return length(max(p,0.)) + min(max(p.x,max(p.y,p.z)),0.);
}