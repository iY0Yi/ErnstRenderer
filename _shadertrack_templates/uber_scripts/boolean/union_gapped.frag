float bUniGap(float a, float b, float g){
    return min(max(b,-a+g),a);
}

vec4 bUniGap(vec4 a, vec4 b, float g){
    float d = min(max(b.x,-a.x+g),a.x);
    return vec4(d, (abs(d-a.x)<.001) ? a.yzw:b.yzw);
}