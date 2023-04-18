---
layout: default
title: Native geant4 solid types builders
description: use python to create volumes based on geant4 solids
---
This document describes how to use python to build the volumes described in the <a href="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Detector/Geometry/geomSolids.html">Geant4 User Guide</a><br/><br/>
The volumes are built within a system using the python interface. <br/>
<br/><br/>Each geant4 solid's constructor is documented below.<br/><br/>
<table style="width:60% ">
<tr>
</tr>
<tr>
    <td><a href="#G4Box">G4Box</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aBox.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4Tubs">G4Tubs</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTubs.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4Cons">G4Cons</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aCons.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4Trd">G4Trd</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrd.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
</tr>
<tr>
    <td><a href="#G4TrapRAW">G4TrapRAW</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4TrapG">G4TrapG</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/wTrap.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4Trap8">G4Trap8</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4Trap">G4Trap</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
</tr>
<tr>
    <td><a href="#G4Sphere">G4Sphere</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aSphere.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
    <td><a href="#G4Polycone">G4Polycone</a>                    <img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aBREPSolidPCone.jpg" style="width: 30px; height: 30px; padding: 0px"/></td>
</tr>
</table><br/><br/>
<h4 id="G4Box">G4Box: <i>Simple Box</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_box(dx, dy, dz, lunit='mm')</b><br/>
		<br/>
		Creates a geant4 Box<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		dx : half length in x<br/>
		dy : half length in y<br/>
		dz : half length in z<br/>
		lunit: length unit (optional; default: mm)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		Creates a box with dx=30mm, dy=40mm, dz=60mm:<br/>
		<br/>
		<p style="font-family:courier;">> make_box(30, 40, 60)</p>
		<br/>
		To print the corresponding code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Box -gvp '30, 40, 60' -silent</p>
		<br/>
		To print the generic code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Box</p>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aBox.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Tubs">G4Tubs: <i>Cylindrical Section or Tube</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_tube(rin, rout, length, phistart, phitotal, lunit1='mm', lunit2='deg')</b><br/>
		<br/>
		Creates a geant4 Cylindrical Section or Tube<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		rin : inner radius<br/>
		rout : outer radius<br/>
		length : tube half length in z<br/>
		phistart : starting phi angle<br/>
		phitotal : total phi angle<br/>
		lunit1: length unit (optional; default: mm)<br/>
		lunit2: angle unit (optional; default: deg)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		Creates a tube with rin=10mm, rout=15mm, length=20mm, phistart=0deg, phitotal=90deg:<br/>
		<br/>
		<p style="font-family:courier;">> make_tube(10, 15, 20, 0, 90)</p>
		<br/>
		To print the corresponding code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Tubs -gvp '10, 15, 20, 0, 90' -silent</p>
		<br/>
		To print the generic code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Tubs</p>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTubs.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Cons">G4Cons: <i>Cone or Conical section</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_cone(rin1, rout1, rin2, rout2, length, phi_start, phi_total, lunit1='mm', lunit2='deg')</b><br/>
		<br/>
		Creates a geant4 Cone or Conical section<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		rin1 : inner radius at -dz<br/>
		rout1 : outer radius at -dz<br/>
		rin2 : inner radius at +dz<br/>
		rout2 : outer radius at +dz<br/>
		length : cone half length in z<br/>
		phi_start : starting phi angle<br/>
		phi_total : total phi angle<br/>
		lunit1: length unit (optional; default: mm)<br/>
		lunit2: angle unit (optional; default: deg)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		Creates a cone with rin1=5mm, rout1=10mm, rin2=20mm, rout2=25mm, length=40mm, phi_start=0deg, phi_total=270deg:<br/>
		<br/>
		<p style="font-family:courier;">> make_cone(5, 10, 20, 25, 40, 0, 270)</p>
		<br/>
		To print the corresponding code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Cons -gvp '5, 10, 20, 25, 40, 0, 270' -silent</p>
		<br/>
		To print the generic code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Cons</p>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aCons.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Trd">G4Trd: <i>Trapezoid</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_trapezoid(dx1, dx2, dy1, dy2, z, lunit='mm')</b><br/>
		<br/>
		Creates a geant4 Trapezoid<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		dx1 : half length in x at -dz<br/>
		dx2 : half-length in x at +dz<br/>
		dy1 : half-length in y at -dz<br/>
		dy2 : half-length in y at +dz<br/>
		z : half-length in z<br/>
		lunit: length unit (optional; default: mm)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		Creates a trapezoid with dx1=30mm, dx2=10mm, dy1=40mm, dy2=15mm, z=60mm:<br/>
		<br/>
		<p style="font-family:courier;">> make_trapezoid(30, 10, 40, 15, 60)</p>
		<br/>
		To print the corresponding code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Trd -gvp '30, 10, 40, 15, 60' -silent</p>
		<br/>
		To print the generic code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4Trd</p>
		<br/>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrd.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4TrapRAW">G4TrapRAW: <i>Generic Trapezoid: right Angular Wedge (4 parameters)</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_trap_from_angular_wedges(pz, py, px, pltx, lunit1='mm')</b><br/>
		<br/>
		Creates a geant4 Generic Trapezoid: right Angular Wedge (4 parameters)<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		pz : Length along Z<br/>
		py : Length along Y<br/>
		px : Length along X at the wider side<br/>
		pltx : Length along X at the narrower side (plTX<=pX)<br/>
		unit: length unit (optional; default: mm)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		TO VERIFY:<br/>
		Creates a trapezoid with pz=30mm, py=40mm, px=50mm, pltx=20mm:<br/>
		<br/>
		<p style="font-family:courier;">> make_trap_from_angular_wedges(30, 40, 50, 20)</p>
		<br/>
		To print the corresponding code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4TrapRAW -gvp '30, 40, 50, 20' -silent</p>
		<br/>
		To print the generic code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4TrapRAW</p>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4TrapG">G4TrapG: <i>Generic Trapezoid: general trapezoid (11 parameters)</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		<br/>
		Function: <b>make_general_trapezoid(pDz, pTheta, pPhi, pDy1, pDx1, pDx2, pAlp1, pDy2, pDx3, pDx4, pAlp2, lunit1='mm', lunit2='deg')</b><br/>
		<br/>
		Creates a geant4 Generic Trapezoid: general trapezoid (11 parameters)<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		pDz: Half Z length - distance from the origin to the bases<br/>
		pTheta: Polar angle of the line joining the centres of the bases at -/+pDz<br/>
		pPhi: Azimuthal angle of the line joining the centre of the base at -pDz to the centre of the base at +pDz<br/>
		pDy1: Half Y length of the base at -pDz<br/>
		pDy2: Half Y length of the base at +pDz<br/>
		pDx1: Half X length at smaller Y of the base at -pDz<br/>
		pDx2: Half X length at bigger Y of the base at -pDz<br/>
		pDx3: Half X length at smaller Y of the base at +pDz<br/>
		pDx4: Half X length at bigger y of the base at +pDz<br/>
		pAlp1: Angle between the Y-axis and the centre line of the base at -pDz (lower endcap)<br/>
		pAlp2: Angle between the Y-axis and the centre line of the base at +pDz (upper endcap)<br/>
		lunit1: length unit (optional; default: mm)<br/>
		lunit2: angle unit (optional; default: deg)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		Creates a trapezoid with pDz=30mm, pTheta=40deg, pPhi=50deg, pDy1=60mm, pDx1=70mm, pDx2=80mm, pAlp1=90deg, pDy2=100mm, pDx3=110mm, pDx4=120mm, pAlp2=130deg:<br/>
		<br/>
		<p style="font-family:courier;">> make_general_trapezoid(30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130)</p>
		<br/>
		To print the corresponding code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4TrapG -gvp '30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130' -silent</p>
		<br/>
		To print the generic code:<br/>
		<br/>
		<p style="font-family:courier;">> scigTemplate.py -gv G4TrapG</p>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/wTrap.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Trap8">G4Trap8: <i>Generic Trapezoid: from eight points (24 parameters)</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		<br/>
		Function: <b>make_trap_from_vertices(v1x, v1y, v1z, v2x, v2y, v2z, v3x, v3y, v3z, v4x, v4y, v4z, v5x, v5y, v5z, v6x, v6y,</b><br/>
		v6z, v7x, v7y, v7z, v8x, v8y, v8z, lunit1='mm')<br/>
		<br/>
		Creates a geant4 Generic Trapezoid: from eight points (24 parameters)<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		v1x, v1y, v1z: Coordinates of the first vertex<br/>
		v2x, v2y, v2z: Coordinates of the second vertex<br/>
		v3x, v3y, v3z: Coordinates of the third vertex<br/>
		v4x, v4y, v4z: Coordinates of the fourth vertex<br/>
		v5x, v5y, v5z: Coordinates of the fifth vertex<br/>
		v6x, v6y, v6z: Coordinates of the sixth vertex<br/>
		v7x, v7y, v7z: Coordinates of the seventh vertex<br/>
		v8x, v8y, v8z: Coordinates of the eighth vertex<br/>
		lunit1: length unit (optional; default: mm)<br/>
		<br/>
		v1, v2 | Edge with smaller Y of the base at -z<br/>
		v3, v4 | Edge with bigger Y of the base at -z<br/>
		v5, v6 | Edge with smaller Y of the base at +z<br/>
		v7, v8 | Edge with bigger Y of the base at +z<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		MISSING, build one<br/>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Trap">G4Trap: <i>Generic Trapezoid: will call the G4Trap constructor based on the number of parameters</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		<br/>
		Function: <b>make_trap(params, lunit1='mm', lunit2='deg')</b><br/>
		<br/>
		Creates a geant4 Generic Trapezoid: will call the G4Trap constructor based on the number of parameters<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		params: list of parameters<br/>
		lunit1: length unit (optional; default: mm)<br/>
		lunit2: angle unit (optional; default: deg)<br/>
		<br/>
		<br/>
		<i><b>Example::</b></i> <br/>

		<br/>
		MISSING, build one<br/>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Sphere">G4Sphere: <i>Sphere or Spherical Shell Section</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_sphere(rmin, rmax, sphi, dphi, stheta, dtheta, lunit1='mm', lunit2='deg')</b><br/>
		<br/>
		Creates a geant4 Sphere or Spherical Shell Section<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		rmin: inner radius<br/>
		rmax: outer radius<br/>
		sphi: starting phi angle<br/>
		dphi: delta phi angle<br/>
		stheta: starting theta angle<br/>
		dtheta: delta theta angle<br/>
		lunit1: length unit (optional; default: mm)<br/>
		lunit2: angle unit (optional; default: deg)<br/>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aSphere.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

<h4 id="G4Polycone">G4Polycone: <i>Polycons</i> </h4>
<div class="align-items-center">
	<p>
		<br/>
		Function: <b>make_polycone(phiStart, phiTotal, zplane, iradius, oradius, lunit1='mm', lunit2='deg')</b><br/>
		<br/>
		Creates a geant4 Polycone<br/>
		<br/>
		<i><b>Parameters:</b></i> <br/>

		<br/>
		phiStart: starting phi angle<br/>
		phiTotal: total phi angle<br/>
		zplane: list of z coordinates<br/>
		iradius: list of inner radii<br/>
		oradius: list of outer radii<br/>
		lunit1: length unit (optional; default: mm)<br/>
		lunit2: angle unit (optional; default: deg)<br/>
		<br/>
		<br/>
		<i><b>Example:</b></i> <br/>

		<br/>
		MISSING, build one<br/>
		<br/>
		<br/>
	</p>
		
	<div>
		<img  src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aBREPSolidPCone.jpg"/>
	</div>
</div>
<hr style="color:black; opacity: 0.8"><br/>

