vec3 s = dim;
float r = (trp.y < 0.) ? 0. : s.x;
vec2 q = abs(trp.xy) - s.xy + r;
td = min(max(q.x, q.y), 0.) + length(max(q, 0.)) - r;
vec2 w = vec2(td, abs(trp.z) - s.z);
td = min(max(w.x, w.y), 0.) + length(max(w, 0.));
