// "BezierExtrude" by Del:
// https://www.shadertoy.com/view/7dyBz3
// --------------------------------------------------------------------
// returns xyz = position, w = spline position (t)
void sdBezierExtrude(vec3 pos, vec3 A, vec3 B, vec3 C, inout float rest)
{    
    // check for colinear
    //if (abs(dot(normalize(B - A), normalize(C - B)) - 1.0) < 0.0001)
    //    return sdLinearSegment(pos, A, C);

	// first, calc curve T value
    vec3 a = B - A;
    vec3 b = A - 2.0*B + C;
    vec3 c = a * 2.0;
    vec3 d = A - pos;

    float kk = 1.0 / dot(b,b);
    float kx = kk * dot(a,b);
    float ky = kk * (2.0*dot(a,a)+dot(d,b)) / 3.0;
    float kz = kk * dot(d,a);      

    float p = ky - kx*kx;
    float p3 = p*p*p;
    float q = kx*(2.0*kx*kx - 3.0*ky) + kz;
    float h = q*q + 4.0*p3;
	float t;

    if(h >= 0.0) 
    { 
        h = sqrt(h);
        vec2 x = (vec2(h, -h) - q) / 2.0;
        vec2 uv = sign(x)*pow(abs(x), vec2(1.0/3.0));
        t = uv.x+uv.y-kx;
        // 1 root
    }
    else
    {
        float z = sqrt(-p);
        float v = acos( q/(p*z*2.0) ) / 3.0;
        float m = cos(v);
        float n = sin(v)*1.732050808;
        vec3 tt = clamp( vec3(m+m,-n-m,n-m)*z-kx, 0.0, 1.0);
		// 3 roots, but only need two
		vec3 r1 = d + (c + b * tt.x) * tt.x;
		vec3 r2 = d + (c + b * tt.y) * tt.y;
		//t = length(r2.xyz) < length(r1.xyz) ? tt.y : tt.x;
        t = dot(r2,r2) < dot(r1,r1) ? tt.y : tt.x; // quicker
        
    }
    // now we have t, calculate splineposition and orient to spline tangent
    t = clamp(t,0.,1.); // clamp spline start/end
    vec3 ttan = normalize((2.0 - 2.0 * t) * (B - A) + 2.0 * t * (C - B));  // spline tangent
    vec3 up = vec3(0.0, 1.0, 0.0);
    vec3 binormal = normalize(cross(up, ttan));
    vec3 _normal = cross(ttan, binormal);
//	vec3 t1 = normalize(cross(_normal, ttan));
	vec3 t1 = cross(_normal, ttan); // no need to normalize this?
	mat3 mm = mat3(t1, cross(ttan, t1), ttan);
    vec3 tp = mix(mix(A, B, t), mix(B, C, t), t);
    pos.xyz = tp - pos; // spline position
    pos *= mm;
    rest = t;
}