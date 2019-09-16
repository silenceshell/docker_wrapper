# docker_wrapper
An wrapper of docker for pulling image from gcr.io/k8s.gcr.io/quay.io

# install

```bash
git clone https://github.com/silenceshell/docker_wrapper.git
sudo cp docker_wrapper/docker_wrapper.py /usr/local/bin/docker_wrapper
```

# usage

You can use docker_wrapper to pull images from `gcr.io/k8s.gcr.io/quay.io` and also from `hub.docker.com`. In the later condition, It will directly pull from `hub.docker.com`.

```bash
docker_wrapper pull k8s.gcr.io/kube-apiserver:v1.14.1
docker_wrapper pull gcr.io/google_containers/kube-apiserver:v1.14.1
docker_wrapper pull quay.io/coreos/flannel:v0.10.0-amd64
docker_wrapper pull nginx
docker_wrapper pull silenceshell/godaddy:0.0.2
```
