#include bl_modules/bl_inc_common.glslinc

// Curvature
// ---------------------------------------------------------------------
// "Screen Space Curvature Shader" by Evan Wallace:
// http://madebyevan.com/shaders/curvature/
vec2 calcCurvature(vec3 n, vec2 fragCoord, vec2 f) {
  vec3 dx = getNormal(fragCoord + vec2(-1, 0)) - getNormal(fragCoord + vec2(+1, 0));
  vec3 dy = getNormal(fragCoord + vec2(0, -1)) - getNormal(fragCoord + vec2(0, +1));
  vec3 difx = cross(n + dx, n - dx);
  vec3 dify = cross(n + dy, n - dy);
  float dif = difx.y - dify.x;
  return clamp(vec2(dif, -dif) * f, 0., 1.);
}

// ---------------------------------------------------------------------
void mainImage( out vec4 fragColor, vec2 fragCoord){
  fragCoord /= ERNST_RENDER_SCALE;

  vec2 uv = fragCoord.xy / iResolution.xy;
  vec2 cuv = uv;
  float ml = (min(iResolution.x, iResolution.y) == iResolution.x) ? 1. : iResolution.y / iResolution.x;
  cuv = (cuv * 2. - 1.) * ml;
  cuv.x *= iResolution.x / iResolution.y;
  init();
  camera(cuv);
  unpackRenderData(fragCoord);
  
  vec3 n = renDat.normal;
  // Compute surface properties
  vec2 curvature = calcCurvature(n, fragCoord, vec2(.15, 5));
  float corrosion = clamp(-curvature.x * 6.0, 0.0, 1.0);
  float shine = clamp(curvature.x * 3.0, 0.0, 1.0);
  float dirt = clamp(0.25 - curvature.x * 4.0, 0.0, 1.0);
  vec3 light = normalize(vec3(0.0, 1.0, 10.0));
  vec3 ambient = vec3(0.098, 0.1216, 0.1059) * 1.5;
  vec3 diffuse = mix(mix(vec3(0.149, 0.3804, 0.2549) * .5, vec3(0.0, 0.1216, 0.1137) * .5, corrosion), vec3(0.9608, 1.0, 0.4275) * .9, shine) - ambient;
  // if (distance(renDat.albedo, MAT_DEBUG_FONTS_COL) < .01)diffuse = MAT_DEBUG_FONTS_COL;
  // vec3 diffuse = mix(mix(renDat.albedo, renDat.albedo * .1, corrosion), vec3(0.9961, 1.0, 0.9569) * .5, shine) - ambient;
  vec3 specular = mix(vec3(1) - ambient, vec3(0.0), dirt);
  float shininess = 256.0;
  #if 0 
        if (distance(getAlbedo(fragCoord), MAT_DEBUG_FONTS_COL) < .01)
          diffuse = MAT_DEBUG_FONTS_COL;
  #endif
  // Compute final color
  float cosAngle = dot(n, light);
  fragColor.rgb = ambient +
    diffuse * max(0.0, cosAngle) +
    specular * pow(max(0.0, cosAngle), shininess)*renDat.shadow;
  fragColor.rgb *= sat(u2s(renDat.diffuse))*renDat.shadow+pow(renDat.ao, 1.)*.5;
  fragColor.rgb = pow(sat(fragColor.rgb), vec3(.4545));
  if (renDat.depth > .9)fragColor.rgb = vec3(0.1922, 0.1804, 0.1804);
  fragColor.a = 1.;
}
