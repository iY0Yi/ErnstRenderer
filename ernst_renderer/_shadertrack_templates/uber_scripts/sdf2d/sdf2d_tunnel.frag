vec2 s = dim;
float r = (trp.z < 0.) ? 0. : s.x;
vec2 q = abs(trp.xz) - s.xy + r;
td = min(max(q.x, q.y), 0.) + length(max(q, 0.)) - r;
