<blockquote class="doc-important" markdown="1">

**gstreamer**

The `gstreamer` option allows select the name and format of the output.
Run `gemc help gstreamer` to check its documentation:
	
	-gstreamer=<sequence> ......: define a gstreamer output
	
	• filename: name of output file. Default value: NODFLT
	• format: format of output file. Default value: NODFLT
	• type: type of output fileDefault value: event


	Define output formats and filenames. 
	It can be used to select <events> or <frame> streams.
	The file extension is added automatically based on the format.

	Supported formats:
		
      - jlabsro
	  - root
	  - ascii
	  - csv
	  - json
	

	Output types:

	  - event: write events
	  - stream: write frame time snapshots
	
	Example that defines two gstreamer outputs:

	 -gstreamer="[{format: root, filename: out}, {format: csv, filename: out}]"
	

	The produced files structure depends on the accumulation method used:

	  - event-based digitization (like <flux>) will have one file for every j 
	    thread, with "_tj" appended to the filename
	  - run-based digitization (like <dosimeter>) will have one file only

</blockquote>

