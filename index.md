---
layout: default
---

## A 3D-Image-Flow-Based Metric in Camera Space for Camera Paths in Scenes with Extreme Scale Variations

<div style="text-align:right; margin-bottom:3rem;">
  Lisa Piotrowski<br>
  Michael Motejat<br>
  Christian Rössl<br>
  Holger Theisel
</div>

{% include sharing.html %}

### Abstract

<div style="text-align:justify;">
Interpolation between camera positions is a standard problem in computer graphics 
and can be considered the foundation of camera path planning. 
As the basis for a new interpolation method, we introduce a new Riemannian metric 
in camera space, which measures the 3D image flow under a small movement of the camera. 
Building on this, we define a linear interpolation between two cameras as shortest 
geodesic in camera space, for which we provide a closed-form solution after 
a mild simplification of the metric. 
Furthermore, we propose a geodesic Catmull-Rom interpolant for keyframe camera 
animation. We compare our approach with several standard camera interpolation 
methods and obtain consistently better camera paths especially for cameras with 
extremely varying scales.
</div>

### Resources

- [Author PDF](https://github.com/LivelyLiz/OptFlowCam/blob/assets/paper/optFlowCam.pdf?raw=true)
- [Presentation]() (TBD)
- [Blender Add-On](https://github.com/LivelyLiz/OptFlowCam)
- [Additional Material](https://github.com/LivelyLiz/OptFlowCam/blob/assets/paper/optFlowCam_maple.zip?raw=true)

**Video 1: Results**  
<iframe width="560" height="315" src="https://www.youtube.com/embed/_2oiWZafFb8?si=L4bSyUA4M8fPOcLR" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

**Video 2: Interactive Session**  
<iframe width="560" height="315" src="https://www.youtube.com/embed/gMEZpkAyOB0?si=AKsryRCQUFArHobB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### Cite As

```
TBD
```