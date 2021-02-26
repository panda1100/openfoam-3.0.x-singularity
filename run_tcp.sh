# run without SLURM
/usr/local/openmpi/bin/mpirun -np 4 --mca btl ^openib --hostfile /srv/hostfile /srv/singularity/bin/singularity exec /srv/openfoam-3.0.x.sif rhoPimpleFoam -parallel

#real    22m5.139s
#user    31m15.791s
#sys     13m36.902s
