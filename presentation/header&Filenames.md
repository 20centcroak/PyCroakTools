# Header & Filename conventions

## Filename convention
To create a slide from a txt, markdown or image file, the file name should comply with this pattern *ID_title[_part][_version]* where :
- ID is a unique identifier (integer), ID may be not unique when part or version number differs
- title is an arbitrary title for the slide,
- part is an optional part number (to display slide parts vertically)
- version is an optional version number (to create presentation versions relative to slide or image versions)

file name examples:
>0_mon image.jpg  
1_mon image_1.2_0.5.png

## Header convention
A text or markdown (text with style) file may contain a header section to define the above information.  
In this case, the file can be named as we want.
This header section is composed of a "---" sequence defining the start and end of the header.  
It should be at the very beginning of the file. In this header at least 2 key/value pairs must be defined : ID and title. Part and version are optional.
These key/value pairs represent the same information than the one described for filename.

Here is an example
```md
---
title: my title
id:4
version:1.0
part:0.5
---
This is what will be displayed in the slide
```