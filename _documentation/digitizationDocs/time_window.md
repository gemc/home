---
layout: default
title: Time Window
order: 50
description: How to use the command line and / or jcards to setup a gemc session

---



gemc can be configured using: 

- command line options
- steering cards 

For example:

```
gemc -gui example.jcard
```

will launch gemc using the command line option `-gui` (which activates the graphical user interface) 
and the directives specified in the steering card 'example.jcard'

<br/>

---

<br/>

## JCards

<br/>
The gemc steering cards are JSON files the extentson **.jcard**, with comments added using the `#` sign.
An example of jcard:

<script src="https://gist.github.com/maureeungaro/f4449d88f5b63c4ef368d9e6f76589c1.js"></script>

---

<br/>

## Complete List of gemc options

The following is the output of gemc -h. Soon this help will be better formatted to be displayed online.

<script src="https://gist.github.com/maureeungaro/f104c42d76858ea6a1b8eb11d22758e4.js"></script>