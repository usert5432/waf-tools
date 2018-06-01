#!/usr/bin/env python
'''
This is NOT a waf tool but generic functions to be called from a waf
tool, in particular by wcb.py.

There's probably a wafier way to do this.

The interpretation of options are very specific so don't change them
unless you really know all the use cases.  The rules are:

1) Give no --with-NAME* or --with-NAME=yes then try to use pkg-config
2) Give --with-NAME=no then do NOT use it, this may fail package is mandatory
3) Give --with-NAME=/path use it as default path for inc/lib
4) Give any --with-NAME-{include,lib} then do NOT use pkg-config and use it to locate inc/lib

'''

import os.path as osp
def _options(opt, name):
    lower = name.lower()
    opt = opt.add_option_group('%s Options' % name)
    opt.add_option('--with-%s'%lower, type='string', default=None,
                   help="give %s installation location" % name)
    opt.add_option('--with-%s-include'%lower, type='string', 
                   help="give %s include installation location"%name)
    opt.add_option('--with-%s-lib'%lower, type='string', 
                   help="give %s lib installation location"%name)
    return

def _configure(ctx, name, incs=(), libs=(), pcname=None, mandatory=True):
    lower = name.lower()
    UPPER = name.upper()
    if pcname is None:
        pcname = lower

    inst = getattr(ctx.options, 'with_'+lower, None)
    inc = getattr(ctx.options, 'with_%s_include'%lower, None)
    lib = getattr(ctx.options, 'with_%s_lib'%lower, None)

    if inst and inst.lower() in ['no','off','false']:
        assert(not mandatory)
        return

    # rely on package config
    if not any([inst,inc,lib]) or (inst and inst.lower() in ['yes','on','true']):
        ctx.start_msg('Checking for %s in PKG_CONFIG_PATH' % name)
        args = "--cflags"
        if libs:                # things like eigen may not have libs
            args += " --libs"
        ctx.check_cfg(package=pcname,  uselib_store=UPPER,
                      args=args, mandatory=mandatory)
        ctx.end_msg(["failed","found"][getattr(ctx.env, 'HAVE_' + UPPER, None)])

    else:                       # do manual setting

        if incs:
            if not inc and inst:
                inc = osp.join(inst, 'include')
            if inc:
                setattr(ctx.env, 'INCLUDES_'+UPPER, [inc])

        if libs:
            if not lib and inst:
                lib = osp.join(inst, 'lib')
            if lib:
                setattr(ctx.env, 'LIBPATH_'+UPPER, [lib])

    
    # now check, this does some extra work in the caseof pkg-config

    if incs:
        ctx.start_msg("Location for %s headers" % name)
        for tryh in incs:
            ctx.check_cxx(header_name=tryh,
                          use=UPPER, uselib_store=UPPER, mandatory=mandatory)
        ctx.end_msg(str(getattr(ctx.env, 'INCLUDES_' + UPPER, None)))

    if libs:
        ctx.start_msg("Location for %s libs" % name)
        for tryl in libs:
            ctx.check_cxx(lib=tryl,
                          use=UPPER, uselib_store=UPPER, mandatory=mandatory)
        ctx.end_msg(str(getattr(ctx.env, 'LIBPATH_' + UPPER, None)))

        ctx.start_msg("Libs for %s" % name)
        ctx.end_msg(str(getattr(ctx.env, 'LIB_' + UPPER)))
