
# Publicity Strategy by Audience

## Physicists (HEP, nuclear, astrophysics)


- Submit a dedicated paper to Computer Physics Communications (the standard venue for simulation tools) — 
  your EPJ CHEP paper is a conference proc; a full CPC paper gets far more citations and visibility.
- Post to the Geant4 mailing list (geant4-users@cern.ch) — this is the single highest-value action you can take immediately.
- Present at CHEP (next edition), IEEE NSS/MIC, and DPF.
- Submit to INSPIRE-HEP and make sure the record links to the GitHub repo.


## Medical physicists / dosimetry


- The built-in dosimeter sensitive type is a killer feature here. Target the AAPM 
  (American Association of Physicists in Medicine) annual meeting and their journal Medical Physics.
- Reach out to the OpenDosimetry and TOPAS communities — TOPAS users in particular 
  are already comfortable with Python-driven Geant4 wrappers and are a natural overlap.
- Post in the FLUKA and EGSnrc user forums, framing GEMC as a complementary Python-first option.



## Engineers / space / NASA

- NASA's GSFC Radiation Effects group and JPL both run Geant4 simulations for shielding analysis. 
  Contact them directly via their group websites.
- Submit to IEEE Transactions on Nuclear Science, which covers radiation effects engineering.
- Reach the Space Weather community via AGU meetings and the Space Weather journal.
- Post to the NASA Technical Reports Server community and NASA Goddard's simulation listservs if you have contacts there.



# General developers / Python community

- Write a PyPI package or at minimum a pip install wrapper, and ensure GEMC appears in PyPI search results — 
  Python developers will not search GitHub first.
- Post a detailed writeup on Towards Data Science or The Gradient, framing GEMC 
  as "Monte Carlo particle simulation in Python."
- A Real Python or Scientific Python tutorial guest post would reach tens of thousands.


# Specific Sites, People & Publications to Contact

## Mailing lists / forums

- geant4-users@cern.ch — primary Geant4 user list
- geant4-physics@cern.ch — Geant4 physics developers
- TOPAS user forum (topasmc.org)
- ROOT forum (root-forum.cern.ch) — your ROOT output support is directly relevant
- sci.physics.research newsgroup
- Physics Stack Exchange (write a self-answered Q&A: "How do I run Geant4 simulations without knowing C++?")

## Journals to submit to

- Computer Physics Communications (Elsevier) — the #1 venue for simulation software
- SoftwareX (Elsevier) — open-access, specifically for research software
- Journal of Open Source Software (JOSS) — lightweight peer review, high GitHub/PyPI visibility
- Medical Physics — for the dosimetry angle
- Nuclear Instruments and Methods A (NIMA) — classic venue for detector simulation tools

## Specific people / groups to reach

- The Geant4 Collaboration leadership at CERN — they maintain an "Applications and Tools" page and have featured community tools before
- TOPAS developers at MGH/UCSF — natural collaborators/cross-promoters
- OpenMC community (openmc.org) — adjacent Monte Carlo simulation, overlapping audience
- Fermilab and SLAC simulation groups
- ESA's SPENVIS team — they wrap Geant4 for space radiation

## Community aggregators

- Hacker News "Show HN" post — frame it as "I built a Python API for Geant4, no C++ needed"
- Reddit: r/physics, r/Python, r/MachineLearning (for the ML+simulation intersection), r/aerospace
- Awesome Geant4 lists on GitHub (search for them and submit a PR)
- PyOpenSci — they review and promote scientific Python packages

## Conferences

- CHEP (Computing in High Energy Physics)
- IEEE NSS/MIC
- AAPM Annual Meeting
- AGU Fall Meeting (space/atmospheric radiation)
- SciPy Conference — very high Python community visibility

# Website Improvement Suggestions

- Add a "Who uses GEMC?" section early on the homepage with institutional logos (JLab, etc.) — social proof matters.
- Add a 5-minute quickstart as the very first link — lower the time-to-first-simulation dramatically.
- Add a comparison table vs. raw Geant4 and TOPAS showing setup complexity, lines of code, etc.
- Add a Google Analytics / Plausible tracker to understand where visitors come from so you can double down on what works.
- Submit the site to JOSS, PyOpenSci, and the Geant4 Application Database — these will generate inbound links.
- Fix the broken Sanitizer badge link (it reads ttps:// instead of https://).
- Add a comparison page: “When to use GEMC vs raw Geant4 vs GATE vs TOPAS vs GAMOS.”
- Add GitHub topics such as geant4, monte-carlo, particle-transport, detector-simulation, 
  radiation-transport, medical-physics, dosimetry, gdml, cad, pyvista, root, scientific-computing.

# How to Improve Your Original Prompt

- Provide the target audience more explicitly — e.g., "I'm a researcher at JLab, the primary users so 
  far are HEP experimentalists, and I want to expand to medical and aerospace." Context lets me prioritize advice.
- State your constraints — budget (zero? some?), time (one-person project?), 
  existing network (do you have CERN contacts?). This changes the strategy significantly.
- Ask for a prioritized action list, not just a list — "rank these by expected impact per 
  hour spent" yields more actionable output.
- Separate the asks — your prompt bundled 6 distinct questions. Breaking them into separate 
  prompts (one for outreach strategy, one for specific contacts, one for website feedback) gets deeper answers on each.
- Attach examples of similar successful projects — e.g., "TOPAS got wide adoption — what did they do?" 
  gives me a concrete benchmark to work from.

6. Additional Developer Engagement Methods

- Write a Jupyter notebook tutorial and post it to Binder (mybinder.org) so anyone can run GEMC 
  in-browser with zero installation. This is extremely effective for developer adoption.
- Create a Docker Hub "featured" listing — since you already have Docker images, getting 
  a well-written Docker Hub page with a good README dramatically increases organic discovery.
- Record a 10-minute YouTube demo — "Geant4 simulation in 10 minutes with Python." 
  YouTube has a large scientific computing audience and it's permanently findable.
- GitHub Discussions — enable it on your repo and actively answer questions there. 
  Stack Overflow visibility comes from answered questions.
- Write a GEMC plugin/example for a well-known detector (e.g., a simple NaI(Tl) gamma detector) 
  and post it as a standalone repo. People searching for that detector type will find GEMC.
- Reach out to university course instructors who teach Geant4 — a single professor adopting GEMC 
  for a graduate course brings dozens of users per year sustainably.
- Submit to AlternativeTo.net as an alternative to raw Geant4, TOPAS, FLUKA, and EGSnrc — people 
  researching those tools will discover GEMC.
- Zenodo DOI — publish a Zenodo record for each release. This makes the software citable 
  independently of the paper and appears in academic software searches. Add CITATION.cff + Zenodo DOI. 
  Zenodo has GitHub/software integration specifically for archiving GitHub releases and software metadata


# Developer engagement methods

- A 60-second demo GIF: Python geometry → pyvista preview → GEMC run → JSON/ROOT output.
- A “zero Geant4 setup” Docker tutorial.
- A benchmark example against a known Geant4 example, showing that GEMC produces equivalent physics output for a simple geometry.
  1. A “cookbook” folder:
	  - [ ] flux plane
	  - [ ] dosimeter
	  - [ ] particle counter
	  - [ ] magnetic field
	  - [ ] GDML import
	  - [ ] CAD mesh import
	  - [ ] ROOT output
	  - [ ] geometry variations
        - [ ] A contributor-friendly roadmap with small issues labeled:
				- good first issue
				- documentation
				- example
				- physics validation
				- medical physics
				- space radiation
  - Monthly short releases with changelog posts. Publicize small wins repeatedly instead of one big announcement.
  - Cross-link with adjacent projects respectfully: GATE, TOPAS, GAMOS, Geant4-DNA, Scikit-HEP, ROOT, pyvista.
  - Make a GEMC citation badge and put it in the README, docs, and examples.
    - Add a “Who should use GEMC?” page:
		- “I know Python but not Geant4”
		- “I need detector geometry variations”
		- “I need fast geometry iteration without recompilation”
		- “I need ROOT/JSON/CSV output”
		- “I need built-in flux/dose/particle counting”
  - Record a 15-minute YouTube/Indico-style tutorial. Developers are much more likely to try the tool after seeing it run once.

| Target                           | Why it matters                                                                                                                                          | Suggested action                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **CHEP 2026 / future CHEP**      | CHEP is the major computing conference for high-energy and nuclear physics; CHEP 2026 is listed for May 25–29, 2026. ([Indico][1])                      | Submit a proceedings-style paper or poster for the next available cycle.               |
| **PyHEP**                        | PyHEP is an HSF activity for Python in particle physics and welcomes discussion of Python tools for the HEP community. ([hepsoftwarefoundation.org][2]) | Propose a demo talk: “Python-defined Geant4 geometry and detector response with GEMC.” |
| **HSF Training Working Group**   | HSF Training supports software training for researchers in HEP. ([hepsoftwarefoundation.org][3])                                                        | Offer a Carpentries-style lesson: “Geant4 simulation concepts through GEMC.”           |
| **IRIS-HEP Topical Meetings**    | IRIS-HEP topical meetings cover software topics and are usually recorded. ([iris-hep.org][4])                                                           | Propose a topical seminar/demo.                                                        |
| **EICUG Software Working Group** | The EIC Software Working Group includes over 100 physicists and software professionals. ([EIC Software][5])                                             | Since GEMC has CLAS/JLab credibility, this is a natural community to engage.           |

[1]: https://indico.cern.ch/event/1471803/?utm_source=chatgpt.com "28th Conference on Computing in High Energy and ..."
[2]: https://hepsoftwarefoundation.org/activities/pyhep.html?utm_source=chatgpt.com "PyHEP - Python in HEP"
[3]: https://hepsoftwarefoundation.org/activities/training.html?utm_source=chatgpt.com "HSF Training"
[4]: https://iris-hep.org/topical.html?utm_source=chatgpt.com "IRIS-HEP Topical Meetings"
[5]: https://eic.github.io/organization/swg.html?utm_source=chatgpt.com "Software Working Group"


| Target                        | Why it matters                                                                                                                                          | Suggested action                                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **AAPM**                      | AAPM is a central medical-physics organization; its 2026 abstract deadline was Jan. 27, 2026, so plan for the next cycle. ([AAPM][1])                   | Submit a medical-physics-oriented abstract: “Rapid Geant4-based dosimetry prototypes with GEMC.”                                  |
| **TOPAS community**           | TOPAS wraps Geant4 to make radiotherapy simulations easier for medical physicists. ([TopasMC][2])                                                       | Do not present GEMC as a replacement. Position it as a general database-driven Geant4 application layer with different strengths. |
| **OpenGATE / GATE community** | GATE is an open-source Geant4-based platform for emission tomography, CT, optical imaging, and radiotherapy simulations. ([Open Gate Collaboration][3]) | Add a respectful “related tools” page and invite maintainers to review the comparison.                                            |
| **GAMOS community**           | GAMOS is a Geant4-based easy/flexible framework with a scripting language. ([Fismed][4])                                                                | Compare GEMC’s database/Python workflow against scripting-based workflows.                                                        |
| **Geant4-DNA**                | Geant4-DNA extends Geant4 for radiation biophysics and radiobiology. ([Geant4-DNA][5])                                                                  | Useful if you create microdosimetry/radiobiology examples.                                                                        |
| **NSREC**                     | NSREC 2026 is July 20–24, 2026, and late-news summaries are listed as due May 15, 2026. ([NSREC][6])                                                    | Consider a space-radiation/shielding demo if you can produce a concrete example quickly.                                          |
| **RADECS**                    | RADECS 2026 is Sept. 28–Oct. 2, 2026, focused on radiation effects on components and systems. ([RADECS 2026][7])                                        | Pitch GEMC for radiation-effects simulation workflows.                                                                            |
| **NASA Open Science / OSSI**  | NASA promotes open science, transparency, collaboration, and software sustainability. ([NASA Science][8])                                               | Subscribe/engage, but contact NASA only with a clear space-radiation example or collaborator use case.                            |

[1]: https://aapm.confex.com/aapm/2026am/cfp.cgi?utm_source=chatgpt.com "Call for Abstracts"
[2]: https://www.topasmc.org/?utm_source=chatgpt.com "TOPAS Tool for Particle Simulation"
[3]: https://www.opengatecollaboration.org/?utm_source=chatgpt.com "OpenGATE collaboration"
[4]: https://fismed.ciemat.es/GAMOS/?utm_source=chatgpt.com "GAMOS"
[5]: https://geant4-dna.org/?utm_source=chatgpt.com "Geant4-DNA"
[6]: https://www.nsrec.com/?utm_source=chatgpt.com "IEEE Nuclear & Space Radiation Effects Conference: NSREC"
[7]: https://radecs2026.org/?utm_source=chatgpt.com "RADECS 2026 | RADiation and its Effects on Components ..."
[8]: https://science.nasa.gov/open-science/?utm_source=chatgpt.com "Open Science at NASA"


| Venue                                    | Best use                                                                                                                                                                                                                                 |
|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **JOSS**                                 | Best for a concise peer-reviewed software paper if GEMC has an OSI-approved license, documentation, and tests. JOSS describes itself as developer-friendly and open access for research software. ([Journal of Open Source Software][1]) |
| **SoftwareX**                            | Good for a broader software paper emphasizing research impact and reusable software. SoftwareX explicitly aims to recognize research software and developers. ([ScienceDirect][2])                                                       |
| **Computer Physics Communications**      | Strong fit for a more complete computational-physics software article. CPC publishes papers and application software in computational physics. ([ScienceDirect][3])                                                                      |
| **NIM A**                                | Good if you emphasize detector design, detector performance, or scientific-instrument simulation. NIM A covers scientific instruments, detector systems, and facilities using ionizing radiation. ([ScienceDirect][4])                   |
| **JOSE**                                 | Useful only if you create formal training material or a course module. JOSE publishes open-source educational materials and software. ([Journal of Open Source Education][5])                                                            |
| **ASCL**                                 | Useful if GEMC is used in astronomy/astrophysics research. ASCL is a registry for astrophysics research software and gives citable ASCL IDs. ([re3data][6])                                                                              |
| **Research Software Directory / OpenAIRE** | Useful for discoverability and citation tracking. RSD is designed to show research-software impact and encourage reuse/citation; OpenAIRE links open research outputs including software. ([Research Software Directory][7])             |
| https://numfocus.org                     | Useful for discoverability                                                                                                                                                                                                               | 

[1]: https://joss.theoj.org/?utm_source=chatgpt.com "Journal of Open Source Software"
[2]: https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors?utm_source=chatgpt.com "Guide for authors - SoftwareX - ISSN 2352-7110"
[3]: https://www.sciencedirect.com/journal/computer-physics-communications/publish/guide-for-authors?utm_source=chatgpt.com "Guide for authors - Computer Physics Communications"
[4]: https://www.sciencedirect.com/journal/nuclear-instruments-and-methods-in-physics-research-section-a-accelerators-spectrometers-detectors-and-associated-equipment/publish/guide-for-authors?utm_source=chatgpt.com "Guide for authors - Nuclear Instruments and Methods in ..."
[5]: https://jose.theoj.org/?utm_source=chatgpt.com "Journal of Open Source Education"
[6]: https://www.re3data.org/repository/r3d100011865?utm_source=chatgpt.com "Astrophysics Source Code Library"
[7]: https://research-software-directory.org/?utm_source=chatgpt.com "Research Software Directory: Home"
