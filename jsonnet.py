import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('Jsonnet Options')
    opt.add_option('--with-jsonnet', type='string', default=None,
                   help="give Jsonnet installation location")

@conf
def check_jsonnet(ctx, mandatory=False):
    instdir = ctx.options.with_jsonnet
    # default or user says they want it but doesn't say where it is.  Let's see
    # if pkg-config can find it.
    if instdir is None or instdir.lower() in ['yes','on','true']:   
        ctx.start_msg('Checking for Eigen in PKG_CONFIG_PATH')
        ctx.check_cfg(package='jsoncpp',  uselib_store='JSONCPP', args='--cflags --libs', mandatory=mandatory)
    # user explicitly doesn't want it
    elif instdir.lower() in ['no','off','false']:
        return
    # user wants it and has told us where it is
    else:
        ctx.start_msg('Checking for Jsonnet in %s' % instdir)
        ctx.env.LIBPATH_JSONNET = [ osp.join(instdir, 'lib') ]
        ctx.env.INCLUDES_JSONNET = [ osp.join(instdir, 'include') ]

    ctx.check_cxx(header_name="libjsonnet++.h", use='JSONNET', mandatory=mandatory)
    ctx.check_cxx(lib='jsonnet++', use='JSONNET', mandatory=mandatory)
    if len(ctx.env.INCLUDES_JSONNET):
        ctx.end_msg(ctx.env.INCLUDES_JSONNET[0])
    else:
        ctx.end_msg("Jsonnet not found")


def configure(cfg):
    cfg.check_jsonnet()
