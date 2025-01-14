float sdNGon(vec2 uv, const float N, const float R){
  uv = -uv.yx; 								 // if you want the corner to be up
  float sa = TAU / N; 						 // segment angle
  float a = floor(atan(uv.y,uv.x)/sa+.5)*sa;  // round current angle to closest segment angle
    
  vec2 p1 = vec2(cos(a),sin(a)); 				 // plane to find distance to
  float distr = dot(uv,p1) - R; 				 // signed distance to edge
#ifndef FAST
  float hw = R * tan(sa * .5); 				 // half-width of the edge
  float disth = abs(dot(uv,vec2(-p1.y,p1.x))); // horizontal distance to the middle of the edge
  return length(vec2(min(hw-disth,0.),distr))*sign(distr); // distance to the edge or corner point
#endif
  return distr;
}