# Build from the docker-pcstudio source root after applying the Save Project fix
# to bin/galaxy_functions.py.

ARG BASE_IMAGE=quay.io/physicell/pcstudio:0.14
FROM ${BASE_IMAGE}

ARG MATPLOTLIB_VERSION=3.10.9

RUN /usr/local/pcstudio-venv/bin/python3 -m pip install \
        --no-cache-dir \
        --no-deps \
        "matplotlib==${MATPLOTLIB_VERSION}" \
    && /usr/local/pcstudio-venv/bin/python3 -c \
        "import matplotlib; assert matplotlib.__version__ == '${MATPLOTLIB_VERSION}'"

COPY bin/galaxy_functions.py /opt/pcstudio/bin/galaxy_functions.py
