td = sdEllipsoid(trp, dim);
td -= (u2s(1. - vrn1)) * 6.;
float disp = u2s(vrn2 + vrn3 + vrn4 + vrn5) * 5.;
td -= disp;
td *= .8;
