
# Build and Install GEMC from Source


<br/>

## Download the source code 

For illustration only, we will use  `{{ page.path_prefix }}` as the installation location, and `{{ page.latest_tag }}` as the version to be installed.

Create the installation directory and move into a `source` directory to hold the source code:

```bash
mkdir -p {{ page.path_prefix }}/{{ page.latest_tag }}/source
cd {{ page.path_prefix }}/{{ page.latest_tag }}/source
```

Download the latest stable release from GitHub:

```bash
wget {{ page.repo_link }}/{{ page.latest_tag }}.tar.gz
tar -xvzf {{ page.latest_tag }}.tar.gz --strip-components=1
```

Alternatively, at your own risk, clone the repository to get the development version[^source_dir_empty]:
```bash
git clone --depth=1 https://github.com/gemc/src .
```

<br/>

## Compile and install GEMC

The [meson build system](https://mesonbuild.com) is used to compile and install GEMC. Temporary files are stored in a `build` directory.

Inside the source directory:


```bash
meson setup build --native-file=core.ini --prefix={{ page.path_prefix }}/{{ page.latest_tag }}
meson compile -C build
meson install -C build
```

- The setup phase will check for the required dependencies and fetch the external libraries if needed.
- The compile phase will build the code using all your available CPU cores. Use `-jN` to limit the number of cores used.
- The install phase will copy the binaries, libraries, and python modules to the installation directory.

<br/>

#### Build Options

- Use `-v` at build time to log on screen the compiler commands
- To test the build, use `meson test -v`. This will run several tests of various components of GEMC and also create a database with the examples geometries.
- To wipe out the build directory and start over, use `rm -rf build` and then re-run the commands above.


<br/>



## Post Installation 
Add the `bin` and `api` directories to your `PATH` and `PYTHONPATH` environment variables.

```bash
export PATH={{ page.path_prefix }}/{{ page.latest_tag }}/bin:$PATH
export PYTHONPATH={{ page.path_prefix }}/{{ page.latest_tag }}/api:$PYTHONPATH
```

[^source_dir_empty]: The directory must be empty (aside from . and ..) to clone the repository into it
