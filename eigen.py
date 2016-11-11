import os
import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('Eigen Options')
    opt.add_option('--with-eigen', type='string', help='path to Eigen3 installation')

@conf
def check_eigen(ctx):
    instdir = ctx.options.with_eigen
    if instdir:
        ctx.start_msg('Checking for Eigen in %s' % instdir)
        ctx.env.INCLUDES_EIGEN = [ osp.join(instdir,'include/eigen3') ]
    else:
        ctx.start_msg('Checking for Eigen in PKG_CONFIG_PATH')
        # note: Eigen puts its eigen3.pc file under share as there is
        # no lib.  Be sure your PKG_CONFIG_PATH reflects this.
        ctx.check_cfg(package='eigen3',  uselib_store='EIGEN', args='--cflags --libs')
    ctx.check(header_name="Eigen/Dense", use='EIGEN')
    ctx.end_msg(ctx.env.INCLUDES_EIGEN[0])

def configure(cfg):
    cfg.check_eigen()
