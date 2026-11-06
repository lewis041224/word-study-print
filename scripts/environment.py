"""Read-only capability detection; never installs packages or changes system settings."""
import importlib
import importlib.util
import platform
import shutil
import sys


def doctor():
    packages = {}
    for module, package in [('docx', 'python-docx'), ('pypdf', 'pypdf'), ('openpyxl', 'openpyxl')]:
        try:
            imported = importlib.import_module(module)
            packages[package] = dict(available=True, version=getattr(imported, '__version__', 'unknown'))
        except (ImportError, OSError):
            packages[package] = dict(available=False, version=None)
    supported = sys.version_info >= (3, 10)
    report = dict(python=sys.version.split()[0], executable=sys.executable,
                  architecture=platform.machine(), python_supported=supported,
                  packages=packages, pip_available=importlib.util.find_spec('pip') is not None,
                  can_build=supported and packages['python-docx']['available'],
                  can_read_pdf=supported and packages['pypdf']['available'],
                  can_read_xlsx=supported and packages['openpyxl']['available'],
                  libreoffice_available=bool(shutil.which('soffice') or shutil.which('libreoffice')),
                  image_ocr='Requires host AI vision; not provided by this program',
                  font_check='Not performed; DOCX writing does not require installed fonts; PDF preview may substitute fonts')
    report['advice'] = ('可生成Word；PDF、Excel和渲染能力按各项状态判断。' if report['can_build'] else
                        '请使用Python 3.10+并在当前解释器环境安装python-docx；无需sudo或LibreOffice。')
    report['install_core_argv'] = [sys.executable, '-m', 'pip', 'install', 'python-docx>=1.1,<2']
    return report
