#!/bin/bash

#SBATCH --account=project_465000061
#SBATCH --job-name=gwr
#SBATCH --time=0-2:0:0
#SBATCH --partition=standard
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=128  # 1 node has 128 cores
#SBATCH --cpus-per-task=1

# OpenMp Environment
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# threads : hardware/logical thread
# cores : core (having one or more hardware threads)
# sockets : socket (consisting of one or more cores)
export OMP_PLACES="cores"

# spread : distribute (spread) the threads as evenly as possible
# close : bind threads close to the master thread
# master : assign the threads to the same place as the master thread
# false : allows threads to be moved between places and disables thread affinity
export OMP_PROC_BIND="close"

# Commands before execution
source $HOME/git_repos/abinit/_build_gnu/modules.sh

rm -f core
ulimit -s unlimited
srun -n $SLURM_NTASKS abinit run.abi > run.log 2> run.err
#srun -n $SLURM_NTASKS abinit run.abi --abimem-level 0 --abimem-limit-mb 10 --use-mpi-in-place=yes > run.log 2> run.err

# !!  level = Integer selecting the operation mode:
# !!       0 -> no file abimem.mocc is created, only memory allocation counters running
# !!       1 -> light version. Only memory peaks are written.
# !!       2 -> file abimem.mocc is created with full information inside.
# !!       3 -> Write info only if allocation/deallocation is larger or smaller than limit_mb
# !!                depending on of the sign of limit_mb
# !!    NOTE: By default, only master node writes, use negative values to make all MPI procs write info to disk.
# !!  [delta_time]=Interval in second for snapshots. Will write report to std_out evety delta_time seconds.
# !!  [filename] = If present, activate memory logging only inside filename (basename).
# !!  [limit_mb]= Set memory limit in Mb if level == 3. Print allocation/deallocation only above this limit.
# !!    Positive value to print above the threshold.
# !!    Negative value to print below the threshold.

