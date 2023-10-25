FROM debian:buster

ARG SRIM_DIR="/tmp"

ARG VERSION=v0.5.10
ARG USERNAME=costrouc
ARG PROJECT=pysrim


RUN dpkg --add-architecture i386

# zlib1g-dev and libjpeg-dev and are required for Pillow (matplotlib)
RUN apt update && \
    apt install wget unzip xvfb wine32 cabextract zlib1g-dev libjpeg-dev python3.7 python3-pip -y && \
    rm -rf /var/lib/apt/lists/*

# winetricks
RUN cd /opt && \
    wget -q https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks && \
    chmod +x winetricks && \
    cp winetricks /usr/local/bin

# https://appdb.winehq.org/objectManager.php?sClass=version&iId=27152
RUN xvfb-run winetricks -q comdlg32ocx msflxgrd richtx32 vb5run comctl32ocx tabctl32

# install SRIM 2013
RUN mkdir -p $SRIM_DIR && \
    cd $SRIM_DIR && \
    wget -q https://gitlab.com/costrouc/pysrim/raw/master/assets/srim.2013.zip && \
    unzip srim.2013.zip && \
    cd "$SRIM_DIR/srim" && \
    echo "1" > $SRIM_DIR/srim/TRIMAUTO

RUN pip3 install --no-cache-dir https://github.com/$USERNAME/$PROJECT/archive/refs/tags/$VERSION.tar.gz
