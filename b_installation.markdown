---
layout: default
title: Installation
gemcv: 3.0beta
gemc_container_tag: jeffersonlab/gemc3:1.0

tables:
  gemcInstallationTypes:
    headers: [Type, OS, Requirements, GUI]
    rows:
      - [
      "Docker",
      "Linux, Mac",
      "<a href=\"https://www.docker.com\">docker</a><br/>",
      "web browser"
      ]
      - [
      "Compilation",
      "Linux Fedora, MacOS Ventura (intel chips)",
      "<a href=\"https://github.com/JeffersonLab/ceInstall\">Common Environment Setup</a><br/>",
      "native OS"
      ]
---


<br/>
<table border="1" width="70%" class="table-info">
	<tr>
		{% for header in page.tables.gemcInstallationTypes.headers %}	
		<th>{{ header }}</th>
		{% endfor %}
	</tr>
	{% for row in page.tables.gemcInstallationTypes.rows %}
		<tr>
			{% for item in row %}
				<td> {{ item }} </td>
			{% endfor %}
		</tr>
	{% endfor %}
</table>

<!--# DMG <a href="https://www.jlab.org/12gev_phys/packages/dmg/gemc-{{ page.gemcv }}.dmg"> <span data-feather="download"></span> </a> -->
<!--After installation use the line below to load the environment. -->
<!-- source /Applications/gemc-{{ page.gemcv }}.app/environment.sh-->
<!---->

# Docker 

Pull the latest image:
```docker pull {{ page.gemc_container_tag }}```

It is recommended to mount a working directory to save store your work.
For example `~/mywork`.

## Run docker in batch mode[^1]:

```
docker run -it --rm -v ~/mywork:/mywork {{ page.gemc_container_tag }} bash
```


## Run docker and use a browser for the graphical interface:

```
docker run -it --rm  -v ~/mywork:/mywork  -p 8080:8080  {{ page.gemc_container_tag }}
```

(*point your browser to http://localhost:8080/vnc.html*)


[//]: # (#### run docker and use vnc[^2] for the graphical interface:)

[//]: # (> docker run -it \-\-rm  -v ~/mywork:/jlab/work/mywork  -p 127.0.0.1:6080:6080  -p 5901:5901 {{ page.gemc_container_tag }})

<br/>

---

<br/>

# Compilation Quickstart[^3]

<br/>

Point the environment variable SIM_HOME to an installation location (for example: `/opt/sim`)

```
  export SIM_HOME=/opt/sim
  mkdir -p $SIM_HOME
  cd $SIM_HOME
  git clone https://github.com/jeffersonlab/ceInstall
  source $SIM_HOME/ceInstall/setup.(c)sh install
  module load gemc3/1.0
```

To install gemc3:

```
install_gemc3 1.0
```

This will install gemc and the  [sci-g](https://github.com/gemc/sci-g)  python api.

#### Put in your .shellrc file to load the env at login:

```
  export SIM_HOME=/opt/sim
  source $SIM_HOME/ceInstall/setup.(c)sh
  module load gemc3/1.0
```


For more details and system requirements check the [Common Environment Install](https://github.com/JeffersonLab/ceInstall) repository.

<br/> <br/> <br/> <br/>

---

[^1]: on linux permissions problems for /var/run/docker.sock may be solved with  ```sudo chmod 666 /var/run/docker.sock```
[^2]: recommended: <a href='https://www.realvnc.com/en/connect/download/viewer/'>realvnc vnc viewer</a>
[^3]: tested on Macos Ventura and Linux Fedora 36
