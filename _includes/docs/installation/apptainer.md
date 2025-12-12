
{% include mynotes.html %}

## Run GEMC using Apptainer


Linux host can use `apptainer` (formally `singularity`) to run docker containers. 
You can use it with the docker images above.  It runs similarly to docker:


```

apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash

```

<br/>

> Apptainer uses a default cache directory to store the images. If that becomes full, one can use
> environment variables to point to a location with enough disk space.
> For example, to point to `/path/to/$USER/cache`:

```bash
	export sif_cache=/path/to/$USER/cache
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

> Then run apptainer again.




