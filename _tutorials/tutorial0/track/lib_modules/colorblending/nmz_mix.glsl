//---------------Improved RGB--------------
// https://www.shadertoy.com/view/lsdGzN
/*
	The idea behind this function is to avoid the low saturation area in the
	rgb color space. This is done by getting the direction to that diagonal
	and displacing the interpolated	color by it's inverse while scaling it
	by saturation error and desired lightness.

	I find it behaves very well under most circumstances, the only instance
	where it doesn't behave ideally is when the hues are very close	to 180
	degrees apart, since the method I am using to find the displacement vector
	does not compensate for non-curving motion. I tried a few things to
	circumvent this problem but none were cheap and effective enough..
*/

//Changes the strength of the displacement
#define DSP_STR 1.5

//Optimizaton for getting the saturation (HSV Type) of a rgb color
#if 0
float getsat(vec3 c)
{
    c.gb = vec2(max(c.g, c.b), min(c.g, c.b));
	c.rg = vec2(max(c.r, c.g), min(c.r, c.g));
	return (c.r - min(c.g, c.b)) / (c.r + 1e-7);
}
#else
//Further optimization for getting the saturation
float getsat(vec3 c)
{
    float mi = min(min(c.x, c.y), c.z);
    float ma = max(max(c.x, c.y), c.z);
    return (ma - mi)/(ma+ 1e-7);
}
#endif

//Improved rgb lerp
vec3 nmz_mix(in vec3 a, in vec3 b, in float x)
{
    //Interpolated base color (with singularity fix)
    vec3 ic = mix(a, b, x) + vec3(1e-6,0.,0.);

    //Saturation difference from ideal scenario
    float sd = abs(getsat(ic) - mix(getsat(a), getsat(b), x));

    //Displacement direction
    vec3 dir = normalize(vec3(2.*ic.x - ic.y - ic.z, 2.*ic.y - ic.x - ic.z, 2.*ic.z - ic.y - ic.x));
    //Simple Lighntess
    float lgt = dot(vec3(1.0), ic);

    //Extra scaling factor for the displacement
    float ff = dot(dir, normalize(ic));

    //Displace the color
    ic += DSP_STR*dir*sd*ff*lgt;
    return clamp(ic,0.,1.);
}