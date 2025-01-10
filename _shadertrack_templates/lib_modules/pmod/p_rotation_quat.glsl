void pRotQuat(inout vec3 p, vec4 quat){
    p = p + 2. * cross(quat.xyz, cross(quat.xyz, p) + quat.w * p);
}