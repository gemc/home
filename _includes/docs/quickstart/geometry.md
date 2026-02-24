## Build the geometry

Inside the `counter` directory, run `counter.py` to create the geometry and materials databases:

```shell
./counter.py
```

You should see the following output:

<pre>
  ❖ Database file gemc.db does not exist
  ❖ Created new SQLite database: gemc.db

  ❖  GConfiguration for experiment &lt;example&gt;,  system &lt;counter&gt; : 
	▪︎ Factory: sqlite         
	▪︎ SQLite File: gemc.db
	▪︎ (Variation, Run): (default, 1)
	▪︎ Number of volumes: 2
	▪︎ Number of materials: 2
</pre>

By default, the `sqlite` factory is used, so an the file `gemc.db` is been created containing the geometry and materials. 

The geometry is created for run number 1 and variation `default`, using . 
Use `-h` to see other options for the factory, run number and variations.

<br/>