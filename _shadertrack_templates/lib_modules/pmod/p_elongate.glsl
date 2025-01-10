void pElongate(inout float p, float h){
	p = p-clamp(p,-h,h);
}