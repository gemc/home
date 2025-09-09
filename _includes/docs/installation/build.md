
# Build and Install GEMC from Source

Please see the [GEMC/Geant4 Software Prerequisites](#gemc-and-geant4-software-prerequisites) in the appendix for the requirements.

<br/>

## Obtaining the source 

For illustration only, we will use  `{{ page.path_prefix }}` as the installation location, and `{{ page.latest_tag }}` as the version to be installed.

Create a `source` sub-dir in the installation location and cd into it:

```bash
mkdir -p {{ page.path_prefix }}/{{ page.latest_tag }}/source
cd {{ page.path_prefix }}/{{ page.latest_tag }}/source
```

There are two approaches:

{% capture tab1 %}
Download the latest release:
```bash
cd {{ page.path_prefix }}/{{ page.latest_tag }}/source
wget {{ page.repo_link }}/{{ page.latest_tag }}.tar.gz
tar -xvzf {{ page.latest_tag }}.tar.gz --strip-components=1
```
{% endcapture %}

{% capture tab2 %}
At your own risk, clone the repository to get the development version. The directory must be empty.
```bash
git clone --depth=1 https://github.com/gemc/src .
```
{% endcapture %}

{% include tabs.html 
   tab1_title="Release Download" tab1_content=tab1
   tab2_title="Git Clone" tab2_content=tab2
%}






<br/>

## Compile and install GEMC

The [meson build system](https://mesonbuild.com) is used to compile and install GEMC. 
A `build` directory is used:


```bash
meson setup build --native-file=core.ini --prefix={{ page.path_prefix }}/{{ page.latest_tag }}
meson compile -C build
meson install -C build
```

- The setup phase will check for the required dependencies and fetch external libraries.
- The compile phase will build the code using all your available CPU cores. Use `-jN` to limit the number of cores used.
- The install phase will copy the binaries, libraries, and python modules to the installation directory.

<br/>

#### Build Options

- Use `-v` at build time to log the compiler commands
- `meson test -v` will run several tests of various components of GEMC and also create a database with the examples geometries.
- To wipe out the build directory and start over, use `rm -rf build` and then re-run the commands above.


<br/>



## Post Installation 
Add the `bin` and `api` directories to your `PATH` and `PYTHONPATH` environment variables.

```bash
export GEM_VERSION={{ page.latest_tag }}
export PATH={{ page.path_prefix }}/$GEM_VERSION/bin:$PATH
export PYTHONPATH={{ page.path_prefix }}/$GEM_VERSION/api:$PYTHONPATH
```

You can add the lines above to your shell configuration file (e.g. `~/.bashrc` or `~/.zshrc`), and use
`$GEMC_VERSION` to control the version of GEMC you want to use.




