void perspectiveCam(vec2 uv){
    vec3 up = vec3(0,1,0);
    vec3 dir = vec3(0,0,-1);
    pRotQuat(up, cam0.quaternion);
    pRotQuat(dir, cam0.quaternion);
    up = up.xzy, dir = dir.xzy;
    vec3 pos = cam0.position;
    float fov = cam0.fov;
    vec3 target = pos-dir;

    vec3 cw = normalize(target - pos);
    vec3 cu = normalize(cross(cw, up));
    vec3 cv = normalize(cross(cu, cw));

    cam0.up = up;

    mat3 camMat = mat3(cu, cv, cw);
    ray.origin = pos;
    ray.direction = normalize(camMat * normalize(vec3(sin(fov) * uv.x, sin(fov) * uv.y, -cos(fov))));
}