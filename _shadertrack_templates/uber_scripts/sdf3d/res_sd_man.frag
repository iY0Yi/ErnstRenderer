float domain = 7.;
vec3 numRep = vec3(121,61,401);
trp.z-=numRep.z*domain*.5;
vec3 cellCenter = floor(trp/domain)*domain + .5*domain;
vec3 offsetToNearestNeighbourCell = face(trp/domain - cellCenter)*domain;
vec3 neighbourCellCenter = cellCenter + offsetToNearestNeighbourCell;
vec4 rnd = hash43(cellCenter);
vec3 cp = trp;//mod(trp, vec3(domain))-vec3(domain)*.5;
// cp.y-=numRep.y*2.*domain - 200.;
// pRot(cp.xz, PI*.25);
pRepLim(cp.x, domain, numRep.x);
pRepLim(cp.y, domain, numRep.y);
pRepLim(cp.z, domain, numRep.z);
vec3 np = trp - neighbourCellCenter;
vec3 nq = max(abs(np)-vec3(domain*.48), 0.);
vec4 worst = vec4(length(nq), MAT_VOID);
if(rnd.w>.98){
    cp+=(rnd.xyz)*domain*.25;
    pRot(cp.xz, rnd.x*PI*2.);
    cp+=vec3(0,1.8,0);
    vec4 resMan = sdMan(cp);
    worst = bUni(resMan, worst);
}
// worst.x = max(worst.x, -trp.z);
res = bUni(worst, res);
