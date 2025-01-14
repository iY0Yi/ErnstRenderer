float sdCurveQuadratic(vec3 pos, vec3 A, vec3 B, vec3 C, float r1, float r2){ 
    vec3 a = B - A;
    vec3 b = A - 2.*B + C;
    vec3 c = a * 2.;
    vec3 d = A - pos;

    float kk = 1./dot(b,b);
    float kx = kk*dot(a,b);
    float ky = kk*(2.*dot(a,a)+dot(d,b))/3.;
    float kz = kk*dot(d,a);      

    float p = ky - kx*kx;
    float p3 = p*p*p;
    float q = kx*(2.*kx*kx-3.*ky)+kz;
    float h = q*q+4.*p3;

    #define rr (r2/r1)
    #define f(x) ((x)*(1.-rr)+rr)
    vec3 dt;
    if(h>=0.){ 
        h = sqrt(h);
        vec2 x = (vec2(h, -h) - q)*.5;
        vec2 uv = sign(x)*pow(abs(x), vec2(1./3.));
        float t = clamp(uv.x+uv.y-kx,0.,1.);

        // 1 root
        dt = d+(c+b*t)*t;
        return length(dt)-r1*f(1.-t);
    }
    
    float z = sqrt(-p);
    float v = acos( q/(p*z*2.))/3.;
    float m = cos(v);
    float n = sin(v)*1.732050808;
    vec3 t = clamp(vec3(m+m,-n-m,n-m)*z-kx,0.,1.);

    // 3 roots, but only need two
    dt = d+(c+b*t.x)*t.x;
    float dis = length(dt)-r1*f(1.-t.x);
    dt = d+(c+b*t.y)*t.y;
    dis = min(length(dt)-r1*f(1.-t.y), dis);
    return dis;
}