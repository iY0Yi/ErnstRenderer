// https://postd.cc/understanding-perlin-noise/
float gnoise(in vec2 st) {
  st *= .75;
  vec2 i = floor(st);
  vec2 f = fract(st);

  vec2 u = smoothstep(0., 1., f);

  vec2 rnd_x0y0 = u2s(hash22(i + vec2(0, 0)));
  vec2 rnd_x1y0 = u2s(hash22(i + vec2(1, 0)));
  vec2 rnd_x0y1 = u2s(hash22(i + vec2(0, 1)));
  vec2 rnd_x1y1 = u2s(hash22(i + vec2(1, 1)));

  vec2 dir_x0y0 = st - (i + vec2(0, 0));
  vec2 dir_x1y0 = st - (i + vec2(1, 0));
  vec2 dir_x0y1 = st - (i + vec2(0, 1));
  vec2 dir_x1y1 = st - (i + vec2(1, 1));

  float dot_x0y0 = dot(rnd_x0y0, dir_x0y0);
  float dot_x1y0 = dot(rnd_x1y0, dir_x1y0);
  float dot_x0y1 = dot(rnd_x0y1, dir_x0y1);
  float dot_x1y1 = dot(rnd_x1y1, dir_x1y1);

  float res_x = mix(dot_x0y0, dot_x1y0, u.x);
  float res_y = mix(dot_x0y1, dot_x1y1, u.x);
  return s2u(mix(res_x, res_y, u.y) * 2.);
}
