
// Interpolation funcs from:
// https://www.shadertoy.com/view/MsXGDj
float tcCatmullRom(float x, float v0,float v1, float v2,float v3){
    if(abs(v1-v2)<.001)return v1; // edited
	float c2 = -.5 * v0	+ 0.5*v2;
	float c3 = v0		+ -2.5*v1 + 2.0*v2 + -.5*v3;
	float c4 = -.5 * v0	+ 1.5*v1 + -1.5*v2 + 0.5*v3;
	return(((c4 * x + c3) * x + c2) * x + v1);
}
float tcThirdOrderSpline(float x, float L1,float L0, float H0,float H1){
	return 		  L0 +.5 *
			x * ( H0-L1 +
			x * ( H0 + L0 * -2.0 +  L1 +
			x * ((H0 - L0)* 9.0	 + (L1 - H1)*3.0 +
			x * ((L0 - H0)* 15.0 + (H1 - L1)*5.0 +
			x * ((H0 - L0)* 6.0	 + (L1 - H1)*2.0 )))));
}
float tcCubic(float x, float v0,float v1, float v2,float v3){
	float p = (v3 - v2) - (v0 - v1);
	return p*(x*x*x) + ((v0 - v1) - p)*(x*x) + (v2 - v0)*x + v1;
}
float tcSmoothstep(float x, float v0, float v1, float v2,float v3){
	x = x*x*(3.0-2.0*x);
	return (v2-v1)*x + v1;
}
float tcLinear(float x, float v0, float v1, float v2,float v3){
	return (v2-v1)*x + v1;
}

#define INTP tcCatmullRom

float fivePointToneCurve(float col, float low, float lmid, float mid, float hmid, float high){
    float VU = -0.25+low;
	float V1 =  0.0 +low;
	float V2 =  0.25+lmid;
	float V3 =  0.5 +mid;
	float V4 =  0.75+hmid;
	float V5 =  1.0 +high;
	float VO =  1.25+high;

	if(col<.25)
		return INTP( col*4.,      VU, V1, V2, V3);
	else if(col<.5)
		return INTP((col-.25)*4., V1, V2, V3, V4);
    else if(col<.75)
		return INTP((col- .5)*4., V2, V3, V4, V5);
	else if(col<1.)
		return INTP((col-.75)*4., V3, V4, V5, VO);
    else
        return 0.;
}

vec3 fivePointToneCurve(vec3 col, float low, float lmid, float mid, float hmid, float high){
	vec3 res;
	res.x = fivePointToneCurve(col.r, low, lmid, mid, hmid, high);
	res.g = fivePointToneCurve(col.g, low, lmid, mid, hmid, high);
	res.b = fivePointToneCurve(col.b, low, lmid, mid, hmid, high);
	return res;
}

float drawTCGraph(vec2 uv, float low, float lmid, float mid, float hmid, float high){
    vec2 gv = uv;
    gv.x*=iResolution.x/iResolution.y;
    gv.x-=.5*iResolution.x/iResolution.y-.5;

    float line = 1.;
    if(gv.x>0. && gv.x<1.){
        line = fivePointToneCurve(gv.x, low, lmid, mid, hmid, high);
        line = sms(.0,.005,abs(line-gv.y));

        line *= sms(.005,.0055,abs(0.001-gv.x));
        line *= sms(.0,.0025,abs(0.25-gv.x));
        line *= sms(.0,.0025,abs(0.5-gv.x));
        line *= sms(.0,.0025,abs(0.75-gv.x));
        line *= sms(.005,.0055,abs(.999-gv.x));

        line *= sms(.005,.0055,abs(0.001-gv.y));
        line *= sms(.0,.0025,abs(0.25-gv.y));
        line *= sms(.0,.0025,abs(0.5-gv.y));
        line *= sms(.0,.0025,abs(0.75-gv.y));
        line *= sms(.005,.0055,abs(.999-gv.y));
    }

    float hndls = 1.;
    hndls *= sms(.01,.012, distance(gv, vec2(0., low)));
    hndls *= sms(.01,.012, distance(gv, vec2(.25, lmid+.25)));
    hndls *= sms(.01,.012, distance(gv, vec2(.5, mid+.5)));
    hndls *= sms(.01,.012, distance(gv, vec2(.75, hmid+.75)));
    hndls *= sms(.01,.012, distance(gv, vec2(1., high+1.)));

    return line * hndls;
}
