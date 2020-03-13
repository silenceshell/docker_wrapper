#!/usr/bin/python
# coding=utf8
# utf8 without BOM

import os
import sys

#  gcr.io/xxx/yyy:zzz -> gcr.azk8s.cn/xxx/yyy:zzz, for example gcr.io/google_containers/kube-apiserver:v1.14.1
#  k8s.gcr.io/xxx:yyy => gcr.io/google-containers/xxx:yyy -> gcr.azk8s.cn/google-containers/xxx:yyy, for example k8s.gcr.io/kube-apiserver:v1.14.1
#  quay.io/xxx/yyy:zzz -> quay.azk8s.cn/xxx/yyy:zzz, for example quay.io/coreos/flannel:v0.10.0-amd64
#  xxx:yyy -> dockerhub.azk8s.cn/library/xxx:yyy

converts = {
    'gcr.io': 'gcr.azk8s.cn',
    'k8s.gcr.io': 'gcr.azk8s.cn/google-containers',
    'quay.io': 'quay.azk8s.cn',
}

def proxy_image(image):
    repo = image.split("/")[0]
    if repo in converts:
        return  image.replace(repo, converts[repo])
    # docker hub
    return  'dockerhub.azk8s.cn/library/' + image

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
    newImage = proxy_image(image)
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
