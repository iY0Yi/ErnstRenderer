// quaternion functions
vec4 invQuat = vec4(1,1,1,-1);

vec4 getQuat(vec3 ax, float a) {
    return vec4(normalize(ax)*sin(a*.5), cos(a*.5));
}

vec4 getQuat(vec3 curDir, vec3 trgtDir) {
    curDir = normalize(curDir);
    trgtDir = normalize(trgtDir);
    vec3 ax = cross(trgtDir, curDir);
    float a = acos(dot(curDir, trgtDir));
    return getQuat(ax, a);
}

vec4 mulQuat(vec4 q1, vec4 q2) {
    vec3 ax = q1.w*q2.xyz + q2.w*q1.xyz + cross(q1.xyz,q2.xyz);
    float a = q1.w*q2.w - dot(q1.xyz,q2.xyz);
    return vec4(ax, a);
}

void pRotQuat(inout vec3 p, vec4 quat){
    p = p + 2.*cross(quat.xyz, cross(quat.xyz,p)-quat.w*p);
}
