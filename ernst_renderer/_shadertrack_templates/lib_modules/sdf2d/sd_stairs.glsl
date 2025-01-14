float sdStairs(vec2 p, vec2 wh, float n){
  vec2 ba = wh*n;
  float d = min(dot2(p-vec2(clamp(p.x,0.,ba.x),0.)), 
    dot2(p-vec2(ba.x,clamp(p.y,0.,ba.y))) );
  float s = sign(max(-p.y,p.x-ba.x) );

  float dia = length(wh);
  p = mat2(wh.x,-wh.y, wh.y,wh.x)*p/dia;
  float id = clamp(round(p.x/dia),0.,n-1.);
  p.x = p.x - id*dia;
  p = mat2(wh.x, wh.y,-wh.y,wh.x)*p/dia;

  float hh = wh.y/2.;
  p.y -= hh;
  if( p.y>hh*sign(p.x) ) s=1.;
  p = (id<0.5 || p.x>0.) ? p : -p;
  d = min( d, dot2(p-vec2(0.,clamp(p.y,-hh,hh))) );
  d = min( d, dot2(p-vec2(clamp(p.x,0.,wh.x),hh)) );
  
  return sqrt(d)*s;
}