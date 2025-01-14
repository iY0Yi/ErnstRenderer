// "Noise - gradient - 3D" by iq:
// https://www.shadertoy.com/view/Xsl3Dl
// 0: cubic
// 1: quintic
#define INTERPOLANT 0
float gnoise( in vec3 p ){
    vec3 i = floor( p );
    vec3 f = fract( p );

    #if INTERPOLANT==1
    // quintic interpolant
    vec3 u = f*f*f*(f*(f*6.-15.)+10.);
    #else
    // cubic interpolant
    vec3 u = f*f*(3.-2.*f);
    #endif

    return mix( mix( mix( dot( hash33( i + vec3(0,0,0) ), f - vec3(0,0,0) ),
                          dot( hash33( i + vec3(1,0,0) ), f - vec3(1,0,0) ), u.x),
                     mix( dot( hash33( i + vec3(0,1,0) ), f - vec3(0,1,0) ),
                          dot( hash33( i + vec3(1,1,0) ), f - vec3(1,1,0) ), u.x), u.y),
                mix( mix( dot( hash33( i + vec3(0,0,1) ), f - vec3(0,0,1) ),
                          dot( hash33( i + vec3(1,0,1) ), f - vec3(1,0,1) ), u.x),
                     mix( dot( hash33( i + vec3(0,1,1) ), f - vec3(0,1,1) ),
                          dot( hash33( i + vec3(1,1,1) ), f - vec3(1,1,1) ), u.x), u.y), u.z );
}