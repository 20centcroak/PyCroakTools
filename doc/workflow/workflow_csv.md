# Workflow definition file

A workflow is a list of steps defined by their id (stepId), their title (optional) and each step may point on one or many next steps, defining a workflow.
The table below shows an example.

|stepId|title|nexts|
|:---|:---:|---:|
|1|my first step|2-3|
|2|my second step|4|
|3|step 3!|12|
|4|step4||
|9|step9|12-4|
|12|step12||

In this example:
- steps 1 and 9 are the first steps in the workflow because the don't have any previous step. (no other step mentions steps 1 and 9) 
- Steps 4 and 12 are the last steps because they don't have any next step.  
- Step 1 points to 2 next steps: steps 2 and 3, step 2 points to step 4, ...

Steps have to be defined with a unique identifier. This identifier must be an integer. But, as we can see, there is no need to define a continuous suite and the identifiers don't need to be sorted. 

Here is the expected format of a .csv workflow definition file:

    stepId,title,nexts  
    1,my first step,2-3  
    2,my second step,4  
    3,step 3!,12  
    4,step4,  
    9,step9,12-4  
    12,step12, 

or basically:

    stepId,nexts  
    1,2-3  
    2,4  
    3,12  
    4,  
    9,12-4  
    12, 