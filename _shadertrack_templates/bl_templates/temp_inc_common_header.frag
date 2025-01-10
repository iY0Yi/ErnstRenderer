#version 420
#extension GL_ARB_uniform_buffer_object : require
in vec3 pos;
out vec4 outColor;
uniform float iTime;
uniform int iFrame;
uniform vec2 iResolution;
