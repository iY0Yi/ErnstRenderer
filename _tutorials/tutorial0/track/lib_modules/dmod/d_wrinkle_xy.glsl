
float wkXY(vec3 p, float s, float m){
    vec3 qp = p, qn = p;
    float z = sms(-.4, .75, sin(p.y*m*TAU));
    float id = floor(p.y*m*TAU);
    float rnd = hash11(id);
    float r = mix(PI*.1/m*z, PI*.1/m, sms(-.4, .3, p.x));
    float o = -.2;

    qp.x*=s*.5;
    qn.x*=s*.5;

    qp.y-=p.y;
    qp.x-=o;
    pRot(qp.xy, -r);
    qp.y+=p.y;
    qp.x+=o;

    qn.y-=p.y;
    qn.x-=o;
    pRot(qn.xy, r);
    qn.y+=p.y;
    qn.x+=o;

    float dv = TAU*m;
    float n = gfbm(vec2(2,p.y)*3., 3, .25);
    float np = sin(qp.y*dv+n*3.)*.5+.5;
    float nn = sin(qn.y*dv-n*1.)*.5+.5;
    return pow(sms(-.8, .8, bUniS(np, nn, 1.)), 1.);//pow(sms(-.6, .7+sin(n*2.), .5)*.2, bUniS(np, nn, .5));
}