'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_SGIX_shadow'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_SGIX_shadow',error_checker=_errors._error_checker)
GL_TEXTURE_COMPARE_OPERATOR_SGIX=_C('GL_TEXTURE_COMPARE_OPERATOR_SGIX',0x819B)
GL_TEXTURE_COMPARE_SGIX=_C('GL_TEXTURE_COMPARE_SGIX',0x819A)
GL_TEXTURE_GEQUAL_R_SGIX=_C('GL_TEXTURE_GEQUAL_R_SGIX',0x819D)
GL_TEXTURE_LEQUAL_R_SGIX=_C('GL_TEXTURE_LEQUAL_R_SGIX',0x819C)

