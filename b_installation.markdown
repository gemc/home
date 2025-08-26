---
layout: default
title: Installation
gemc_latest_docker_tag: jeffersonlab/gemc3:1.1-fedora36

---

{% include mynotes.html %}


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

# Local installation through compilation[^3]

<br/>

Download the common environment and installation repo 
[ceInstall](https://github.com/jeffersonlab/ceInstall) 
to an installation location (for example: `/opt/sim`)

```
  git clone https://github.com/jeffersonlab/ceInstall
  module use ceInstall/modules
  module load sim_system
```

```
install_gemc 3.0
```

This will install gemc and the  [sci-g](https://github.com/gemc/sci-g)  python api.

#### Put in your .bashrc/.zshrc/.tcshrc file to load the env at login:

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
[^3]: tested on macOS Ventura, Linux Fedora 36
