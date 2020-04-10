import PyInstaller.__main__
import os.path
from pycroaktools.windows.options import Options
import distutils.file_util as fileutil
import distutils.dir_util as dirutil
from distutils.dist import DistutilsError
import logging


class Package:

    def __init__(self, options: Options, data=None, example_folder=None, doc_folder=None):
        command = []
        root_path = '/dist'
        modulename, _ = os.path.splitext(options.package)
        name = os.path.basename(modulename)
        if options.name:
            command.append('--name={}'.format(options.name))
            name = options.name
        if options.onefile:
            command.append('--onefile')
        if options.no_confirm:
            command.append('--noconfirm')
        if options.console:
            command.append('--console')
        else:
            command.append('--noconsole')
        if options.icon:
            command.append('--icon={}'.format(options.icon))
        if options.distpath:
            command.append('--distpath={}'.format(options.distpath))
            root_path = options.distpath
        if options.workpath:
            command.append('--workpath={}'.format(options.workpath))
        if options.clean:
            command.append('--clean')
        if options.specpath:
            command.append('--specpath={}'.format(options.specpath))
        if options.paths:
            for path in options.paths:
                command.append('--paths={}'.format(path))
        if options.hiddenimports:
            for module in options.hiddenimports:
                command.append('--hidden-import={}'.format(module))
        if options.additionalhooks:
            for path in options.additionalhooks:
                command.append('--additional-hooks-dir={}'.format(path))
        if options.runtimehooks:
            for path in options.runtimehooks:
                command.append('--runtime-hook={}'.format(path))
        if options.excludemodules:
            for module in options.excludemodules:
                command.append('--exclude-module={}'.format(module))
        if options.binaries:
            for src in options.binaries:
                command.append('--add-binary={}{}{}'.format(src,
                                                            os.path.pathsep, options.binaries[src]))
   
        command.append(options.package)

        self._package(command)
        self._createbat(root_path, name)
        self._copyFilesAndFolders(data, root_path, name)

    def _package(self, command):
        PyInstaller.__main__.run(command)

    def _createbat(self, path, name):
        file = os.path.join(path, name+'.bat')
        with open(file, 'w') as f:
            f.write('START '+os.path.join(name, name+'.exe'))

    def _copyFilesAndFolders(self, data, root_path, name):
        for dataobj in data:
            src = dataobj['src']
            dest = dataobj['dst'] if 'dst' in dataobj else ''
            root_level = dataobj['root_level']
            if root_level:
                dest = os.path.join(root_path, dest)
            else:
                dest = os.path.join(root_path, name, dest)
            if os.path.isdir(src):                
                self._copyFolder(src, dest)
            else:
                self._copyFile(src, dest)

    def _copyFolder(self, src, dest):
        if not src:
            return
        try:
            dirutil.copy_tree(src, dest)
        except DistutilsError:
            logging.warning("can't copy {} from {}".format(dest, src))

    def _copyFile(self, src, dest):
        if not src:
            return
        try:
            fileutil.copy_file(src, os.path.join(dest, os.path.basename(src)))
        except DistutilsError:
            logging.warning("can't copy {} from {}".format(dest, src))
