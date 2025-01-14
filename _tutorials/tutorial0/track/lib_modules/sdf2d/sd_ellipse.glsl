float sdEllipse(vec2 p, vec2 ab){
  p = abs(p); if( p.x > p.y ) {p=p.yx;ab=ab.yx;}
  float l = ab.y*ab.y - ab.x*ab.x;
  float m = ab.x*p.x/l;    float m2 = m*m; 
  float n = ab.y*p.y/l;    float n2 = n*n; 
  float c = (m2+n2-1.)/3.; float c3 = c*c*c;
  float q = c3 + m2*n2*2.;
  float d = c3 + m2*n2;
  float g = m + m*n2;
  float co;
  if( d<0.){
    float h = acos(q/c3)/3.;
    float s = cos(h);
    float t = sin(h)*sqrt(3.);
    float rx = sqrt( -c*(s + t + 2.) + m2 );
    float ry = sqrt( -c*(s - t + 2.) + m2 );
    co = (ry+sign(l)*rx+abs(g)/(rx*ry)- m)/2.;
  }
  else{
    float h = 2.*m*n*sqrt( d );
    float s = sign(q+h)*pow(abs(q+h), 1./3.);
    float u = sign(q-h)*pow(abs(q-h), 1./3.);
    float rx = -s - u - c*4. + 2.*m2;
    float ry = (s - u)*sqrt(3.);
    float rm = sqrt( rx*rx + ry*ry );
    co = (ry/sqrt(rm-rx)+2.*g/rm-m)/2.;
  }
  vec2 r = ab * vec2(co, sqrt(1.-co*co));
  return length(r-p) * sign(p.y-r.y);
}