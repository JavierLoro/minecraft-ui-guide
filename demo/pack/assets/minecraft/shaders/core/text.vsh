#version 330
#extension GL_ARB_separate_shader_objects : require

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
#include <minecraft:fog.glsl>
#include <minecraft:sample_lightmap.glsl>
#endif

#include <minecraft:dynamictransforms.glsl>
#include <minecraft:projection.glsl>

layout(location = 0) in vec3 Position;
layout(location = 1) in vec4 Color;
layout(location = 2) in vec2 UV0;
#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
layout(location = 3) in ivec2 UV2;
#endif

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
uniform sampler2D Sampler2;
layout(location = 0) out float sphericalVertexDistance;
layout(location = 1) out float cylindricalVertexDistance;
#endif

layout(location = 2) out vec4 vertexColor;
layout(location = 3) out vec2 texCoord0;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
    sphericalVertexDistance = fog_spherical_distance(Position);
    cylindricalVertexDistance = fog_cylindrical_distance(Position);
    vertexColor = Color * sample_lightmap(Sampler2, UV2);
#else
    vertexColor = Color;
#endif
    texCoord0 = UV0;

    // Taller: opt-in bossbar anchor. The compositor always advances exactly 160 GUI pixels.
    // Main markers: #FA02F0 (white), #FA02E0 (teal). Also move their vanilla 25% shadows.
    #ifdef IS_GUI
    ivec3 marker = ivec3(round(Color.rgb * 255.0));
    bool mainMarker = marker.r == 250 && marker.g == 2 && (marker.b == 240 || marker.b == 224);
    bool shadowMarker = (marker.r == 62 || marker.r == 63) && (marker.g == 0 || marker.g == 1) && (marker.b == 60 || marker.b == 56);
    if (mainMarker || shadowMarker) {
        float guiWidth = 2.0 / ProjMat[0][0];
        vec3 anchored = Position;
        anchored.x += 12.0 - (guiWidth - 160.0) * 0.5;
        anchored.y += 5.0;
        gl_Position = ProjMat * ModelViewMat * vec4(anchored, 1.0);
        bool teal = marker.b == 224 || marker.b == 56;
        vec3 palette = teal ? vec3(81.0, 212.0, 203.0) / 255.0 : vec3(1.0);
        vertexColor = vec4(palette * (shadowMarker ? 0.25 : 1.0), Color.a);
    }
    #endif

}
