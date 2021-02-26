sudo apt-get update
sudo apt-get install -y \
	build-essential uuid-dev libgpgme-dev squashfs-tools libseccomp-dev \
	wget pkg-config git cryptsetup-bin
sudo snap install go --classic
git clone https://github.com/hpcng/singularity.git
cd singularity
git checkout v3.7.1
git branch
./mconfig --prefix=/opt/singularity
make -C ./builddir
sudo make -C ./builddir install

