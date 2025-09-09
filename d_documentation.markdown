---
title: Documentation
layout: doc_master_toc
permalink: /documentation/
topic_id: Documentation
---


This manual provides documentation for the **GEMC** application. 
It is assumed that the software has been installed. See also the [installation instructions](/home/installation/).

Navigate through the various documentation using the table of content on the left or below. 

<br/>


## Table of Contents

<ul class="toc">
  {% for section in site.data.docs_topics %}
    <li>
      <a href="../docs/{{ section.id }}" >{{ section.title }}</a>
    </li>
  {% endfor %}
</ul>




[systems]:  /home/assets/images/systems.png

[geometry]: /home/assets/images/examples/scintillator_array/geometry.png

[materials]: /home/assets/images/materials.png

[digitization]: /home/assets/images/digitization.png

[generator]: /home/assets/images/generator.png

[em_fields]: /home/assets/images/em_fields.png

[physics]: /home/assets/images/physics.png

[mirrors]: /home/assets/images/mirrors.png

[time_window]: /home/assets/images/time_window.png

[options]: /home/assets/images/options.png

[faq]: /home/assets/images/faq.png

[exit_codes]: /home/assets/images/exit_codes.png

[doxygen]: /home/assets/images/doxygen.png

