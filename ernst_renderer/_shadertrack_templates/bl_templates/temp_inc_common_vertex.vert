#version 430
in vec3 position;
uniform vec2 iResolution;
void main() {
  vec3 pos = position;
  pos.xy -= iResolution.xy * .5;
  gl_Position = vec4(pos, 1.);
}
