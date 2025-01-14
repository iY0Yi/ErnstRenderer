#include bl_modules/bl_inc_common.glslinc
#include bl_modules/bl_inc_sdf.glslinc

vec4 intersect(vec3 ro, vec3 rd){
	float d = 0.;
	vec3  m = vec3(0);

	for (int i = 0; i < ITERATION; i++){
		vec4 res = sdScene(ro + d * rd);
		m = res.rgb;
		if (abs(res.w) < MIN_DIST || res.w >= MAX_DIST) break;
		d += res.w;
		if (d >= MAX_DIST) break;
	}
	return vec4(m,d);
}

vec3 normal(vec3 p){
    // Copy from iq shader.
    // inspired by tdhooper and klems - a way to prevent the compiler from inlining map() 4 times
    vec3 n = vec3(0.0);
    for( int i=0; i<4; i++ ){
        vec3 e = 0.5773*(2.0*vec3((((i+3)>>1)&1),((i>>1)&1),(i&1))-1.0);
        n += e*sdScene(p+0.0005*e).w;
    }
    return normalize(n);
}

float shadow(vec3 o, vec3 ldir){
	float mint=.001;
	float maxt=25.;
	float k = 40.;
	float res = 1.;
	float t=mint;
	for( int i=0; i < 80; i++){
		float h = sdScene(o + ldir*t).w;
		res = min( res, k*h/t);
		t += h;
		if( res<MIN_DIST || t>maxt ) break;
	}
	return sat(res);
}

// "Multi Level AO" by iY0Yi
// https://www.shadertoy.com/view/fsBfDR
float aoSeed = 0.;
const float MAX_SAMP = 16.;
float ao(vec3 p, vec3 n, float sphereRadius) {
    float ao = 0.;
    for(float i = 0.; i <= MAX_SAMP; i++) {
        vec2 rnd = hash21(i + 1. + aoSeed);

        float scale = (i + 1.)/MAX_SAMP;
        scale = mix(.0, 1., pow(scale, .5));

        rnd.x = (rnd.x * 2. - 1.) * PI * .5;
        rnd.y = (rnd.y * 2. - 1.) * PI;
        vec3 rd = normalize(n + hash21(i + 2. + aoSeed).xyx);
        rd.xy *= mat2(cos(rnd.x), sin(rnd.x), -sin(rnd.x), cos(rnd.x));
        rd.xz *= mat2(cos(rnd.y), sin(rnd.y), -sin(rnd.y), cos(rnd.y));

        rd *= sign(dot(rd, n));

        float raylen = sphereRadius * scale;
        vec3 rndp = p + normalize(n + rd) * raylen;
        float res = sdScene(rndp).w;
        ao += res;
        aoSeed++;
    }
    return ao/float(MAX_SAMP);
}

// https://hanecci.hatenadiary.org/entry/20130505/p2
// http://www.project-asura.com/program/d3d11/d3d11_006.html
float normalizedBlinnPhong(float shininess, vec3 n, vec3 vd, vec3 ld){
	float norm_factor = (shininess+1.) / (2.*PI);
	vec3 h  = normalize(-vd+ld);
	return pow(max(0., dot(h, n)), shininess) * norm_factor;
}

vec3 render(vec2 uv){
  vec3 ro=ray.origin;
  vec3 rd=ray.direction;
  // ray march
  vec4 res=intersect(ro, rd);
  vec3 p=ro+res.w*rd;
  vec3 m=res.rgb;
  vec3 fogCol=AMB_COL;
  vec3 col=pow(fogCol, vec3(2.2));
  if (res.w<MAX_DIST){
    vec3 ldir=normalize(lit0.direction);
    vec3 n=normal(p);
    float lamb1=sat(dot(n, ldir))*(1./PI);
    float lamb2=sat(dot(n, -ldir))*(1./PI);
    float sh=shadow(p+n*.01, ldir);
    float rgh=.0005;
    float spec=normalizedBlinnPhong(1./rgh, n, rd, ldir);
    float a=ao(p, n, .1);
    a+=ao(p, n, .65);
    a/=2.;
    float dif=lamb1*7.+lamb2*1.*a;
    dif*=sh;
    col*= dif*m;
    col=mix(col, pow(fogCol, vec3(2.2)), .5*a);
    float intensity=10.;
    spec=spec*intensity*sh*sh*sh;
    col+=spec;
    col=mix(col, pow(fogCol, vec3(2.2)), pow(distance(ro, p)/MAX_DIST, 1.));
  }
  col=tanh(col);
  return col;
}

// ---------------------------------------------------------------------
void mainImage(out vec4 fragColor, vec2 fragCoord){
  vec2 uv=(fragCoord.xy-iResolution.xy*.5)/iResolution.y;
  init();
  camera(uv+vec2(.02,0));
  vec3 col=render(uv);
  col=mix(col, sms(-.025, .55, col), .75);
  col=pow(col, vec3(.4545));
  fragColor=vec4(col, 1);
}