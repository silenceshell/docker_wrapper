#!/usr/bin/python
# coding=utf8

import os
import sys

mirror = "gcr.azk8s.cn"
namespace = "google_containers"
prefix = "gcr.io"
specialPrefix = "k8s.gcr.io"

def execute_sys_cmd(cmd):
    result = os.system(cmd)
    if result != 0:
        print(cmd + " failed.")
        sys.exit(-1)

def usage():
    print("Usage: " + sys.argv[0] + " pull ${image}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)

    # image name like k8s.gcr.io/kube-apiserver:v1.14.1 or gcr.io/google_containers/kube-apiserver:v1.14.1
    image = sys.argv[2]
    imageArray = image.split("/")
    
    if imageArray[0] != prefix and imageArray[0] != specialPrefix:
        cmd = "docker pull {image}".format(image=image)
        execute_sys_cmd(cmd)
        sys.exit(0)

    if len(imageArray) == 2:
        seq = (mirror, namespace, imageArray[1])
    else:
        seq = (mirror, imageArray[1], imageArray[2])

    newImage = "/".join(seq)

    print("-- pull {image} from gcr.azk8s.cn instead --".format(image=image))
    cmd = "docker pull {image}".format(image=newImage)
    execute_sys_cmd(cmd)

    cmd = "docker tag {newImage} {image}".format(newImage=newImage, image=image)
    execute_sys_cmd(cmd)

    cmd = "docker rmi {newImage}".format(newImage=newImage)
    execute_sys_cmd(cmd)

    print("-- pull {image} done --".format(image=image))
    sys.exit(0)
