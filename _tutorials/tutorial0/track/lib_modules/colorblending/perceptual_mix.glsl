// ------------------------------
// 1)  sRGB → リニア変換 (0~1 の範囲)
// ------------------------------
float srgb_to_lin(float c)
{
    return (c <= 0.04045)
        ? (c / 12.92)
        : pow((c + 0.055) / 1.055, 2.4);
}

vec3 from_sRGB(vec3 col)
{
    return vec3(
        srgb_to_lin(col.r),
        srgb_to_lin(col.g),
        srgb_to_lin(col.b)
    );
}

// ------------------------------
// 2)  リニア → sRGB 変換 (0~1 の範囲)
// ------------------------------
float lin_to_srgb(float c)
{
    return (c <= 0.0031308)
        ? (12.92 * c)
        : (1.055 * pow(c, 1.0/2.4) - 0.055);
}

vec3 to_sRGB(vec3 col)
{
    return vec3(
        lin_to_srgb(col.r),
        lin_to_srgb(col.g),
        lin_to_srgb(col.b)
    );
}

// ------------------------------
// 3)  Markさんのアルゴリズムで 色A/色B を知覚的に混色
//     (0~1 sRGB空間の色を補間)
// ------------------------------
vec3 perceptual_mix(vec3 colA, vec3 colB, float factor)
{
    // 3-1) sRGB -> リニア
    vec3 linA = from_sRGB(colA);
    vec3 linB = from_sRGB(colB);

    // 3-2) ガンマ (0.43) を使った「擬似的な知覚的明るさ」
    //      → sum(linA)^(gamma)
    float gamma     = 0.43;
    float brightA   = pow(linA.r + linA.g + linA.b, gamma);
    float brightB   = pow(linB.r + linB.g + linB.b, gamma);

    // 3-3) 明るさを factor で線形補間 → perceptualIntensity
    float perceptualIntensity = mix(brightA, brightB, factor);
    float targetIntensity     = pow(perceptualIntensity, 1.0 / gamma);

    // 3-4) リニアRGB そのものも補間
    vec3 mixedLin = mix(linA, linB, factor);

    // 3-5) 補間後の合計
    float sumC = mixedLin.r + mixedLin.g + mixedLin.b;
    if(sumC > 1e-10) {
        // (目標明度 / 実際の合計) でスケール
        mixedLin *= (targetIntensity / sumC);
    }

    // 3-6) リニア -> sRGB に戻して返す
    return to_sRGB(mixedLin);
}
