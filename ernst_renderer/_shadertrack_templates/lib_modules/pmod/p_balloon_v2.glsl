void pBalloonV2(inout vec2 p, float k){
	p-=normalize(p)*k;
}