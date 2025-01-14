mat4 getRotMat( vec3 v, float a )
{
    float s = sin(a);
    float c = cos(a);
    float ic = 1. - c;

    return mat4( v.x*v.x*ic + c,     v.y*v.x*ic - s*v.z, v.z*v.x*ic + s*v.y, 0,
                 v.x*v.y*ic + s*v.z, v.y*v.y*ic + c,     v.z*v.y*ic - s*v.x, 0,
                 v.x*v.z*ic - s*v.y, v.y*v.z*ic + s*v.x, v.z*v.z*ic + c,     0,
			     0, 0, 0, 1 );
}

mat4 getMat(vec3 tr, vec3 rot) {
    mat4 trM = mat4(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        tr.x, tr.y, tr.z, 1);
    mat4 rxM = getRotMat(vec3(1,0,0), rot.x);
    mat4 ryM = getRotMat(vec3(0,1,0), rot.y);
    mat4 rzM = getRotMat(vec3(0,0,1), rot.z);
    return trM * rxM * ryM * rzM;
}

mat4 getInvM(mat4 m) {
    mat3 rotM = mat3(m);
    mat3 invRotM = transpose(rotM);

    vec3 tr = vec3(m[3].xyz);
    vec3 invTr = -invRotM * tr;

    return mat4(
        invRotM[0], 0,
        invRotM[1], 0,
        invRotM[2], 0,
        invTr, 1
    );
}

vec3 mul(mat4 m, vec3 v){
    return (m*vec4(v,1)).xyz;
}