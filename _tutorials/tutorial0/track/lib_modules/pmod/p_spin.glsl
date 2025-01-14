void pSpin(inout vec3 p){
	p=vec3(length(p.xz), p.y, 0);
}