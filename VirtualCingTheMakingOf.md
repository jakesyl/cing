  * From: http://releases.ubuntu.com/9.10/ubuntu-9.10-server-i386.iso This is the 32 bit edition of the Karmic Koala version of Ubuntu server.
  * Install Gnome GUI:
    * sudo apt-get update
    * sudo apt-get install ubuntu-desktop \
> > > linux-generic-pae
    * restart: sudo halt
  * Install Extras:
```
sudo apt-get install \
    pymol python-matplotlib python-dev cython ipython imagemagick python-scipy python-numpy \
    gawk subversion konsole tcsh csh povray povray-includes python-sqlalchemy \
    eclipse-plugin-cvs \
    jedit curl lynx \
    konsole \
    libx11-dev \
    libmotif-dev \
    libxt-dev libxaw7-dev \
    openssh-server \
    apt-file \ # nice for looking up dependencies
    eclipse-csv eclipse-pde
    postgresql \ #for the default user postgres (password = postgres) and for user i (password = ilovevc)
```
  * Install VMware tools inside guest OS.

  * Copy over goodies through shared folder on host os which in the guest os is at:

> > ` /mnt/hgfs/Desktop `

  * On Ubuntu 9.10 for molmol I had to
    * add a def for AR: ar rcs
    * sudo apt-get install libxt-dev libxaw-headers or the suggested
    * Install the above libs.