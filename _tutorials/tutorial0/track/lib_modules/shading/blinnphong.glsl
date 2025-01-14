float BlinnPhong(float shininess, vec3 n, vec3 vd, vec3 ld) {
  vec3 h = normalize(-vd + ld);
  return pow(max(0., dot(h, n)), shininess);
}
