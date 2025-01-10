
// "Eroded Terrain Noise" by clayjohn:
//https://www.shadertoy.com/view/MtGcWh

// from https://www.shadertoy.com/view/XdXBRH
//name:Noise - Gradient - 2D - Deriv
//Author: iq
//License: MIT
// return gradient noise (in x) and its derivatives (in yz)
vec3 noised( in vec2 p )
{
    vec2 i = floor( p );
    vec2 f = fract( p );

    vec2 u = f*f*f*(f*(f*6.0-15.0)+10.0);
    vec2 du = 30.0*f*f*(f*(f-2.0)+1.0);

    vec2 ga = hash22( i + vec2(0.0,0.0) );
    vec2 gb = hash22( i + vec2(1.0,0.0) );
    vec2 gc = hash22( i + vec2(0.0,1.0) );
    vec2 gd = hash22( i + vec2(1.0,1.0) );

    float va = dot( ga, f - vec2(0.0,0.0) );
    float vb = dot( gb, f - vec2(1.0,0.0) );
    float vc = dot( gc, f - vec2(0.0,1.0) );
    float vd = dot( gd, f - vec2(1.0,1.0) );

    return vec3( va + u.x*(vb-va) + u.y*(vc-va) + u.x*u.y*(va-vb-vc+vd),   // value
                 ga + u.x*(gb-ga) + u.y*(gc-ga) + u.x*u.y*(ga-gb-gc+gd) +  // derivatives
                 du * (u.yx*(va-vb-vc+vd) + vec2(vb,vc) - va));
}
// code adapted from https://www.shadertoy.com/view/llsGWl
// name: Gavoronoise
// author: guil
// license: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
//Code has been modified to return analytic derivatives and to favour
//direction quite a bit.
vec3 erosion(in vec2 p, vec2 dir) {
    vec2 ip = floor(p);
    vec2 fp = fract(p);
    float f = 2.*PI;
    vec3 va = vec3(0.0);
   	float wt = 0.0;
    for (int i=-2; i<=1; i++) {
		for (int j=-2; j<=1; j++) {
        	vec2 o = vec2(i, j);
        	vec2 h = hash22(ip - o)*0.5;
            vec2 pp = fp +o - h;
            float d = dot(pp, pp);
            float w = exp(-d*2.0);
            wt +=w;
            float mag = dot(pp,dir);
            va += vec3(cos(mag*f), -sin(mag*f)*(pp+dir))*w;
        }
    }
    return va/wt;
}


//This is where the magic happens
float mountain(vec2 p) {
    // p*=.02;
    //First generate a base heightmap
    //it can be based on any type of noise
    //so long as you also generate normals
    //Im just doing basic FBM based terrain using
    //iq's analytic derivative gradient noise
    vec3 n = vec3(0.0);
    float nf = 1.0;
    float na = 0.6;
    vec2 q = p*.002;
    for (int i=0;i<3;i++) {
       n+= noised(q*nf)*na*vec3(1.0, nf, nf);
       na *= 0.3;
       nf *= 2.5;
       pRot(q,PI*.3);
    }

    //take the curl of the normal to get the gradient facing down the slope
    vec2 v = vec2(1,1);
    vec2 dir = n.zy*v;

    //Now we compute another fbm type noise
    // erosion is a type of noise with a strong directionality
    //we pass in the direction based on the slope of the terrain
    //erosion also returns the slope. we add that to a running total
    //so that the direction of successive layers are based on the
    //past layers
    q = p*.04;
    vec3 h = vec3(0.0);
    float f = 1.0;
    h+= erosion(q*f, dir+h.zy*v)*3.;
    f = 2.;
    h+= erosion(q*f, dir+h.zy*v)*1.;
    f = 8.;
    h+= erosion(q*f, dir+h.zy*v)*.2;
    f = 12.;
    h+= erosion(q*f, dir+h.zy*v)*.1;
    f = 20.;
    h+= erosion(q*f, dir+h.zy*v)*.05;
    //remap height to [0,1] and add erosion
    //looks best when erosion amount is small
    float bh = smoothstep(-1.0, 1.0, n.x) * smoothstep(300., 550., p.y);
    float er = smoothstep(-5.0, 5.0, h.x) * smoothstep(50., 150., p.y);
    bh = pow(bh, 1.);
    er = pow(er, 2.);
    return bh * 750. + er * 20.;
}