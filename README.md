# Canvas on the Command-line

Easily download files or view assignments from Canvas

##Installation

You will need a Canvas access token to run the script.

1. To obtain an access token go to https://(school-url).instructure.com/profile/settings

2. Remember to replace (school-url) with your actually school.

   - For example: [https://sjsu.instructure.com/profile/settings](https://sjsu.instructure.com/profile/settings)

3. Scroll to the bottom of the page and click on the light blue button that reads: "New Access Token"

4. You can put anything you like for the "Purpose" option, and click "Generate Token"

5. Copy your Canvas access token to a secure place. 

6. Clone the repository: git clone https://github.com/calvinha/canvas-command-line.git

7. Run canvas_tools.py

## Usage
```
python canvas_tools.py [course-name] [course-number]
```

* This will download the last file from the course and displays a download prompt from your web browser.

* The first you time you run the script, you will need to enter in your Canvas access-token

## Example
```
python canvas_tools.py MATH 129A
```

## Optional arguments
* To list and view specific assignment(s) use the `-a` option 
* To list and download specific file(s) use the `-f` option
* To download the last 'n' files, use the `-g` option with a numeric argument
``` 
python canvas_tools.py MATH 129A -g 3
```
This will download the *last* 3 files from the class MATH 129A.

##An example run: 

<pre><code>python canvas_tools.py MATH 129 -f

Enter the number(s) corresponding to the files you want to download separated by spaces:

1. Lecture1.pdf
2. Lecture2.pdf
3. HW1.txt

1 3 #User enters 1 and a 3 </code></pre>
   
- This will open the web browser with a download prompt for files `Lecture1.pdf` and `HW1.txt`


## Warnings
* The current version of the script does **not** check for bad user input.

## Resources

* Dependedent on the [Requests](http://docs.python-requests.org/en/latest/) library
* Special thanks to Daniel Mai for his guidance 
  * This Python script is inspired from his [Canvas codecheck grading](https://bitbucket.org/danielmai/code-check-homework-grading) 

