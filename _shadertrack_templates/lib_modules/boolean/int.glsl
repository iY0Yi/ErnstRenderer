float bInt(float a,float b){
  return max(a, b);
}

vec4 bInt(vec4 a,vec4 b){
  float res = max(a.x, b.x);
  return (res==a.x)?a:b;
}
