//------------------------------------------------------
// 1) RGB → RYB の変換
//------------------------------------------------------
vec3 rgb2ryb(vec3 rgb_color) {
    // Remove the white from the color
    float white = min(min(rgb_color.r, rgb_color.g), rgb_color.b);
    rgb_color -= vec3(white);

    float max_green = max(max(rgb_color.r, rgb_color.g), rgb_color.b);

    // Get the yellow out of the red & green
    float yellow = min(rgb_color.r, rgb_color.g);
    rgb_color.r -= yellow;
    rgb_color.g -= yellow;

    // If there's leftover in both b & g, halve them (avoid exceeding range)
    if (rgb_color.b > 0. && rgb_color.g > 0.) {
        rgb_color.b /= 2.;
        rgb_color.g /= 2.;
    }

    // Redistribute the remaining green
    yellow += rgb_color.g;
    rgb_color.b += rgb_color.g;

    // Normalize to values
    float max_yellow = max(max(rgb_color.r, yellow), rgb_color.b);
    if (max_yellow > 0.) {
        float n = max_green / max_yellow;
        rgb_color.r *= n;
        yellow     *= n;
        rgb_color.b *= n;
    }

    // Add the white back in
    rgb_color.r += white;
    yellow      += white;
    rgb_color.b += white;

    return vec3(rgb_color.r, yellow, rgb_color.b);
}

//------------------------------------------------------
// 2) RYB → RGB の変換
//------------------------------------------------------
vec3 ryb2rgb(vec3 ryb_color) {
    // Remove the white
    float white = min(min(ryb_color.r, ryb_color.g), ryb_color.b);
    ryb_color -= vec3(white);

    float max_yellow = max(max(ryb_color.r, ryb_color.g), ryb_color.b);

    // Get the green out of the yellow & blue
    float green = min(ryb_color.g, ryb_color.b);
    ryb_color.g -= green;
    ryb_color.b -= green;

    if (ryb_color.b > 0. && green > 0.) {
        ryb_color.b *= 2.;
        green       *= 2.;
    }

    // Redistribute the remaining yellow
    ryb_color.r += ryb_color.g;
    green       += ryb_color.g;

    // Normalize
    float max_green = max(max(ryb_color.r, green), ryb_color.b);
    if (max_green > 0.) {
        float n = max_yellow / max_green;
        ryb_color.r *= n;
        green       *= n;
        ryb_color.b *= n;
    }

    // Add white back
    ryb_color.r += white;
    green       += white;
    ryb_color.b += white;

    return vec3(ryb_color.r, green, ryb_color.b);
}

//------------------------------------------------------
// 3) RYBで混色しつつ、明度をブレンドする関数
//    （mainImageのロジックをまとめたもの）
//------------------------------------------------------
vec3 ryb_mix(vec3 colA, vec3 colB, float factor)
{
    // 3-1) 明度を計算するための行列 M
    //      (mainImage内で mat3(0.241,0,0, 0,0.691,0, 0,0,0.068) )
    //      参考: BT.601 や近い係数から派生したもの
    mat3 M = mat3( 0.241, 0.0,   0.0,
                   0.0,   0.691, 0.0,
                   0.0,   0.0,   0.068);

    // 3-2) 各色の「明度」(b1, b2) を計算
    float bA = sqrt(dot(colA, M * colA));
    float bB = sqrt(dot(colB, M * colB));

    // 3-3) RGB→RYBへ変換後に線形補間
    vec3 rybA = rgb2ryb(colA);
    vec3 rybB = rgb2ryb(colB);
    vec3 rybMixed = mix(rybA, rybB, factor);

    // 3-4) いったんRYB→RGBに戻して、混色後の明度を計算
    vec3 rgbMixed = ryb2rgb(rybMixed);
    float bMixed   = sqrt(dot(rgbMixed, M * rgbMixed));

    // 3-5) 最終的な明度を (bA,bB) から factor で補間
    float bFinal = mix(bA, bB, factor);

    // 3-6) bMixed が 0 でなければ、RYB上でスケールして明度を合わせる
    if (bMixed > 1e-6) {
        rybMixed *= (bFinal / bMixed);
    }

    // 3-7) 再度 RYB → RGB へ変換して返す
    return ryb2rgb(rybMixed);
}
