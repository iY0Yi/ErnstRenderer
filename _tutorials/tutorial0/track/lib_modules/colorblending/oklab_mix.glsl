// oklab - optimized color mix by iq
// https://www.shadertoy.com/view/ttcyRS
vec3 oklab_mix( vec3 colA, vec3 colB, float h ){
    // https://bottosson.github.io/posts/oklab
    const mat3 kCONEtoLMS = mat3(
         0.4121656120,  0.2118591070,  0.0883097947,
         0.5362752080,  0.6807189584,  0.2818474174,
         0.0514575653,  0.1074065790,  0.6302613616);
    const mat3 kLMStoCONE = mat3(
         4.0767245293, -1.2681437731, -0.0041119885,
        -3.3072168827,  2.6093323231, -0.7034763098,
         0.2307590544, -0.3411344290,  1.7068625689);

     colA = sat(colA);
     colB = sat(colB);
    // rgb to cone (arg of pow can't be negative)
    vec3 lmsA = pow( sat(kCONEtoLMS*colA)+1e-6, vec3(1.0/3.0) );
    vec3 lmsB = pow( sat(kCONEtoLMS*colB)+1e-6, vec3(1.0/3.0) );
    // lerp
    vec3 lms = mix( lmsA, lmsB, h );
    // gain in the middle (no oaklab anymore, but looks better?)
 // lms *= 1.0+0.2*h*(1.0-h);
    // cone to rgb
    return kLMStoCONE*(lms*lms*lms);
}