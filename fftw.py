import os
import os.path as osp
from waflib.Configure import conf

def options(opt):
    opt = opt.add_option_group('FFTW Options')
    opt.add_option('--with-fftw', type='string',
                   help="give FFTW3 installation location")


@conf
def check_fftw(ctx, mandatory=True):
    instdir = ctx.options.with_fftw

    if instdir is None or instdir.lower() in ['yes','true','on']:
        ctx.start_msg('Checking for FFTW in PKG_CONFIG_PATH')
        ctx.check_cfg(package='fftw3',  uselib_store='FFTW', args='--cflags --libs', mandatory=mandatory)
    elif instdir.lower() in ['no','off','false']:
        return
    else:
        ctx.start_msg('Checking for FFTW in %s' % instdir)
        ctx.env.INCLUDES_FFTW = [ osp.join(instdir,'include/fftw3') ]

    ctx.check(header_name="fftw3.h", use='FFTW', mandatory=mandatory)
    ctx.env.LIB_FFTW += ['fftw3f'] # need to explicitly add floating point version of lib
    if len(ctx.env.INCLUDES_FFTW):
        ctx.end_msg(ctx.env.INCLUDES_FFTW[0])
    else:
        ctx.end_msg('FFTW3 not found')

def configure(cfg):
    cfg.check_fftw()
