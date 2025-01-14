void orthographicCam(vec2 uv){
    vec3 up = vec3(0,1,0);
    vec3 dir = vec3(0,0,1);
    pRotQuat(up, cam0.quaternion);
    pRotQuat(dir, cam0.quaternion);
    up = up.xzy, dir = dir.xzy;
    cam0.up = up;

    vec3 pos = dir*100.;

    vec3 cw = normalize(dir - pos);
    vec3 cu = normalize(cross(cw, up));
    vec3 cv = normalize(cross(cu, cw));

    uv *= cam0.orthoScale/cam0.orthoDist;

    float perspective = 1.5;
    float fv = acos(dot(cw, normalize(cu * uv.x)));
    float screenSize = (cam0.orthoDist*perspective / (2. * tan(abs(fv) / 2.)));
    vec3 virtscreen = pos + cw * 2. + (cu * uv.x + cv * uv.y) * screenSize;

    ray.origin = -pos + (cu * uv.x + cv * uv.y) * (.7 + .2 * perspective) * screenSize;
    ray.direction = normalize(virtscreen - ray.origin);
    ray.origin+=cam0.pivot.xzy-ray.direction*50.;
}
