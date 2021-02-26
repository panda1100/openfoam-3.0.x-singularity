"""
HPCCM recipe for OpenFOAM 3.0.x Singularity image (MPI)
Contents:
  Ubuntu 18.04
  GNU compilers
  OpenMPI 2.1.1
  OFED/MOFED
  PMI2 (SLURM)
  OpenFOAM 3.0.x
Generating recipe (stdout):
  $ hpccm --recipe openfoam-3.0.x.py --format singularity --singularity-version=3.7
"""
from hpccm.templates.git import git

os_version = '18.04'
openfoam_version = '3.0.x'
openmpi_version = '2.1.1'
ofed_version = '4.9-2.2.4.0' # Host system: Ubuntu 20.04 & this ofed_version

# Ubuntu base image
Stage0 += baseimage(image='ubuntu:{}'.format(os_version), _as='build')

# OpenFOAM Dependencies
ospackages = [  'ca-certificates', 'time', 'wget', 'git-core', 'build-essential', 'cmake',
                'libfl-dev', 'bison', 'zlib1g-dev', 'qt4-dev-tools', 'libqt4-dev',
                'libqtwebkit-dev', 'gnuplot', 'libreadline-dev', 'libncurses-dev',
                'libxt-dev', 'libboost-system-dev', 'libboost-thread-dev', 'libgmp-dev',
                'libmpfr-dev', 'python', 'python-dev', 'libcgal-dev', 'curl']
Stage0 += apt_get(ospackages=ospackages)

compiler = gnu(version=5)
Stage0 += compiler

# (M)OFED
Stage0 += mlnx_ofed(version=ofed_version)

# UCX: no UCX for this recipe, due to OF30x uses OpenMPI 2.1.1

# PMI2
Stage0 += slurm_pmi2()

# OpenMPI
Stage0 += openmpi(
                cuda=False,
                infiniband=True,
                pmi='/usr/local/slurm-pmi2',
                ucx=False,
                toolchain=compiler.toolchain,
                version=openmpi_version)

# OpenFOAM
Stage0 += shell(commands=[
	'mkdir -p /opt/OpenFOAM',
	'cd /opt/OpenFOAM',
	git().clone_step(repository='https://github.com/OpenFOAM/OpenFOAM-3.0.x.git',
			branch='master', path='/opt/OpenFOAM'),
	git().clone_step(repository='https://github.com/OpenFOAM/ThirdParty-3.0.x.git',
			branch='master', path='/opt/OpenFOAM'),
	r"sed -i 's@^foamInstall=$HOME/$WM_PROJECT@# foamInstall=$HOME/$WM_PROJECT@' /opt/OpenFOAM/OpenFOAM-3.0.x/etc/bashrc",
	r"sed -i 's@^# foamInstall=/opt/$WM_PROJECT@foamInstall=/opt/$WM_PROJECT@' /opt/OpenFOAM/OpenFOAM-3.0.x/etc/bashrc",
	'cd ThirdParty-3.0.x',
	'mkdir download',
	'wget -P download  http://www.paraview.org/files/v4.4/ParaView-v4.4.0-source.tar.gz',
	'wget -P download https://gforge.inria.fr/frs/download.php/file/34099/scotch_6.0.3.tar.gz',
	'wget -P download https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-4.7/CGAL-4.7.tar.xz',
	'tar -xzf download/ParaView-v4.4.0-source.tar.gz',
	'tar -xzf download/scotch_6.0.3.tar.gz',
	'tar -xJf download/CGAL-4.7.tar.xz',
	'mv ParaView-v4.4.0-source ParaView-4.4.0'
	])

Stage0 += shell(commands=[
        '. /opt/OpenFOAM/OpenFOAM-3.0.x/etc/bashrc',
	'cd $WM_THIRD_PARTY_DIR',
	'export QT_SELECT=qt4',
	'./Allwmake',
	'wmSet $FOAM_SETTINGS',
	'cd $WM_THIRD_PARTY_DIR',
	'export QT_SELECT=qt4',
	'wget https://raw.githubusercontent.com/Kitware/VTK/40937e934308e5009e80769dc0c451ee4f157749/IO/Geometry/vtkSTLReader.cxx -O ParaView-4.4.0/VTK/IO/Geometry/vtkSTLReader.cxx',
	r"sed -i 's@^345@34567@' /opt/OpenFOAM/ThirdParty-3.0.x/ParaView-4.4.0/VTK/CMake/vtkCompilerExtras.cmake",
	r"sed -i 's@^345@34567@' /opt/OpenFOAM/ThirdParty-3.0.x/ParaView-4.4.0/VTK/CMake/GenerateExportHeader.cmake",
	'./makeParaView4 -python -mpi -python-lib /usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0 2>&1 | tee log.makePV',
	'wmSet $FOAM_SETTINGS',
	'cd $WM_PROJECT_DIR',
	'export QT_SELECT=qt4',
	'./Allwmake -j 4 2>&1 | tee log.make',
	'./Allwmake -j 4 2>&1 | tee log.make'
	])

Stage0 += shell(commands=['echo ". /opt/OpenFOAM/OpenFOAM-3.0.x/etc/bashrc" >> $SINGULARITY_ENVIRONMENT'])

