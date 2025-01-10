#include bl_modules/bl_inc_common.glslinc
#include lib_modules/shading/blinnphong.glsl
#include bl_modules/bl_inc_sdf.glslinc

// ---------------------------------------------------------------------
vec4 intersect(){
	float d = 1.;
	vec3  m = MAT_VOID;
	for (int i = 0; i < ITERATION; i++){
		vec3 p = ray.origin + d * ray.direction;
		vec4 res = sdScene(p);
		m = res.yzw;
		res.x *= .5;
		if (abs(res.x) < MIN_DIST || res.x >= MAX_DIST) break;
		d += res.x;
		if (d >= MAX_DIST) break;
	}
	return vec4(d,m);
}

// ---------------------------------------------------------------------
vec3 normal(vec3 p){
	float c=sdScene(p).x;
	float e=MIN_DIST*10.;
	return normalize(vec3(
		sdScene(p+vec3(e,0.,0.)).x-c,
		sdScene(p+vec3(0.,e,0.)).x-c,
		sdScene(p+vec3(0.,0.,e)).x-c)
	);
}

// ---------------------------------------------------------------------
float shadow(vec3 p) {
  float t = MIN_DIST;
  for(int i = 0; i < ITERATION; i++) {
    vec4 res = sdScene(p + lit0.direction * t);
    if(res.x < MIN_DIST) return 0.;
    t += res.x;
    if(t > MAX_DIST) break;
  }
  return 1.;
}

// AO
// ---------------------------------------------------------------------
float aoSeed = 0.;
float ao(vec3 p, vec3 n, float radius) {
  const float MAX_SAMP = 16.;
  float ao = 0.;
  for(float i = 0.; i <= MAX_SAMP; i++) {
    vec3 rnd = hash31(i + 1. + aoSeed);

    // The contribution is adjusted according to the distance from the origin.
    // http://john-chapman-graphics.blogspot.com/2013/01/ssao-tutorial.html
    float scale = (i + 1.) / MAX_SAMP;
    scale = mix(.0, 1., pow(scale, .25));

    // radians for rotate normal in hemisphere.
    rnd.x = (rnd.x * 2. - 1.) * PI;
    rnd.y = (rnd.y * 2. - 1.) * PI;
    vec3 rd = normalize(n + hash31(i + 2. + aoSeed));
    rd.zy *= mat2(cos(rnd.x), sin(rnd.x), -sin(rnd.x), cos(rnd.x));
    rd.xz *= mat2(cos(rnd.y), sin(rnd.y), -sin(rnd.y), cos(rnd.y));

    // http://www.aduprat.com/portfolio/?page=articles/hemisphericalSDFAO
    rd *= sign(dot(rd, n));

    float raylen = radius * scale;
    vec3 rndp = p + normalize(n + rd) * raylen;  // sampling position
    float res = clamp(sdScene(rndp).x / raylen, .01, 1.);
    ao += res;
    aoSeed++;
  }
  return ao / float(MAX_SAMP);
}

float shadowLow(vec3 o, vec3 n){
    o+=n*.01;
	float t=.01;
	for( int i=0; i < 40; i++){
		float res = sdScene(o + lit0.direction*t).x;
		t += res;
		if(res<0.01)return 0.;
        if(t>20.) break;
	}
	return 1.;
}
#define PIXEL_NOISE
const float MAX_SAMP = 20.;
const float BOUNCE = 5.;
vec2 c = vec2(0);
vec3 amb = vec3(0);
vec4 fakeGI(vec3 p, vec3 n, float radius) {
  float ao = 0.;
  float tbnc = 0.;
  vec3 bleed = vec3(0);
  bleed = renDat.albedo;
  float mskDirect=0., litIndirect=1., roughness = 1.;
  for(float i = 0.; i <= MAX_SAMP; i++) {
    vec2 rnd = hash21(i + aoSeed++ + length(c));
    
    float scale = (i + 1.) / (MAX_SAMP+1.);
    scale = mix(0., 1., pow(scale, .5));

    rnd.x = (rnd.x * 2. - 1.) * PI*.05*roughness;
    rnd.y = (rnd.y * 2. - 1.) * PI*roughness;
    vec2 rnd1 = hash21(i + aoSeed++ + length(c))*roughness;
    vec2 rnd2 = hash21(i + aoSeed++ + length(c))*roughness;
    vec3 rd = normalize(n + vec3(rnd1.xy, rnd2.x));
    rd.xz *= mat2(cos(rnd.x), sin(rnd.x), -sin(rnd.x), cos(rnd.x));
    rd.xy *= mat2(cos(rnd.y), sin(rnd.y), -sin(rnd.y), cos(rnd.y));
    rd *= sign(dot(rd, n));
    //sign(-dot(n, r.d))
    rd = normalize(n + rd);
    
    float raylen = radius * scale;
    vec3 rndp = p + rd * raylen;
    vec4 res = sdScene(rndp);
    vec3 vp = p+rd*res.x;
    
    // ao
    float rndao = distance(p,vp) / raylen;
    ao += rndao;
    
    vec3 vn = n;
    // color bleeding and bounce light
    vec3 tot = res.yzw;
    vec3 mask = vec3(1);
    for(float j=0.;j<BOUNCE;j++){
        
        vec2 rnd3 = hash21(j + aoSeed++ + length(c));
        //float scale = (i+j + 1.) / (MAX_SAMP+1.);
        //scale = mix(MIN_DIST, 1., pow(scale, 1.));

        rnd3.x = (rnd3.x * 2. - 1.) * PI*.025*roughness;
        rnd3.y = (rnd3.y * 2. - 1.) * PI*roughness;
        vec2 rnd4 = hash21(i+j + aoSeed++ + length(c))*roughness;
        vec2 rnd5 = hash21(i+j + aoSeed++ + length(c))*roughness;
        vec3 rd = normalize(vn + vec3(rnd4.xy, rnd5.x));
        rd.xz *= mat2(cos(rnd3.x), sin(rnd3.x), -sin(rnd3.x), cos(rnd3.x));
        rd.xy *= mat2(cos(rnd3.y), sin(rnd3.y), -sin(rnd3.y), cos(rnd3.y));
        rd *= sign(dot(rd, vn));
        rd = normalize(vn + rd);
        
        vp = vp+rd*res.x;
        res = sdScene(vp);
        vn = normal(vp);
        float direct = sat(dot(vn, lit0.direction));
        float shadow = shadowLow(vp, vn);
        float mskDirect = direct*shadow;
        
        if(res.x>radius){tot+=AMB_STRENGTH*AMB_COL+mskDirect*lit0.color*lit0.intensity*mask;break;}
        tot+=res.yzw*mskDirect*lit0.color*lit0.intensity*mask;
        mask*=res.yzw;
        // https://www.shadertoy.com/view/4sfGDB
        // acc += mask * obj.e * E + mask * obj.c * e;
		// mask *= obj.c;
        
    }
    bleed += tot/(BOUNCE+1.);
  }
    
  //return vec4(bleed/(MAX_SAMP+1.), ao / float((MAX_SAMP+1.)));
  return vec4(bleed/(MAX_SAMP+1.), ao / float((MAX_SAMP+1.)));
}

#include lib_modules/debug/debugISO.glsl
// ---------------------------------------------------------------------
void render(){
	vec4 res = intersect();
	vec3 p = ray.origin + res.x * ray.direction;

	if (res.x>=MAX_DIST){
		renDat.albedo = FOG_COL;
		renDat.normal = vec3(0);
		renDat.diffuse = 0.;
		renDat.specular = 0.;
		renDat.shadow = 0.;
		renDat.ao = 0.;
		renDat.depth = 1.;
		renDat.result = FOG_COL;
	}
	else{
		renDat.albedo = res.yzw;

		// Normal (convert it World Space to Screen Space)
		vec3 n = normal(p);
		vec3 up = vec3(0,1,0);
    vec3 dir = vec3(0,0,-1);
    pRotQuat(up, cam0.quaternion);
    pRotQuat(dir, cam0.quaternion);
    up = up.xzy, dir = dir.xzy;
		vec3 pos = cam0.position;
		float fov = cam0.fov;
		vec3 target = pos - dir;
		vec3 cw = normalize(target - pos);
		vec3 cu = normalize(cross(cw, up));
		vec3 cv = normalize(cross(cu, cw));
		vec3 side = cross(dir, up);
		renDat.normal.x = dot(n, cu);
		renDat.normal.y = dot(n, up);
		renDat.normal.z = dot(n, -dir);
		renDat.normal = normalize(renDat.normal);

		// Diffuse (Half-Lambert)
		renDat.diffuse = dot(n, lit0.direction) * .5 + .5;

		renDat.shadow = shadow(p)*smoothstep(.0, .01, sat(dot(n, lit0.direction)));

		// Ambient Occulusion (Multi level)
		renDat.ao = 0.;
		renDat.ao += pow(ao(p, n, .1), 1.25);
		renDat.ao += pow(ao(p, n, .25), 1.25);
		renDat.ao += pow(ao(p, n, .5), 1.25);
		renDat.ao += pow(ao(p, n, 1.), 1.25);
		renDat.ao += pow(ao(p, n, 2.), 1.25);
		renDat.ao = smoothstep(1., 5., renDat.ao);

		// vec4 gi = fakeGI(p,n,1.);
		// renDat.albedo = gi.rgb*renDat.albedo;

		renDat.result = mix(vec3(0), lit0.color, renDat.diffuse);
		renDat.result += mix(vec3(0), AMB_COL, renDat.ao*AMB_STRENGTH);
		renDat.result*= renDat.albedo;

		float roughness = .001;
		float intensity = 1.;
		getMaterialParams(renDat.albedo, intensity, roughness);
		float spec = BlinnPhong(1./roughness, n, ray.direction, lit0.direction)*(1./PI);
    	renDat.specular = spec * intensity;
		renDat.result = mix(renDat.result, renDat.result+lit0.color, renDat.specular*renDat.shadow);
		renDat.depth = distance(ray.origin, p)/MAX_DIST;
		renDat.result = mix(renDat.result, FOG_COL, sat(pow(renDat.depth+FOG_START, FOG_POW)));
	}
}

// Pack all data in a vec4
vec4 packRenderData() {
#define dlamp(x) clamp(abs(x) * .994 + .003, .0, 1.) * sign(x)
  return vec4(
      packU4(vec4(renDat.albedo, renDat.shadow)),
      packS3(dlamp(vec3(u2s(renDat.diffuse), renDat.specular, u2s(renDat.ao)))),
      packS3(dlamp(renDat.normal)),
      renDat.depth);
}

// ---------------------------------------------------------------------
void mainImage(out vec4 fragColor, vec2 fragCoord){
	vec2 uv = fragCoord.xy / iResolution.xy;
	if(uv.x>INV_ERNST_RENDER_SCALE || uv.y>INV_ERNST_RENDER_SCALE) return;

	uv*=ERNST_RENDER_SCALE;
	float ml = (min(iResolution.x, iResolution.y)==iResolution.x)?1.0:iResolution.y/iResolution.x;
	uv = (uv*2.-1.)*ml;
	uv.x *= iResolution.x / iResolution.y;

	init();
	camera(uv);
	render();
	fragColor = packRenderData();
}
