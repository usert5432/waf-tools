# Aggregate all the waftools to make the wscript shorter.


from waflib.Utils import to_list

import os.path as osp
mydir = osp.dirname(__file__)

def options(opt):

    # from here
    opt.load('smplpkgs',tooldir=mydir)
    opt.load('rootsys',tooldir=mydir)
    opt.load('fftw',tooldir=mydir)
    opt.load('eigen',tooldir=mydir)
    opt.load('jsoncpp',tooldir=mydir)
    opt.load('tbb',tooldir=mydir)

    opt.add_option('--build-debug', default='-O2 -ggdb3',
                   help="Build with debug symbols")

def configure(cfg):
    print 'Compile options: %s' % cfg.options.build_debug

    cfg.load('smplpkgs')
    cfg.load('rootsys')
    cfg.load('eigen')
    cfg.load('jsoncpp')
    cfg.load('tbb')
    cfg.load('fftw')


    cfg.check_boost(lib='system filesystem graph thread program_options iostreams')

    cfg.check_cxx(header_name="boost/pipeline.hpp", use='BOOST',
                  define_name='BOOST_PIPELINE', mandatory=False)
    cfg.check(header_name="dlfcn.h", uselib_store='DYNAMO',
              lib=['dl'], mandatory=True)


    cfg.check(features='cxx cxxprogram', lib=['pthread'], uselib_store='PTHREAD')

    # boost 1.59 uses auto_ptr and GCC 5 deprecates it vociferously.
    cfg.env.CXXFLAGS += ['-Wno-deprecated-declarations']

    cfg.env.CXXFLAGS += to_list(cfg.options.build_debug)
    cfg.env.CXXFLAGS += ['-DEIGEN_FFTW_DEFAULT=1']

    cfg.env.SUBDIRS = 'util iface gen alg sst bio rootvis apps sigproc'.split()

    if 'BOOST_PIPELINE=1' in cfg.env.DEFINES:
        cfg.env.SUBDIRS += ['dfp'] # fixme: rename, make B.P specific

    if 'HAVE_TBB_TBB_H=1' in cfg.env.DEFINES:
        cfg.env.SUBDIRS += ['tbb']

    #print cfg.env
    
