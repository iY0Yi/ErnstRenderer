float sdRoundedX(vec2 p, float w, float r){
  p = abs(p);
  return length(p-min(p.x+p.y,w)*.5) - r;
}