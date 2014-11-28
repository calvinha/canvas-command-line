# Canvas on the Command-line

Easily download files or view assignments from Canvas


## Usage
```
python canvas-tools.py [course-name] [course-number]
```

* This will download the last file from the course and displays a download prompt from the web browser.

## Example
```
python canvas-tools.py MATH 129A
```

## Optional arguments
* To list and view specific assignment(s) use the `-a` option 
* To list and download specific file(s) use the `-f` option
* To list and download the last 'n' files, use the `-g` option with a numeric argument
``` bash
python canvas-tools.py MATH 129A -g 3
```
This will download the *last* 3 files from the class MATH 129A.

# Resources

* Dependedent on [Requests](http://docs.python-requests.org/en/latest/) library
* Special thanks to Daniel Mai 
  * This Python script is inspired from his [Canvas codecheck grading](https://bitbucket.org/danielmai/code-check-homework-grading) 

