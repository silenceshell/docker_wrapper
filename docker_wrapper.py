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
    }
]


def execute_sys_cmd(cmd):
    result = os.system(cmd)
    if result != 0:
        print(cmd + " failed.")
        sys.exit(-1)


def usage():
    print("Usage: " + sys.argv[0] + " pull ${image}")


def pull_and_tag_image(image):
    imageArray = image.strip().split('/')
    newImage = ''
    for cvt in converts:
        if imageArray[0] == cvt['prefix']:
            newImage = cvt['replace'](image)
            break
    if newImage:
        print("-- pull {image} from {newimage} instead --".format(image=image, newimage=newImage))
        cmd = "docker pull {image}".format(image=newImage)
        execute_sys_cmd(cmd)

        cmd = "docker tag {newImage} {image}".format(newImage=newImage, image=image)
        execute_sys_cmd(cmd)

        cmd = "docker rmi {newImage}".format(newImage=newImage)
        execute_sys_cmd(cmd)

        print("-- pull {image} done --".format(image=image))
    else:
        cmd = "docker pull {image}".format(image=image)
        execute_sys_cmd(cmd)


def pull_images_list_from_file(images_list_path):
    if not os.path.exists(images_list_path):
        print("the images list path {} not exists".format(images_list_path))
        sys.exit(-1)
    with open(images_list_path, mode='r', encoding='utf-8') as f:
        for i in f.readlines():
            if i:
                pull_and_tag_image(i)


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage()
        sys.exit(-1)

    if sys.argv[2] == '-r':
        images_list_path = sys.argv[3]
        pull_images_list_from_file(images_list_path)

    else:
        image = sys.argv[2]
        pull_and_tag_image(image)

    print("Pull all images completed")
    sys.exit(0)
