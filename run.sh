# run without SLURM
/usr/local/openmpi/bin/mpirun -np 4 --mca btl openib,self --hostfile /srv/hostfile /srv/singularity/bin/singularity exec /srv/openfoam-3.0.x.sif rhoPimpleFoam -parallel

#real    9m52.484s
#user    19m43.203s
#sys     0m43.900s
