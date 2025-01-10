float sdTrapezoid(vec2 p, float r1, float r2, float he){
  vec2 k1 = vec2(r2,he);
  vec2 k2 = vec2(r2-r1,2.*he);
  p.x = abs(p.x);
  vec2 ca = vec2(p.x-min(p.x,(p.y<0.)?r1:r2), abs(p.y)-he);
  vec2 cb = p - k1 + k2*clamp( dot(k1-p,k2)/dot2(k2), 0., 1. );
  float s = (cb.x<0. && ca.y<0.) ? -1. : 1.;
  return s*sqrt( min(dot2(ca),dot2(cb)) );
}