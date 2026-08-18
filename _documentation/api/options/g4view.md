---
layout: default
title: 'GEMC option: g4view'
---

# `g4view`

Type: `option`

Description: Defines the geant4 viewer properties

Generated from:

```sh
gemc help g4view
```

```text
-g4view=<sequence> .........: Defines the geant4 viewer properties

   • driver: Geant4 visualization driver. See the detailed help for driver tradeoffs. Default value: TOOLSSG_QT_GLES
   • dimension: Geant4 viewer dimensionDefault value: 800x800
   • position: Geant4 viewer positionDefault value: -400+100
   • segsPerCircle: Number of segments per circleDefault value: 100
   • background: Geant4 viewer background color as '<red> <green> <blue>'Default value: 0 0.07059 0.16863
   • cloudPoints: Number of points used for cloud volume renderingDefault value: 1000


   Defines the Geant4 viewer properties:
   - screen dimensions
   - screen position
   - resolution in terms of segments per circle
   
   - viewer background color as '<red> <green> <blue>'
   - number of cloud points for cloud volume rendering
   
   Viewer drivers (interactive-driver availability depends on the Geant4 build and platform):
   - ASCIITree (ATree): writes the geometry hierarchy as text; headless, but not graphical.
   - DAWNFILE (DAWNFILE): exports for high-quality DAWN rendering; external DAWN is required.
   - RayTracer (RT): software ray tracing to JPEG; realistic, but slower and not interactive.
   - VRML2FILE (VRML2FILE): exports a portable 3D scene for an external VRML viewer.
   - gMocrenFile (gMocrenFile): exports medical volume data for the specialized gMocren viewer.
   - TOOLSSG_OFFSCREEN (TSG_OFFSCREEN, TSG_FILE): headless image/vector output for batch jobs.
   - OpenGLImmediateQt (OGLIQt, OGLI): Qt/OpenGL with low scene memory, but slower redraws.
   - OpenGLStoredQt (OGLSQt, OGLS): Qt/OpenGL with fast redraw and picking; uses more memory.
   - OpenGLImmediateX (OGLIX, OGLIQt_FALLBACK): X11/OpenGL immediate mode; requires X.
   - OpenGLStoredX (OGLSX, OGLSQt_FALLBACK): fast X11/OpenGL redraw; uses more memory.
   - RayTracerX (RTX): ray-traced JPEG plus an X window; high quality, but slow and X-only.
   - TOOLSSG_X11_GLES (TSG_X11_GLES, TSGX11, TSG_QT_GLES_FALLBACK): interactive X11/GLES; avoids Qt, but requires an X server and GLES support.
   Examples:
   
   -g4view="[{dimension: 1200x1000}]"
   -g4view="[{driver: OGL, dimension: 1100x800, position: +200+100, segsPerCircle: 100, background: 0 0.07059 0.16863}]"
   -g4view="[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200, cloudPoints: 3000}]" takes a screenshot at the end of each run
```
