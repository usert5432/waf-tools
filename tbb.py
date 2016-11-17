import os
import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('TBB Options')
    opt.add_option('--with-tbb', type='string',
                   help="give TBB installation location")

@conf
def check_tbb(ctx, mandatory=True):
    instdir = ctx.options.with_tbb

    if instdir is None or instdir.lower() in ['yes','on','true']:
        from_pc = set()
        for maybe in os.environ.get('PKG_CONFIG_PATH','').split(':'):
            from_pc.add(osp.dirname(osp.dirname(maybe))) # strip .../lib/pkgconfig

        ctx.start_msg('Checking for TBB in system paths', mandatory=mandatory)
        ctx.env.LIBPATH_TBB = [d+'/lib' for d in from_pc] + ['/usr/local/lib/', '/usr/lib', '/opt/intel/tbb/lib']
        ctx.env.INCLUDES_TBB = [d+'/include' for d in from_pc] + ['/usr/local/include', '/usr/include', '/opt/intel/tbb/include']
    elif instdir.lower() in ['no','off','false']:
        return
    else:
        ctx.start_msg('Checking for TBB in %s' % instdir)
        ctx.env.LIBPATH_TBB = [ osp.join(instdir, 'lib') ]
        ctx.env.INCLUDES_TBB = [ osp.join(instdir, 'include') ]

    ctx.check(header_name='tbb/parallel_for.h', use='TBB', mandatory=mandatory)
    ctx.check_cxx(lib='tbb', use='TBB', mandatory=mandatory)
    if len(ctx.env.INCLUDES_TBB):
        ctx.end_msg(ctx.env.INCLUDES_TBB[0])
    else:
        ctx.end_msg('TBB not found')

def configure(cfg):
    cfg.check_tbb()
