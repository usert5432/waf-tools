import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('JsonCpp Options')
    opt.add_option('--with-jsoncpp', type='string', default=None, help='path to JsonCpp installation')

@conf
def check_jsoncpp(ctx):
    instdir = ctx.options.with_jsoncpp
    if instdir:
        ctx.start_msg('Checking for JsonCpp in %s' % instdir)
        ctx.env.LIBPATH_JSONCPP = [ osp.join(instdir, 'lib') ]
        ctx.env.INCLUDES_JSONCPP = [ osp.join(instdir, 'include') ]
    else:
        ctx.start_msg('Checking for Eigen in PKG_CONFIG_PATH')
        ctx.check_cfg(package='jsoncpp',  uselib_store='JSONCPP', args='--cflags --libs')

    ctx.check_cxx(header_name="json/json.h", use='JSONCPP', mandatory=True)
    ctx.check_cxx(lib='jsoncpp', use='JSONCPP')
    ctx.end_msg(ctx.env.INCLUDES_JSONCPP[0])


def configure(cfg):
    cfg.check_jsoncpp()
