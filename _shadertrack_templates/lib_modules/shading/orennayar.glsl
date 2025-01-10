float orenNayarDiffuse(vec3 ldir, vec3 vdir, vec3 n, float roughness) {
  float LdotV = dot(ldir, vdir);
  float NdotL = dot(ldir, n);
  float NdotV = dot(n, vdir);

  float s = LdotV - NdotL * NdotV;
  float t = mix(1., max(NdotL, NdotV), step(0., s));

  float sigma2 = roughness * roughness;
  float A = 1. + sigma2 * (1. / (sigma2 + .13) + .5 / (sigma2 + .33));
  float B = .45 * sigma2 / (sigma2 + .09);

  return max(0., NdotL) * (A + B * s / t) / PI;
}
