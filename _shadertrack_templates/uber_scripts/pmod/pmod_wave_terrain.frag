@CP.y -= (gfbm(@CP.xz*vec2(.005)+vec2(100), 3, .65)-.5)*160. * smoothstep(550., 850., @CP.z);
@CP.y -= gfbm(@CP.xz*vec2(.025), 7, .65)*30. * smoothstep(550., 850., @CP.z);
