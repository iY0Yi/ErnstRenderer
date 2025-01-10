float msk0 = smoothstep(550., 850., @CP.z);
float mks1 = smoothstep(.5, .75, gfbm(@CP.xz, 1, .5));
@CP.y -= pow(mountain(@CP.xz*.015+vec2(10,0), .1).x, 2.) * 300. * msk0 * msk1;
