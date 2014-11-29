# Canvas on the Command-line

Easily download files or view assignments from Canvas

#Installation

You will need a Canvas access token to run the script.

1. To obtain an access token go to https://(school-url).instructure.com/profile/settings

2. Remember to replace (school-url) with your actually school.

   - For example: [https://sjsu.instructure.com/profile/settings](https://sjsu.instructure.com/profile/settings)

4. Scroll to the bottom of the page and click on the light blue button that reads: "New Access Token"

5. Copy your Canvas access token. 

# Usage
```
python canvas-tools.py [course-name] [course-number]
```

* This will download the last file from the course and displays a download prompt from your web browser.

* The first you time you run the script, you will need to enter in your Canvas access-token

# Example
```
python canvas-tools.py MATH 129A
```

# Optional arguments
* To list and view specific assignment(s) use the `-a` option 
* To list and download specific file(s) use the `-f` option
* To download the last 'n' files, use the `-g` option with a numeric argument
```
python canvas-tools.py MATH 129A -g 3
```
This will download the *last* 3 files from the class MATH 129A.

# Resources

* Dependedent on the [Requests](http://docs.python-requests.org/en/latest/) library
* Special thanks to Daniel Mai 
  * This Python script is inspired from his [Canvas codecheck grading](https://bitbucket.org/danielmai/code-check-homework-grading) 

