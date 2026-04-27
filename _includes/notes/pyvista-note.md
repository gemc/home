> **NOTE**
>
> Pass `-h` for additional command line options:
>
	options:
	  -h, --help            show this help message and exit
	  -f, --factory FACTORY
							ascii, sqlite
	  -v, --variation VARIATION
                            Set variation name
	  -r, --run RUN         Set run number
	  -sql, --dbhost DBHOST
                            SQLite filename or MYSQL host
	  -pv, --pyvista        Show geometry using pyvista (needs pyvista)
	  -pvb, --pvb, --pyvista-background
                            Use PyVista BackgroundPlotter (needs pyqt6 pyvistaqt)
	  -pvw, --width WIDTH   Set plotter width
	  -pvh, --height HEIGHT
							Set plotter height
	  -pvx, --x X           Set plotter x position
	  -pvy, --y Y           Set plotter y position
	  -axes, --add_axes_at_zero
>
> If you have `pyvista` (see also [install pyvista](/home/installation/#install-pyvista)), 
> you can use the `-pv` and `-pvb` options to display the setup without having to run GEMC
{: .doc-important }
 