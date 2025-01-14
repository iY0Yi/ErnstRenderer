vec3 sub_mix(vec3 colA, vec3 colB, float factor)
{
    // 1) インク空間に変換 (InkSpace = 1 - Color)
    vec3 inkA = 1.0 - colA;
    vec3 inkB = 1.0 - colB;

    // 2) インク空間で通常の線形補間
    //    factor=0.0 → inkA,  factor=1.0 → inkB
    vec3 inkMix = mix(inkA, inkB, factor);

    // 3) 発光色空間に戻す (Color = 1 - Ink)
    //    factor=0.0 → colA,  factor=1.0 → colB
    return 1.0 - inkMix;
}