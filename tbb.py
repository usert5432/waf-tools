import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('TBB Options')
    opt.add_option('--with-tbb', type='string', help='path to Intel TBB')

@conf
def check_tbb(ctx):
    instdir = ctx.options.with_tbb
    if instdir:
        ctx.start_msg('Checking for TBB in %s' % instdir)
        ctx.env.LIBPATH_TBB = [ osp.join(instdir, 'lib') ]
        ctx.env.INCLUDES_TBB = [ osp.join(instdir, 'include') ]
    else:
        ctx.start_msg('Checking for TBB in system paths')
        ctx.env.LIBPATH_TBB = ['/usr/local/lib/', '/usr/lib', '/opt/intel/tbb/lib']
        ctx.env.INCLUDES_TBB = ['/usr/local/include', '/usr/include', '/opt/intel/tbb/include']

    ctx.check(header_name='tbb/parallel_for.h', use='TBB')
    ctx.check_cxx(lib='tbb', use='TBB')
    ctx.end_msg(ctx.env.INCLUDES_TBB[0])

def configure(cfg):
    cfg.check_tbb()
