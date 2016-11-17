import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('JsonCpp Options')
    opt.add_option('--with-jsoncpp', type='string', default=None,
                   help="enable JsonCpp with 'yes' or specify installation location")

@conf
def check_jsoncpp(ctx, mandatory=True):
    instdir = ctx.options.with_jsoncpp
    if instdir is None or instdir.lower() in ['yes','on','true']:
        ctx.start_msg('Checking for Eigen in PKG_CONFIG_PATH')
        ctx.check_cfg(package='jsoncpp',  uselib_store='JSONCPP', args='--cflags --libs', mandatory=mandatory)
    elif instdir.lower() in ['no','off','false']:
        return
    else:
        ctx.start_msg('Checking for JsonCpp in %s' % instdir)
        ctx.env.LIBPATH_JSONCPP = [ osp.join(instdir, 'lib') ]
        ctx.env.INCLUDES_JSONCPP = [ osp.join(instdir, 'include') ]

    ctx.check_cxx(header_name="json/json.h", use='JSONCPP', mandatory=mandatory)
    ctx.check_cxx(lib='jsoncpp', use='JSONCPP', mandatory=mandatory)
    ctx.end_msg(ctx.env.INCLUDES_JSONCPP[0])


def configure(cfg):
    cfg.check_jsoncpp()
