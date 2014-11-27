#!/usr/bin/env python

"""Get files and assignments from Canvas""" 

__author__ = "Calvin Ha"
__credits__ = "Daniel Mai"
__version__ = "1.0.0"
__email__ = "calvinbha@gmail.com"

import argparse
import json
import os
import requests
import sys
import webbrowser


access_token = ''

CANVAS_KEYS = "canvas_keys.json"
HEADER =  {'Authorization': 'Bearer ' + access_token}
HOST_SITE = 'sjsu.instructure.com'
PAGE_PAGINATION_LIMIT = 75
PROTOCOL = 'https://'
QUIT = "q"


def parse_args():
    """Generates the argument parser"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("class_name", help = 'Specify your class. e.g. MATH')
    parser.add_argument("class_number", help = 'Specifiy the class number. e.g. 129A')
    parser.add_argument("-a", "--listassignments", help = "List all the assignments available ", action = "store_true")
    parser.add_argument("-g", "--getfiles", help = "Enter the amount of files you want to download",  type=int)
    parser.add_argument("-f", "--listfiles", help = "List all the files available to download", action = "store_true")
    return parser.parse_args()


def get_files(courseid):
    """Returns a json object for files"""
    
    params = {'sort': 'created_at',
              'per_page': PAGE_PAGINATION_LIMIT 
    }
    
    path = '/api/v1/courses/%s/files' % (courseid)
    url = '%s%s%s' % (PROTOCOL, HOST_SITE, path)
    files  = requests.get(url, headers=HEADER, params=params).json()
    return files


def get_assignments(course_id):
    """Get assignments for the course"""
    
    path = '/api/v1/courses/%s/assignments' % (course_id)
    url = '%s%s%s' % (PROTOCOL, HOST_SITE, path)
    params = {'include[]':'submission',
              'per_page': PAGE_PAGINATION_LIMIT
    }
    
    assignments = requests.get(url, headers=HEADER, params=params).json()   
    return sorted(assignments, key = lambda assignment: assignment['due_at'])
   

def list_files(files):
    """Lists all the files in the course and stores their url into a map"""
    
    url_map ={}
    count = 1
    for theFile in files:
        url_map[count] = theFile['url']
        print "%s.  %s" % (str(count), theFile['display_name'])
        count += 1
    return url_map


def list_assignments(assignments, upload):
    """Lists all the assignments in the course and stores their url into a map"""
    
    assignments_map ={}
    
    count = 1    
    for assignment in assignments:
        if upload:                        
            assignments_map[count] = assignment['id'] 
        else:
            assignments_map[count] = assignment['html_url']        
        print "%s.  %s" % (str(count), assignment['name'])
        count += 1
    if upload:
        print 'Enter the number corresponding to the assignment you want to turn in: '
        return assignments_map[int(raw_input())]
    return assignments_map



def open_files(file_map, files, is_assignment, amount):
    """Gets user input on which file(s) they would like to download"""
    
    if is_assignment:
        keyword = 'assignments'
    else:
        keyword = 'files'


    if amount < 0 or is_assignment:
        if len(file_map) == 0: #is empty
            print 'This course has no files'
            return None
        print "\nEnter the number(s) corresponding to the %s you want to download separated by spaces" % (keyword)
        user_input = str(raw_input()).split()
        if user_input[0].lower() == QUIT:
            sys.exit()
        numbers_list = [int(number) for number in user_input]
        for number in numbers_list:
            url = file_map[number]
            webbrowser.open(url)
    else: #User wants to download a specifed amount of files 
        # Error checking
        if amount > len(files):
            print "The amount you specified (%d) is greater that the total amount of files (%d) for this course." % (amount, len(files) ) 
            return None
        start_index = len(files) - 1
        while (amount > 0):
            url = files[start_index]['url']
            webbrowser.open(url)
            start_index = start_index - 1
            amount = amount - 1

        
def check_canvas_keys():   
    """Check if the users' Canvas access token and courses are already in the json file

    if not go through prompt the user for their Canvas access token and add their courses to the json file
    returns a dictionary of course:id 
    
    """
    global access_token 
    
    canvas_dict = {}
    directory = os.getcwd()
    canvas_file = directory + '/' + CANVAS_KEYS
    if os.path.isfile(canvas_file):
        #Gets JSON data and puts it into a dict
        json_data = open(CANVAS_KEYS)       
        canvas_dict = json.load(json_data)
        access_token = canvas_dict['access-token']
        HEADER['Authorization'] =  'Bearer ' + access_token
        json_data.close()
    else:
        #Ask the user for their access token 
        print "Please enter your Canvas access token: "
        access_token = raw_input()
        HEADER['Authorization'] =  'Bearer ' + access_token
        canvas_dict = add_courses()
        canvas_dict['access-token'] = access_token
        #Writes JSON data to a new file called courses.json
        with open(CANVAS_KEYS, 'w') as outfile:
            json.dump(canvas_dict, outfile)        
    return canvas_dict
        

        
def add_courses():
    """Add the students' current courses to a map"""
    
    courses_map = {}
    params = {'state': 'available'}
    path = '/api/v1/courses/'
    url = '%s%s%s' % (PROTOCOL, HOST_SITE, path)
    courses = requests.get(url, headers = HEADER, params = params).json()
    course_end_date = None

    #Checks if the course ending date matches if so, add the course to the map

    for course in (courses):
        ending_date = course['end_at']
        if course_end_date == None or course_end_date == ending_date:
            course_end_date = ending_date
            course_name =  parse_course(course['name'])
            course_id = course['id']
            #Add to the map
            courses_map[course_name] = course_id                   
        else:
            return courses_map
    return None


def parse_course(course):
    """Parse the course to get the course_name and course_number"""
    
    course = course.encode('ascii', 'ignore') #Convert to ascii
    course_list = course.split()[1] 
    course_name = course_list.split('-')
    course_identifier = course_name[0] + " " + course_name[1]
    return course_identifier



def main():    

    class_dict = check_canvas_keys()
    args = parse_args()
    class_name = args.class_name.upper()
    class_number = args.class_number
    class_chosen = class_name + " " + class_number
    courseid = class_dict[class_chosen]
    url_map = None
    if args.listfiles or args.getfiles:        
        files = get_files(courseid)
        amount = args.getfiles       
        if args.listfiles:
            url_map = list_files(files)
        open_files(url_map, files, False, amount)
        
    elif args.listassignments: #To list assignments 
        assignments = get_assignments(courseid)
        url_map = list_assignments(assignments, False)
        open_files(url_map, files, True, amount)
    

        
if __name__ == "__main__":
    main()
