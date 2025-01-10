float voronoiSmooth(vec3 p, float s)
{
    vec3 i = floor(p);
    vec3 f = fract(p);

    float res = 8.;
    for(int j=-1; j<=1; j++)
    for(int k=-1; k<=1; k++)
    for(int l=-1; l<=1; l++)
    {
        vec3 b = vec3(j,k,l);
        float d = length(b-f+hash33(i+b));
        float h = smoothstep(0., 1., .5 + .5*(res-d)/s );
        res = mix( res, d, h )-h*(1.-h)*s/(1.+3.*s);
    }
    return res;
}