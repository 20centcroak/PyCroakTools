# EasyPresentation module

## Description

The easyPresentation module makes it easy to produce a revealjs presentation. Besides of what can be done with the presentation module , and what can be done with the workflow module (see documentation of these modules), it is possible to link these 2 modules to create a workflow presentation easily. Then the presentation follows the logical paths defined in the workflow. 

It is also easier to build a standard presentation (without any workflow definition) thanks to high level classes.

## Basic call examples

Suppose to want to create a presentation based on a series of images available in folder *C:/temp/images*. Images should comply with this pattern *ID_title[_part][_version]* where :
- ID is a unique identifier (integer), ID may be not unique when part or version number differs
- title is an arbitrary title for the slide,
- part is an optional part number (to display slide parts vertically)
- version is an optional version number (to create presentation versions relative to slide or image versions)

file name examples:
>0_mon image.jpg  
1_mon image_1.2_0.5.png

```python
from pycroaktools.easyPresentation.generator import Generator
settings= {'imageFolder':'C:/temp/images'}
Generator(settings)
```
That's it! the presentation is generated in the current working directory with name *presentation_v0.0.html*

Now suppose you want to create a presentation without any other content that the workflow definition shown below and saved in a .csv file:  

|stepId|title|nexts|
|:---|:---:|---:|
|1|my first step|2-3|
|2|my second step|4|
|3|step 3!|12|
|4|step4||
|9|step9|12-4|
|12|step12||

here is the csv file:  
>stepId,title,nexts  
1,my first step,2-3  
2,my second step,4  
3,step 3!,12  
4,step4,  
9,step9,12-4  
12,step12,  

and here is the code:
```python
from pycroaktools.easyPresentation.generator import Generator
settings= {'workflowFile':'workflow.csv'}
Generator(settings)
```

And now all together: create a presentation with markown files in the slides folder, images in the images folder, workflow definition workflow.csv. Create presentations for versions 0 and 1 as linear presentations representing all possible paths (for example 1-2-4, 1-3-12, ...) and a workflow presentation with links (slide 1 can drive to slides 2 and 3 thanks to links).

Note that the markdown slides (or simply txt files) should respect one of the following rules:
    - the markdown file owns a header section composed of a "---" sequence defining the start and end of the header. It should be at the very beginning of the file.
    In this header at least 2 keys are defined :
        - title: arbitrary title
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
    - the markdown file name is built as follow: id_title[_part][_version]. The fields are the same than in the header definition

markdown file with header example:
>\---  
title:title  
id:3  
part:1.2  
version:0.5  
\---  
\# My markdown file  
Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...


```python
from pycroaktools.easyPresentation.generator import Generator
settings = {'workflowFile': 'C:/temp/workflow.csv', 'imageFolder': 'C:/temp/images', 'outputFolder': 'C:/temp/pres',
            'slideFolder': 'C:/temp/slides', 'versions': [0, 1], 'createLinearPresentations': True, 'createWorkflowPresentation': True}
Generator(settings)
```

Like I said, easy!