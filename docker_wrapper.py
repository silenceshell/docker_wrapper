#!/usr/bin/python
# coding=utf8
# utf8 without BOM

import os
import sys

#  gcr.io/xxx/yyy:zzz -> gcr.azk8s.cn/xxx/yyy:zzz, for example gcr.io/google_containers/kube-apiserver:v1.14.1
#  k8s.gcr.io/xxx:yyy => gcr.io/google-containers/xxx:yyy -> gcr.azk8s.cn/google-containers/xxx:yyy, for example k8s.gcr.io/kube-apiserver:v1.14.1
#  quay.io/xxx/yyy:zzz -> quay.azk8s.cn/xxx/yyy:zzz, for example quay.io/coreos/flannel:v0.10.0-amd64

converts = [
    {
        'prefix': 'gcr.io',
        'replace': lambda x: x.replace('gcr.io', 'gcr.azk8s.cn'),
    },
    {
        'prefix': 'k8s.gcr.io',
        'replace': lambda x: x.replace('k8s.gcr.io', 'gcr.azk8s.cn/google-containers'),
    },
    {
        'prefix': 'quay.io',
        'replace': lambda x: x.replace('quay.io', 'quay.azk8s.cn'),
    },
    {
        'prefix': 'docker.io',
        'replace': lambda x: x.replace('docker.io', 'dockerhub.azk8s.cn'),
    }
]

cache_prefix = 'dockerhub.azk8s.cn/library/'

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

    image = sys.argv[2]
    imageArray = image.split("/")
   
    newImage = '' 
    for cvt in converts:
        if imageArray[0] == cvt['prefix']:
            newImage = cvt['replace'](image)
            break

    if not newImage:
        newImage = cache_prefix + image

    if newImage:
        print("-- pull {image} from {newimage} instead --".format(image=image, newimage=newImage))
        cmd = "docker pull {image}".format(image=newImage)
        execute_sys_cmd(cmd)
     
        cmd = "docker tag {newImage} {image}".format(newImage=newImage, image=image)
        execute_sys_cmd(cmd)
       
        cmd = "docker rmi {newImage}".format(newImage=newImage)
        execute_sys_cmd(cmd)
       
        print("-- pull {image} done --".format(image=image))
        sys.exit(0)
    else:
        cmd = "docker pull {image}".format(image=image)
        execute_sys_cmd(cmd)
        sys.exit(0)
