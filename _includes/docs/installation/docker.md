# Run GEMC in a Docker Container

You can use docker to run GEMC without having to install it or any of its dependencies.
The available GEMC docker images are listed below.

| Image        | Pull Command                          | VNC Access                          |
|--------------|---------------------------------------|-------------------------------------|
{% for img in site.data.docker.images -%}
| {{ img.label }} | ```docker pull {{ img.tag }}``` | {{ img.vnc_access }} |
{% endfor %}


It is recommended to bind a local directory to save and store your work.
For illustration purposes, below we will bind the image path `{{ page.docker_remote_mount }}`
to the local dir `{{ page.docker_local_mount }}` and we will use the image `{{ site.data.docker.images[0].tag }}`.

For Apple Silicon Mac you may need to add the option `--platform linux/amd64` to the docker commands below.

<br/>

## Run docker in batch mode

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

## Run docker and use a browser for the graphical interface:

```
docker run -it --rm  -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}}  -p 8080:8080 {{ site.data.docker.images[0].tag }}
```

Then point your browser to [`http://localhost:8080/vnc.html`]( http://localhost:8080/vnc.html ) to access the graphical interface.

<br/>



