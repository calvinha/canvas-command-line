
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
import getpass

CANVAS_KEYS = "canvas_keys.json"
PAGE_PAGINATION_LIMIT = 75
PROTOCOL = 'https://'
QUIT = "q"

class CanvasSession():
    def __init__(self, host_site, access_token):
        self.host_site = host_site
        self.header = {"Authorization" : "Bearer " + access_token}

def parse_args():
    """Generates the argument parser"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("class_name", help = 'Specify your class. e.g. MATH')
    parser.add_argument("class_number", help = 'Specifiy the class number. e.g. 129A')
    parser.add_argument("-a", "--listassignments", help = "List all the assignments available ", action = "store_true")
    parser.add_argument("-g", "--getfiles", help = "Enter the amount of files you want to download",  type=int)
    parser.add_argument("-f", "--listfiles", help = "List all the files available to download", action = "store_true")
    parser.add_argument("-u", "--update-courses", help="Update your courses", action="store_true")
    return parser.parse_args()


def get_folders(courseid, header, host_site):
    """Returns all the folders in the course"""
    
    path = '/api/v1/courses/%s/folders/by_path' % courseid
    url = '%s%s%s' % (PROTOCOL, host_site, path)
    root_folder = requests.get(url, headers=header).json()
    for folder in root_folder:
        id = folder['id']
    new_path = '/api/v1/folders/%s/folders' % id
    new_url = '%s%s%s' % (PROTOCOL, host_site, new_path)
    print  requests.get(new_url, headers=header).json()

    
def get_files(courseid, header, host_site):
    """Returns a json object for files"""
    
    params = {'sort': 'created_at',
              'per_page': PAGE_PAGINATION_LIMIT 
    }
    
    path = '/api/v1/courses/%s/files' % (courseid)
    url = '%s%s%s' % (PROTOCOL, host_site, path)
    files  = requests.get(url, headers=header, params=params).json()
    return files


def get_assignments(course_id, header, host_site):
    """Get assignments for the course"""
    
    path = '/api/v1/courses/%s/assignments' % (course_id)
    url = '%s%s%s' % (PROTOCOL, host_site, path)
    params = {'include[]':'submission',
              'per_page': PAGE_PAGINATION_LIMIT
    }
    
    assignments = requests.get(url, headers=header, params=params).json()   
    return sorted(assignments, key = lambda assignment: assignment['due_at'])
   

def list_files(files):
    """Lists all the files in the course and stores their url into a map"""
    
    url_map ={}
    for i, the_file in enumerate(files, 1):
        url_map[i] = the_file['url']
        print "%s.  %s" % (str(i), the_file['display_name'])
    return url_map

def list_assignments(assignments, upload):
    """Lists all the assignments in the course and stores their url into a map"""
    
    assignments_map ={}
    
    for i, assignment in enumerate(assignments, 1):
        if upload:                        
            assignments_map[i] = assignment['id'] 
        else:
            assignments_map[i] = assignment['html_url']        
        print "%s.  %s" % (str(i), assignment['name'])
    if upload:
        print 'Enter the number corresponding to the assignment you want to turn in: '
        return assignments_map[int(raw_input())]
    return assignments_map

def open_specific_files(file_map, is_assignment):
    """Gets user input on which specific file(s) they want to download"""

    keyword = "assignments" if is_assignment else "files"

    if not file_map: #is empty
        print 'This course has no %s listed' % keyword
        sys.exit()
    print "\nEnter the number(s) corresponding to the %s you want to download separated by spaces:" % (keyword)

    user_input = str(raw_input()).split()
    if user_input[0].lower() == QUIT:
        sys.exit()
    numbers_list = [int(number) for number in user_input]
    for number in numbers_list:
        url = file_map[number]
        webbrowser.open(url)

def open_num_files(files, amount):
    """Gets user input on the last n files they want to download"""

    if amount > len(files):
        print "The amount you specified (%d) is greater than the total amount of files (%d) for this course." % (amount, len(files) ) 
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
    
    canvas_dict = {}
    directory = os.getcwd()
    canvas_file = directory + '/' + CANVAS_KEYS
    store_token = ''
    file_exists = os.path.isfile(canvas_file)

    if file_exists: 
        #Gets JSON data and puts it into a dict
        json_data = open(CANVAS_KEYS)       
        canvas_dict = json.load(json_data)
        json_data.close()
    if not canvas_dict.get('access-token') or not file_exists:
        access_token = getpass.getpass('Please enter your Canvas access token: ')
        print "Do you want your access token to be stored in this directory? [y/n]: "
        store_token = raw_input()
        canvas_dict['access-token'] = access_token
    if not file_exists:
        print "Please enter your host school: "
        host_site = raw_input()
        canvas_dict = add_courses({'Authorization': 'Bearer ' + access_token}, host_site)
        canvas_dict['host-site']  = host_site
        if store_token in ('yes', 'y'):
            canvas_dict['access-token'] = access_token  
    if not file_exists or store_token == 'y': 
        with open(CANVAS_KEYS, 'w') as outfile:
            json.dump(canvas_dict, outfile, indent=4)        
        canvas_dict['access-token'] = access_token
    return canvas_dict
        
def add_courses(header, host_site):
    """Add the students' current courses to a map"""
    
    courses_map = {}
    params = {'state': 'available'}
    path = '/api/v1/courses/'
    url = '%s%s%s' % (PROTOCOL, host_site, path)
    courses = requests.get(url, headers = header, params = params).json()
    course_start_date = None
    
    # filter out the restricted courses
    valid_courses = [ co for co in courses if co.get('start_at')]
    # none if the course starting date matches if so, add the course to the map
    courses = sorted(valid_courses, key = lambda course:course['start_at'], reverse=True)

    for course in (courses):        
        start_date = course['start_at']
        if course_start_date == None or course_start_date == start_date:
            course_start_date = start_date
            course_name =  parse_course(course['name'])
            course_id = course['id']
            #Add to the map
            courses_map[course_name] = course_id                   
        else:
            return courses_map
    return None

def update_courses(header, host_site):
    """Updates the JSON file with the most recent courses"""
    current_courses = add_courses(header, host_site)
    with open(CANVAS_KEYS, 'r+') as f:
        canvas_dict = json.loads(f.read())
        for course, id in current_courses.iteritems():
            canvas_dict[course] = id
        f.seek(0)
        json.dump(canvas_dict, f, indent=4)
    print 'Courses have been updated'

def parse_course(course):
    """Parse the course to get the course_name and course_number"""
    
    course = course.encode('ascii', 'ignore') #Convert to ascii
    course_list = course.split()[1] 
    course_name = course_list.split('-')
    course_identifier = course_name[0] + " " + course_name[1]
    return course_identifier

def main():    
    args = parse_args()
    user_keys = check_canvas_keys()
    class_name = args.class_name.upper()
    class_number = args.class_number
    class_chosen = class_name + " " + class_number
    courseid = user_keys[class_chosen]
    canvas = CanvasSession(user_keys['host-site'], user_keys['access-token'])
    url_map = None

    if args.listassignments: #To list assignments 
        assignments = get_assignments(courseid, canvas.header, canvas.host_site)
        url_map = list_assignments(assignments, False)
        open_specific_files(url_map,  True)
    elif args.update_courses:
        update_courses(canvas.header, canvas.host_site)
    else:
        files = get_files(courseid, canvas.header, canvas.host_site)
        if args.listfiles: 
            url_map = list_files(files)
            open_specific_files(url_map, False)
        else:
            #User wants to download the last n files 
            amount = args.getfiles
            #User specified no arguments
            if amount == None: 
                amount = 1
            open_num_files(files, amount)        
        
if __name__ == "__main__":
    main()
