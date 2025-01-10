float bSub(float a,float b){
  return max(-a, b);
}

vec4 bSub(vec4 a,vec4 b){
  float res = max(-a.x, b.x);
  return (res==-a.x)?vec4(-a.x, a.yzw):b;
}
