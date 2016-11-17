import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('TBB Options')
    opt.add_option('--with-tbb', type='string',
                   help="enable TBB with 'yes' or specify installation location")

@conf
def check_tbb(ctx, mandatory=True):
    instdir = ctx.options.with_tbb
    if instdir is None:
        return

    if instdir.lower() in ['yes','on','true']:
        ctx.start_msg('Checking for TBB in system paths', mandatory=mandatory)
        ctx.env.LIBPATH_TBB = ['/usr/local/lib/', '/usr/lib', '/opt/intel/tbb/lib']
        ctx.env.INCLUDES_TBB = ['/usr/local/include', '/usr/include', '/opt/intel/tbb/include']
    else:
        ctx.start_msg('Checking for TBB in %s' % instdir)
        ctx.env.LIBPATH_TBB = [ osp.join(instdir, 'lib') ]
        ctx.env.INCLUDES_TBB = [ osp.join(instdir, 'include') ]

    ctx.check(header_name='tbb/parallel_for.h', use='TBB', mandatory=mandatory)
    ctx.check_cxx(lib='tbb', use='TBB', mandatory=mandatory)
    ctx.end_msg(ctx.env.INCLUDES_TBB[0])

def configure(cfg):
    cfg.check_tbb()
