void pTwist(inout vec3 p, float k){
	float r=p.y*k;
	pRot(p.xz, r+PI*.5);
}