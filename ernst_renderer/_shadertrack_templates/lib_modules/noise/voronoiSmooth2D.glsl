float voronoiSmooth(vec2 p, float s)
{
    vec2 i = floor(p);
    vec2 f = fract(p);

    float res = 8.;
    for(int j=-1; j<=1; j++)
    for(int k=-1; k<=1; k++)
    {
        vec2 b = vec2(j,k);
        float d = length(b-f+hash22(i+b));
        float h = smoothstep(0., 1., .5 + .5*(res-d)/s );
        res = mix( res, d, h )-h*(1.-h)*s/(1.+3.*s);
    }
    return res;
}
