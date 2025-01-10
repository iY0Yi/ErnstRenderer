// Just a copy from https://www.shadertoy.com/view/Msf3WH
float snoise(in vec2 st) {
  st *= .45;  // adjust scale
  const float K1 = 0.366025404;  // (sqrt(3)-1)/2;
  const float K2 = 0.211324865;  // (3-sqrt(3))/6;

  vec2 i = floor(st + (st.x + st.y) * K1);
  vec2 a = st - i + (i.x + i.y) * K2;
  float m = step(a.y, a.x);
  vec2 o = vec2(m, 1.0 - m);
  vec2 b = a - o + K2;
  vec2 c = a - 1.0 + 2.0 * K2;
  vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
  vec3 n = h * h * h * h * vec3(dot(a, u2s(hash22(i + 0.0))), dot(b, u2s(hash22(i + o))), dot(c, u2s(hash22(i + 1.0))));
  return s2u(dot(n, vec3(70.0))) * 1.1;
}
