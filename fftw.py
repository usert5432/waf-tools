import os.path as osp
from waflib.Configure import conf


def options(opt):
    opt = opt.add_option_group('FFTW Options')
    opt.add_option('--with-fftw', type='string',
                   help="give FFTW3 installation location")
    opt.add_option('--with-fftw-include', type='string', default='',
                   help="give FFTW3 include installation location")
    opt.add_option('--with-fftw-lib', type='string', default='',
                   help="give FFTW3 lib installation location")
    opt.add_option('--fftw-no-single',  default=False,
                   help="set if your FFTW3 does not have single-precision libfftw3f")


@conf
def check_fftw(ctx, mandatory=True):
    instdir = ctx.options.with_fftw

    if instdir is None or instdir.lower() in ['yes', 'true', 'on']:
        ctx.start_msg('Checking for FFTW in PKG_CONFIG_PATH')
        ctx.check_cfg(package='fftw3',  uselib_store='FFTW',
                      args='--cflags --libs', mandatory=mandatory)
    elif instdir.lower() in ['no', 'off', 'false']:
        return
    else:
        ctx.start_msg('Checking for FFTW in %s' % instdir)
        if ctx.options.with_fftw_include:
            ctx.env.INCLUDES_FFTW = [ctx.options.with_fftw_include]
        else:
            ctx.env.INCLUDES_FFTW = [osp.join(instdir, 'include/fftw3')]
        if ctx.options.with_fftw_lib:
            ctx.env.LIBPATH_FFTW = [ctx.options.with_fftw_lib]

    if ctx.options.fftw_no_single:
        # For now, allow use of float/double/float casting for FFTs at the
        # expense of 15% slower FFTs but to work around missing library at
        # Fermilab so that MicroBooNE can do its processing ASAP.
        print 'Note: will use slower double-precision FFTW3 library ',
        ctx.env.DEFINES_FFTW = ['MISSING_FFTW_SINGLE_PRECISION']
        ctx.env.LIB_FFTW += ['fftw3']
    else:
        ctx.env.LIB_FFTW += ['fftw3f']

    ctx.check(header_name="fftw3.h", use='FFTW', mandatory=mandatory)

    if len(ctx.env.INCLUDES_FFTW):
        ctx.end_msg(ctx.env.INCLUDES_FFTW[0])
    else:
        ctx.end_msg('FFTW3 not found')


def configure(cfg):
    cfg.check_fftw()
