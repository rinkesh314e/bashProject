import os
import argparse
from shutil import rmtree
from subprocess import run, PIPE, STDOUT

class CourseMount:
    
    def __init__(self):
        self.courses = [
            "Linux_course/Linux_course1",
            "Linux_course/Linux_course2",
            "machinelearning/ML_course1",
            "machinelearning/ML_course2",
            "SQLFundamentals1",
            "SQLFundamentals2",
            "SQLFundamentals3"
        ]
        self.source = '/home/rinkesh/scripts/source/courses'
        self.target = '/home/rinkesh/scripts/target/courses'
    

    def check_course(self, course):
        return course in self.courses


    def check_mount(self, course):
        course_path = os.path.join(self.target, course)
        
        #check mount
        if os.path.isdir(course_path):
            mount_check = run(['mountpoint', course_path], stdout=PIPE, stderr=STDOUT)
            #print(mount_check)
            return True if mount_check.returncode == 0 else False
        return False


    def mount_course(self, course):
        if not self.check_course(course):
            print(f'Incorrect {course} name given. Try again')
            return 1
        if self.check_mount(course):
            print("{course} Already mounted.")
            return 0
        
        #make target directories
        target_course_path = os.path.join(self.target, course)
        source_course_path = os.path.join(self.source, course)
        os.makedirs(target_course_path)

        #mount source to target
        result = run(['bindfs', '-p', '550', '-u', 'rinkesh', '-g',
                        'rinkesh', source_course_path, target_course_path], 
                         stdout=PIPE, stderr=STDOUT)
        #check if mounted successfully
        if result.returncode != 0:
            rmtree(target_course_path)
            print("Mounting failed.")
            return 1

        print(f'{course} Mounted Successfully.')
        return 0


    def mount_all(self):
        for course in self.courses:
            self.mount_course(course)


    def unmount_course(self, course):   
        if not self.check_course(course):
            print(f'Incorrect {course} name given. Try again')
            return 1
        if not self.check_mount(course):
            print(f'{course} is either unmounted or directory does not exists')
            return 0
        else:
            unmount_path = os.path.join(self.target, course)
            result = run(['sudo', 'umount', unmount_path], stdout=PIPE, stderr=STDOUT)
            if result.returncode != 0:
                print("Unmounting Error")
                return 1
            else:
                rmtree(unmount_path, ignore_errors=True)
                print(f'{course} Unmounted Successfully')
                return 0

    def unmount_all(self):
        for course in self.courses:
            self.unmount_course(course)



if __name__ == '__main__':
    #adding CLI 
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mount', action='store_true', help='for mounting courses')
    parser.add_argument('-u', '--unmount', action='store_true', help='for unmounting courses')
    parser.add_argument('-c', '--course', type=str, help='give the course name to mount/unmount' )

    args = parser.parse_args()

    #calling CurseMount
    mount_obj = CourseMount()

    if args.mount:
        if args.course:
            mount_obj.mount_course(args.course)
        else:
            mount_obj.mount_all()
    elif args.unmount:
        if args.course:
            mount_obj.unmount_course(args.course)
        else:
            mount_obj.unmount_all()
    else:
        print('Read the docs with -h flag')
