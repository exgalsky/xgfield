#----------------------------------------------------------------------
# OPTIONS FOR RUNNING ON SCINET-GPC MACHINES
#----------------------------------------------------------------------

F90 = ftn
F77 = ftn

OPTIMIZE =  

MODFLAG = -module 
OMPLIB = -openmp

FFTW2_PATH = /global/homes/m/malvarez/fftw-2.1.5-prlm
CFITS_PATH = /global/homes/m/malvarez/cfitsio-prlm
GSL_PATH = /global/common/software/spackecp/perlmutter/e4s-22.05/75197/spack/opt/spack/cray-sles15-zen3/gcc-11.2.0/gsl-2.7-fhx3zdzzsac7koioqjzpx2uvg4wg4caw

CC = cc
C++ = CC

OPTIONS = -w 

#----------------------------------------------------------------------
# DO NOT MODIFY THIS FILE
#----------------------------------------------------------------------

FFTLIB = -L$(FFTW2_PATH)/lib -lsrfftw_mpi -lsfftw_mpi -lsrfftw -lsfftw
FFTINC = -I$(FFTW2_PATH)/include 

LIB = $FFTLIB 
INC = $FFTINC 
 
# OBJECT FILES
srcdir  = ./src
objs = \
     $(srcdir)/allocate.o \
     $(srcdir)/allvars.o \
     $(srcdir)/commandline.o \
     $(srcdir)/lpt.o \
     $(srcdir)/main.o \
     $(srcdir)/parallel_io.o \
     $(srcdir)/io.o \
     $(srcdir)/memorytracking.o 

COMPILE_FLAGS = $(OPTIMIZE) $(FFTINC) $(OPTIONS)
LINK_FLAGS    = $(OPTIMIZE) $(FFTLIB) 

EXEC = ./delta2s

OBJS     = $(objs)

.SUFFIXES: .o .C

$(srcdir)/%.o: $(srcdir)/%.C 
	$(C++) $(COMPILE_FLAGS) -c $< -o $@

$(EXEC): $(OBJS) 
	$(C++) $(OBJS) $(LINK_FLAGS) -o $(EXEC)  

clean:
	rm -f $(EXEC) $(OBJS) 


