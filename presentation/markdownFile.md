# Markdown files

Markdown is a simple-to-use text formating syntax largely used in wiki and forums.  
See how to use it here: <https://www.markdownguide.org/basic-syntax/>

To define a slide with a markdown file, either you supply necessary information in the filename or in a header section (see [header & Filenames](header&Filenames.html))
Then you can type in you slide content with markdown formating.
Here is an example with a header section:

    ---
    title: my title
    id:4
    version:1.0
    part:0.5
    ---
    # A title
    ## a subtitle
    This is a paragraph
    you can add an image ![logo markdown](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/130px-Markdown-mark.svg.png)
    or a link [qwant](http://www.qwant.fr)
    ...

And here is the rendering:
# A title
## a subtitle
This is a paragraph   
you can add an image  
![logo markdown](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/130px-Markdown-mark.svg.png)  
or a link [qwant](http://www.qwant.fr)