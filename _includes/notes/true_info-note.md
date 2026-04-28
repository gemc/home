<blockquote class="doc-important" markdown="1">

**True Information**

The true information information is processed by GEMC and in certain instances
averaged (weighted by the energy deposition if present); in others, 
like `pid`, `tid` or `processName`, the data come from the first step in the hit.

The complete list of variables are:

- the sensitive element `identifier`, assigned by the user. For example
  - sector
  - layer
- `hitn`: hit number
- `pid`: particle id
- `tid`: track id
- `avgTime`: average time 
- `avglx`: average local x position
- `avgly`: average local y position
- `avglz`: average local z position
- `avgx`: average global x position
- `avgy`: average global y position
- `avgz`: average global z position
- `totalEDeposited`: total energy deposited 
- `processName`: process name creating the first step of this hit

</blockquote>