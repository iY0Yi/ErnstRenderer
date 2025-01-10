void mainImage(out vec4 fragColor, vec2 fragCoord);
void main() {
  vec4 color = vec4(1);
  mainImage(color, gl_FragCoord.xy);
  outColor = color;
}
