float bIntS(float a,float b,float r){
  vec2 u = max(vec2(r + b,r + a), vec2(0));
  return min(-r, max (b, a)) + length(u);
}

vec4 bIntS(vec4 a,vec4 b,float r){
  vec2 u = max(vec2(r + b.x,r + a.x), vec2(0));
  float res =  min(-r, max(b.x, a.x)) + length(u);
  vec3 m = mix(a.yzw, b.yzw, clamp(a.x-res,0.,1.)*r);
  return vec4(res, m);
}
