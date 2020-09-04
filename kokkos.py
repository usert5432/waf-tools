from . import generic

from waflib import Task
from waflib.TaskGen import extension
from waflib.Tools import ccroot, c_preproc
from waflib.Configure import conf

import os

# from waf's playground
class kokkos_cuda(Task.Task):
    run_str = '${NVCC} ${NVCCFLAGS} ${FRAMEWORKPATH_ST:FRAMEWORKPATH} ${CPPPATH_ST:INCPATHS} ${DEFINES_ST:DEFINES} ${CXX_SRC_F}${SRC} ${CXX_TGT_F} ${TGT}'
    color   = 'GREEN'
    ext_in  = ['.h']
    vars    = ['CCDEPS']
    scan    = c_preproc.scan
    shell   = False

@extension('.kokkos')
def kokkos_hook(self, node):
    options = getattr(self.env, 'KOKKOS_OPTIONS', None)
    if 'cuda' in options:
        print('use nvcc on ', node)
        return self.create_compiled_task('kokkos_cuda', node)
    else:
        return self.create_compiled_task('cxx', node)

def options(opt):
    generic._options(opt, "KOKKOS")
    opt.add_option('--kokkos-options', type='string', help="cuda, ...")

def configure(cfg):
    generic._configure(cfg, "KOKKOS", mandatory=False,
                       incs=["Kokkos_Macros.hpp"], libs=["kokkoscore", "kokkoscontainers", "dl"], bins=["nvcc"])

    options = getattr(cfg.options, 'kokkos_options', None)
    setattr(cfg.env, 'KOKKOS_OPTIONS', options)
    options = getattr(cfg.env, 'KOKKOS_OPTIONS', None)
    print('KOKKOS_OPTIONS                           :', options)

    if not 'HAVE_KOKKOS' in cfg.env:
        return
    nvccflags = "-x cu -shared -Xcompiler -fPIC "
    # nvccflags += "--std=c++11 "
    nvccflags += "-Xcudafe --diag_suppress=esa_on_defaulted_function_ignored -expt-extended-lambda -arch=sm_75 -Xcompiler -fopenmp "
    nvccflags += os.environ.get("NVCCFLAGS","")
    cfg.env.NVCCFLAGS += nvccflags.strip().split()
    print ("KOKKOS: NVCCFLAGS = %s" % (' '.join(cfg.env.NVCCFLAGS)))
