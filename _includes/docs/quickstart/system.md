
## Create a system

Create a `counter` system:

```shell 
system_template.py -s counter
```

You should see the following output:

<pre>
 Writing files for experiment &gt;examples&lt;, system template &gt;counter&lt; using variations &gt;['default']&lt;:

  - counter.py
  - geometry.py
  - materials.py
  - README.md

  - Variations defined in counter.py:
    * default
</pre>

This created a subdir called `counter` containing python templates for the system geometry and materials. 
The files are already configured to create the geometry with a target and a flux detector. 
By default, a `yaml` card is provided to shoot protons at the target.

Use `-h` to see other options for `system_template.py`.

<br/>