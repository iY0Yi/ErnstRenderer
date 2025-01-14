float sdTriangleIsosceles(vec2 p, vec2 q){
  p.x = abs(p.x);
  vec2 a = p - q*clamp( dot(p,q)/dot(q,q), 0., 1. );
  vec2 b = p - q*vec2( clamp( p.x/q.x, 0., 1. ), 1. );
  float s = -sign( q.y );
  vec2 d = min( vec2( dot(a,a), s*(p.x*q.y-p.y*q.x) ),
        vec2( dot(b,b), s*(p.y-q.y)  ));
  return -sqrt(d.x)*sign(d.y);
}