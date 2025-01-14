float sdArc(vec2 p, vec2 sc, float ra, float rb){
  // sc is the sin/cos of the arc's aperture
  p.x = abs(p.x);
  return ((sc.y*p.x>sc.x*p.y) ? length(p-sc*ra) : 
                abs(length(p)-ra)) - rb;
}