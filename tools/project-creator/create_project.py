#!/usr/bin/python
# create_project.py
# Create cross-platform cocos2d-x project
# Copyright (c) 2012 cocos2d-x.org
# Author: WangZhe

# define global variables
context = {}.fromkeys(("language", "src_project_name", "src_package_name", "dst_project_name", "dst_package_name", "src_project_path", "dst_project_path", "script_dir"));
platforms_list = []

# begin
import sys
import os, os.path
import json
import shutil

def checkParams(context):
    from optparse import OptionParser
    
    # set the parser to parse input params
    # the correspond variable name of "-x, --xxx" is parser.xxx
    parser = OptionParser(usage="Usage: ./%prog -p PROJECT_NAME -k PACKAGE_NAME -l PROGRAMING_LANGUAGE\nSample : ./%prog -p MyGame -k com.MyCompany.AwesomeGame -l javascript")
    parser.add_option("-p", "--project", metavar="PROJECT_NAME", help="Set a project name")
    parser.add_option("-k", "--package", metavar="PACKAGE_NAME", help="Set a package name for project")
    parser.add_option("-l", "--language",
                      metavar="PROGRAMMING_NAME",
                      type="choice",
                      choices=["cpp", "lua", "javascript"],
                      help="Major programing lanauge you want to used, should be [cpp | lua | javascript]")
    
    #parse the params
    (opts, args) = parser.parse_args()

    # generate our internal params
    context["script_dir"] = os.getcwd() + "/"
    global platforms_list
    
    if opts.project:
        context["dst_project_name"] = opts.project
        context["dst_project_path"] = os.getcwd() + "/../../projects/" + context["dst_project_name"]
    else:
        parser.error("-p or --project is not specified")

    if opts.package:
        context["dst_package_name"] = opts.package
    else:
        parser.error("-k or --package is not specified")

    if opts.language:
        context["language"] = opts.language
    else:
        parser.error("-k or --package is not specified")
                                 
    # fill in src_project_name and src_package_name according to "language"
    if ("cpp" == context["language"]):
        context["src_project_name"] = "HelloCpp"
        context["src_package_name"] = "org.cocos2dx.hellocpp"
        context["src_project_path"] = os.getcwd() + "/../../template/multi-platform-cpp"
        platforms_list = ["ios",
                          "android",
                          "win32",
                          "mac",
                          "blackberry",
                          "linux",
                          "marmalade"]
    elif ("lua" == context["language"]):
        context["src_project_name"] = "HelloLua"
        context["src_package_name"] = "org.cocos2dx.hellolua"
        context["src_project_path"] = os.getcwd() + "/../../template/multi-platform-lua"
        platforms_list = ["ios",
                          "android",
                          "win32",
                          "blackberry",
                          "linux",
                          "marmalade"]
    elif ("javascript" == context["language"]):
        context["src_project_name"] = "HelloJavascript"
        context["src_package_name"] = "org.cocos2dx.hellojavascript"
        context["src_project_path"] = os.getcwd() + "/../../template/multi-platform-js"
        platforms_list = ["ios",
                          "android",
                          "win32"]
# end of checkParams(context) function

def replaceString(filepath, src_string, dst_string):
    content = ""
    f1 = open(filepath, "rb")
    for line in f1:
        if src_string in line:
            content += line.replace(src_string, dst_string)
        else:
            content += line
    f1.close()
    f2 = open(filepath, "wb")
    f2.write(content)
    f2.close()
# end of replaceString

def processPlatformProjects(platform):
    # determine proj_path
    proj_path = context["dst_project_path"] + "/proj.%s/" % platform
    java_package_path = ""

    # read josn config file or the current platform
    f = open("%s.json" % platform)
    data = json.load(f)

    # rename package path, like "org.cocos2dx.hello" to "com.company.game". This is a special process for android
    if (platform == "android"):
        src_pkg = context["src_package_name"].split('.')
        dst_pkg = context["dst_package_name"].split('.')
        os.rename(proj_path + "src/" + src_pkg[0],
                  proj_path + "src/" + dst_pkg[0])
        os.rename(proj_path + "src/" + dst_pkg[0] + "/" + src_pkg[1],
                  proj_path + "src/" + dst_pkg[0] + "/" + dst_pkg[1])
        os.rename(proj_path + "src/" + dst_pkg[0] + "/" + dst_pkg[1] + "/" + src_pkg[2],
                  proj_path + "src/" + dst_pkg[0] + "/" + dst_pkg[1] + "/" + dst_pkg[2])
        java_package_path = dst_pkg[0] + "/" + dst_pkg[1] + "/" + dst_pkg[2]

    # rename files and folders
    for i in range(0, len(data["rename"])):
        tmp = data["rename"][i].replace("PACKAGE_PATH", java_package_path)
        src = tmp.replace("PROJECT_NAME", context["src_project_name"])
        dst = tmp.replace("PROJECT_NAME", context["dst_project_name"])
        if (os.path.exists(proj_path + src) == True):
            os.rename(proj_path + src, proj_path + dst)

    # remove useless files and folders
    for i in range(0, len(data["remove"])):
        dst = data["remove"][i].replace("PROJECT_NAME", context["dst_project_name"])
        if (os.path.exists(proj_path + dst) == True):
            shutil.rmtree(proj_path + dst)
    
    # rename package_name. This should be replaced at first. Don't change this sequence
    for i in range(0, len(data["replace_package_name"])):
        tmp = data["replace_package_name"][i].replace("PACKAGE_PATH", java_package_path)
        dst = tmp.replace("PROJECT_NAME", context["dst_project_name"])
        if (os.path.exists(proj_path + dst) == True):
            replaceString(proj_path + dst, context["src_package_name"], context["dst_package_name"])
    
    # rename project_name
    for i in range(0, len(data["replace_project_name"])):
        tmp = data["replace_project_name"][i].replace("PACKAGE_PATH", java_package_path)
        dst = tmp.replace("PROJECT_NAME", context["dst_project_name"])
        if (os.path.exists(proj_path + dst) == True):
            replaceString(proj_path + dst, context["src_project_name"], context["dst_project_name"])
                  
    # done!
    print "proj.%s\t\t: Done!" % platform
# end of processPlatformProjects



# -------------- main --------------
# dump argvs
# print sys.argv

# prepare valid "context" dictionary
checkParams(context)
# import pprint
# pprint.pprint(context)

# copy "lauguage"(cpp/lua/javascript) platform.proj into cocos2d-x/projects/<project_name>/folder
if (os.path.exists(context["dst_project_path"]) == True):
    print "Error:" + context["dst_project_path"] + " folder is already existing"
    print "Please remove the old project or choose a new PROJECT_NAME in -project parameter"
    sys.exit()
else:
    shutil.copytree(context["src_project_path"], context["dst_project_path"], True)

# call process_proj from each platform's script folder          
for platform in platforms_list:
    processPlatformProjects(platform)
#    exec "import %s.handle_project_files" % (platform)
#    exec "%s.handle_project_files.handle_project_files(context)" % (platform)

print "New project has been created in this path: " + context["dst_project_path"].replace("/tools/project-creator/../..", "")
print "Have Fun!"

