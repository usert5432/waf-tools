# Aggregate all the waftools to make the wscript shorter.


import os.path as osp
mydir = osp.dirname(__file__)

def options(opt):

    # from here
    opt.load('smplpkgs',tooldir=mydir)
    opt.load('rootsys',tooldir=mydir)
    opt.load('fftw',tooldir=mydir)
    opt.load('eigen',tooldir=mydir)
    opt.load('jsoncpp',tooldir=mydir)
    opt.load('jsonnet',tooldir=mydir)
    opt.load('tbb',tooldir=mydir)

    opt.add_option('--build-debug', default='-O2 -ggdb3',
                   help="Build with debug symbols")

def configure(cfg):
    print 'Compile options: %s' % cfg.options.build_debug

    cfg.load('smplpkgs')
    cfg.load('rootsys')
    cfg.load('eigen')
    cfg.load('jsoncpp')
    cfg.load('jsonnet')
    cfg.load('tbb')
    cfg.load('fftw')



    #print cfg.env
    
