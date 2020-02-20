TODO: merge https://github.com/Phelimb/BIGSI/blob/master/Dockerfile into this

TLDR: Pull the docker image and run in a singularity container as:
```
singularity exec docker://leandroishilima/bigsi_700k:0.0.1 <bigsi_args>
```

Wraps all dependencies in a `docker`/`singularity` container. NB: all current dependencies are all installed with `conda`, so we could simply use conda, but using a container is more isolated and extensible.

1. Build the `docker` image:
```
sudo docker build . -t leandroishilima/bigsi_700k:0.0.1
```

2. Convert docker image to singularity image to run in HPC (note: you have to specify the `singularity` version you want to export to (in the cluster, we currently have v2.6)):
```
SING_VERSION="v2.6"
mkdir sing_image
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`/sing_image:/output --privileged -t --rm quay.io/singularity/docker2singularity:${SING_VERSION} leandroishilima/bigsi_700k:0.0.1
```

3. Optionally run the singularity image to make sure everything is fine:
```
cd sing_image
singularity exec leandroishilima/bigsi_700k:0.0.1-<date_id>.simg bigsi
```
