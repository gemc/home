## Run gemc

Use the `counter.yaml` steering card and run `GEMC` in interactive mode:

```shell
gemc counter.yaml -gui
```

You will see the gemc GUI window. Click on the `Run` button (green triangle) to start the simulation. You should see a few particles 
being generated and crossing the flux box, producing red hits.

{% include figure.html
   src="assets/images/documentation/quickstart.png"
   alt="The quickstart example"
   caption="A proton beam impinging on an epoxy target. The flux box collects hits from all particles crossing it."
   width="1000"
%}


