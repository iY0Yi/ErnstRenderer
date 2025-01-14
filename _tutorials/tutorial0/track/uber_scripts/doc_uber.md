# Uber scripts

Special keywords in Uber scripts.
<br>

### Argument, Inline, Pmod, SDF2d/3d scripts
| name | type | description |
| :--- | :--- | :--- |
|**\$cp** | *vec3* | default domain.|
|**\$cppos** | *vec3* | position value of default domain. **read-only*|
|**\$cprot** | *vec3* | rotation value of default domain. **read-only*|
|**\$cpt** | *vec3* | translated default domain.|
|**\$cptr** | *vec3* | translated/rotated default domain.|
|**\$pp** | *vec3* | parent domain.|
|**\$pppos** | *vec3* | position value of parent domain. **read-only*|
|**\$pprot** | *vec3* | rotation value of parent domain. **read-only*|
|**\$ppt** | *vec3* | translated parent domain.|
|**\$pptr** | *vec3* | translated/rotated parent domain.|
<br>

### Argument scripts
| name | type | description |
| :--- | :--- | :--- |
|**\$var** | *float* | store the result into this.|
<br>

### SDF2d/3d scripts
| name | type | description |
| :--- | :--- | :--- |
|**\$d** | *float* | the variable to store the distance.|
|**\$res** | *vec4* | the variable to store the result.|
|**\$dim** | *vec3* | dimension of ui bound. **read-only*|
|**\$prp** | *vec3* | custom properties. **read-only*|
|**\$tp** | *vec3* | translated default domain.|
|**\$trp** | *vec3* | translated/rotated default domain.|
<br>

### IK scripts
**all variables are read-only.*
| name | type | description |
| :--- | :--- | :--- |
|**\$ika** | *IKArmature* | ik armature structure. |
|**\$ika_base** | *vec3* | domain of root.|
|**\$root_pos** | *vec3* | position value of root bone.|
|**\$pole_pos** | *vec3* | position value of pole bone.|
|**\$target_pos** | *vec3* | position value of target bone.|
|**\$length_a** | *float* | length of root bone.|
|**\$length_b** | *float* | length of ik bone.|
|**\$key_target** | *float* | target position via TRV.|
|**\$key_pole** | *float* | pole position via TRV.|

<!-- https://maasaablog.com/integrated-development-environment/visual-studio-code/1762/ -->

<!-- https://tracpath.com/works/development/markdown_basics/ -->