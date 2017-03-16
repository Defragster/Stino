#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Package Docs."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import glob
import codecs
from base_utils import file
from base_utils import default_st_dirs
from base_utils import c_file
from . import const
from . import selected

plugin_name = const.PLUGIN_NAME


def write_menu(menu_type, menu_text):
    """."""
    file_name = 'Main.sublime-menu'
    menu_path = default_st_dirs.get_plugin_menu_path(plugin_name)
    dir_path = os.path.join(menu_path, menu_type)
    file.check_dir(dir_path)
    file_path = os.path.join(dir_path, file_name)
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(menu_text)


def get_sketch_menu_text(level, paths):
    """."""
    text = ''
    none_sketches = ['libraries', 'examples', 'hardware']
    for path in paths:
        path = path.replace('\\', '/')
        name = os.path.basename(path)
        if name in none_sketches:
            continue

        has_sketch = False
        next_paths = glob.glob(path + '/*')
        next_file_paths = [p for p in next_paths if os.path.isfile(p)]
        next_dir_paths = [p for p in next_paths if os.path.isdir(p)]

        for file_path in next_file_paths:
            ext = os.path.splitext(file_path)[-1]
            if ext in c_file.INOC_EXTS:
                has_sketch = True
                break

        if not (has_sketch or next_dir_paths):
            continue
        elif not next_dir_paths:
            text += ',\n'
            text += '\t' * level + '{\n'
            text += '\t' * (level + 1)
            text += '"caption": "%s",\n' % name
            text += '\t' * (level + 1)
            text += '"id": "stino_sketch_%s",\n' % name
            text += '\t' * (level + 1)
            text += '"command": "stino_open_sketch",\n'
            text += '\t' * (level + 1)
            text += '"args": {"sketch_path": "%s"}\n' % path
            text += '\t' * level
            text += '}'
        elif not has_sketch:
            text += ',\n'
            text += '\t' * level + '{\n'
            text += '\t' * (level + 1)
            text += '"caption": "%s",\n' % name
            text += '\t' * (level + 1)
            text += '"id": "stino_sketch_%s",\n' % name
            text += '\t' * (level + 1)
            text += '"children":\n'
            text += '\t' * (level + 1)
            text += '[\n'
            text += '\t' * (level + 2)
            text += '{"caption": "-"}'
            text += get_sketch_menu_text(level + 2, next_paths)
            text += '\t' * (level + 1)
            text += ']\n'
            text += '\t' * level
            text += '}'
        else:
            text += ',\n'
            text += '\t' * level + '{\n'
            text += '\t' * (level + 1)
            text += '"caption": "%s",\n' % name
            text += '\t' * (level + 1)
            text += '"id": "stino_sketch_%s",\n' % name

            text += '\t' * (level + 1)
            text += '"children":\n'
            text += '\t' * (level + 1)
            text += '[\n'
            text += '\t' * (level + 1) + '{\n'
            text += '\t' * (level + 2)
            text += '"caption": "Open",\n'
            text += '\t' * (level + 2)
            text += '"id": "stino_open_%s",\n' % name
            text += '\t' * (level + 2)
            text += '"command": "stino_open_sketch",\n'
            text += '\t' * (level + 2)
            text += '"args": {"sketch_path": "%s"}\n' % path
            text += '\t' * (level + 1)
            text += '},'

            text += '\t' * (level + 2)
            text += '{"caption": "-"}'
            text += get_sketch_menu_text(level + 2, next_paths)
            text += '\t' * (level + 1)
            text += ']\n'

            text += '\t' * level
            text += '}'
    return text


def update_sketchbook_menu(arduino_info):
    """."""
    sketchbook_path = arduino_info.get('sketchbook_path')
    sketch_paths = glob.glob(sketchbook_path + '/*')
    sketch_paths = [p for p in sketch_paths if os.path.isdir(p)]

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Open Sketch",\n'
    text += '\t' * 4 + '"id": "stino_sketchbook",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_sketchbook",\n'
    text += '\t' * 6 + '"command": "stino_refresh_sketchbook"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Change Location...",\n'
    text += '\t' * 6 + '"id": "stino_change_sketchbook_location",\n'
    text += '\t' * 6 + '"command": "stino_change_sketchbook_location"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "In New Window",\n'
    text += '\t' * 6 + '"id": "stino_open_in_new_win",\n'
    text += '\t' * 6 + '"command": "stino_open_in_new_win",\n'
    text += '\t' * 6 + '"checkbox": true\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"},'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "New Sketch...",\n'
    text += '\t' * 6 + '"id": "stino_new_sketch",\n'
    text += '\t' * 6 + '"command": "stino_new_sketch"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    text += get_sketch_menu_text(5, sketch_paths)

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('sketchbook', text)


# def update_sketchbook_menu(arduino_info):
#     """."""
#     none_sketches = ['libraries', 'examples']
#     sketchbook_path = arduino_info.get('sketchbook_path')
#     sketch_paths = glob.glob(sketchbook_path + '/*')
#     sketch_paths = [p for p in sketch_paths if os.path.isdir(p)]

#     text = '\t' * 0 + '[\n'
#     text += '\t' * 1 + '{\n'
#     text += '\t' * 2 + '"caption": "Arduino",\n'
#     text += '\t' * 2 + '"mnemonic": "A",\n'
#     text += '\t' * 2 + '"id": "arduino",\n'
#     text += '\t' * 2 + '"children":\n'
#     text += '\t' * 2 + '[\n'
#     text += '\t' * 3 + '{\n'
#     text += '\t' * 4 + '"caption": "Open Sketch",\n'
#     text += '\t' * 4 + '"id": "stino_sketchbook",\n'
#     text += '\t' * 4 + '"children":\n'
#     text += '\t' * 4 + '[\n'
#     text += '\t' * 5 + '{\n'
#     text += '\t' * 6 + '"caption": "Refresh",\n'
#     text += '\t' * 6 + '"id": "stino_refresh_sketchbook",\n'
#     text += '\t' * 6 + '"command": "stino_refresh_sketchbook"\n'
#     text += '\t' * 5 + '},\n'
#     text += '\t' * 5 + '{\n'
#     text += '\t' * 6 + '"caption": "Change Location...",\n'
#     text += '\t' * 6 + '"id": "stino_change_sketchbook_location",\n'
#     text += '\t' * 6 + '"command": "stino_change_sketchbook_location"\n'
#     text += '\t' * 5 + '},\n'
#     text += '\t' * 5 + '{\n'
#     text += '\t' * 6 + '"caption": "In New Window",\n'
#     text += '\t' * 6 + '"id": "stino_open_in_new_win",\n'
#     text += '\t' * 6 + '"command": "stino_open_in_new_win",\n'
#     text += '\t' * 6 + '"checkbox": true\n'
#     text += '\t' * 5 + '},\n'
#     text += '\t' * 5 + '{"caption": "-"},'
#     text += '\t' * 5 + '{\n'
#     text += '\t' * 6 + '"caption": "New Sketch...",\n'
#     text += '\t' * 6 + '"id": "stino_new_sketch",\n'
#     text += '\t' * 6 + '"command": "stino_new_sketch"\n'
#     text += '\t' * 5 + '},\n'
#     text += '\t' * 5 + '{"caption": "-"}'

#     for sketch_path in sketch_paths:
#         sketch_path = sketch_path.replace('\\', '/')
#         sketch_name = os.path.basename(sketch_path)
#         if sketch_name in none_sketches:
#             continue
#         text += ',\n'
#         text += '\t' * 5 + '{\n'
#         text += '\t' * 6 + '"caption": "%s",\n' % sketch_name
#         text += '\t' * 6 + '"id": "stino_sketch_%s",\n' % sketch_name
#         text += '\t' * 6 + '"command": "stino_open_sketch",\n'
#         text += '\t' * 6 + '"args": {"sketch_path": "%s"}\n' % sketch_path
#         text += '\t' * 5 + '}'

#     text += '\n' + '\t' * 4 + ']\n'
#     text += '\t' * 3 + '}\n'
#     text += '\t' * 2 + ']\n'
#     text += '\t' * 1 + '}\n'
#     text += '\t' * 0 + ']\n'

#     write_menu('sketchbook', text)


def get_example_menu_text(level, paths):
    """."""
    text = ''
    for path in paths:
        path = path.replace('\\', '/')
        name = os.path.basename(path)
        file_path = os.path.join(path, name + '.ino')

        text += ',\n'
        text += '\t' * level + '{\n'
        text += '\t' * (level + 1)
        text += '"caption": "%s",\n' % name
        text += '\t' * (level + 1)
        text += '"id": "stino_example_%s",\n' % name
        text += '\t' * (level + 1)

        if os.path.isfile(file_path):
            text += '"command": "stino_open_example",\n'
            text += '\t' * (level + 1)
            text += '"args": {"example_path": "%s"}\n' % path

        else:
            next_paths = glob.glob(path + '/*')
            next_paths = [p for p in next_paths if os.path.isdir(p)]
            text += '"children":\n'
            text += '\t' * (level + 1)
            text += '[\n'
            text += '\t' * (level + 2)
            text += '{"caption": "-"}'
            text += get_example_menu_text(level + 2, next_paths)
            text += '\t' * (level + 1)
            text += ']\n'

        text += '\t' * level
        text += '}'
    return text


def update_example_menu(arduino_info):
    """."""
    ext_app_path = arduino_info.get('ext_app_path')
    sketchbook_path = arduino_info.get('sketchbook_path')

    paths = []
    if os.path.isdir(ext_app_path):
        paths.append(ext_app_path)
    paths.append(sketchbook_path)

    all_paths = []
    for path in paths:
        examples_path = os.path.join(path, 'examples')
        example_paths = glob.glob(examples_path + '/*')
        example_paths = [p for p in example_paths if os.path.isdir(p)]

        libraries_path = os.path.join(path, 'libraries')
        library_paths = glob.glob(libraries_path + '/*')
        library_paths = [p for p in library_paths if os.path.isdir(p)]
        all_paths.append(example_paths)
        all_paths.append(library_paths)

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Open Example",\n'
    text += '\t' * 4 + '"id": "stino_examples",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_examples",\n'
    text += '\t' * 6 + '"command": "stino_refresh_examples"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    sep_text = ',\n' + '\t' * 5 + '{"caption": "-"}'
    sub_texts = []
    for paths in all_paths:
        sub_texts.append(get_example_menu_text(5, paths))
    text += sep_text.join(sub_texts)

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('examples', text)


def update_library_menu(arduino_info):
    """."""
    ext_app_path = arduino_info.get('ext_app_path')
    sketchbook_path = arduino_info.get('sketchbook_path')

    paths = []
    if os.path.isdir(ext_app_path):
        paths.append(ext_app_path)
    paths.append(sketchbook_path)

    all_paths = []
    for path in paths:
        libraries_path = os.path.join(path, 'libraries')
        library_paths = glob.glob(libraries_path + '/*')
        library_paths = [p for p in library_paths if os.path.isdir(p)]
        all_paths.append(library_paths)

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Import Library",\n'
    text += '\t' * 4 + '"id": "stino_import_library",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_libraries",\n'
    text += '\t' * 6 + '"command": "stino_refresh_libraries"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    sep_text = ',\n' + '\t' * 5 + '{"caption": "-"}'
    sub_texts = []
    for paths in all_paths:
        sub_text = ''
        for library_path in paths:
            library_path = library_path.replace('\\', '/')
            library_name = os.path.basename(library_path)
            sub_text += ',\n'
            sub_text += '\t' * 5 + '{\n'
            sub_text += '\t' * 6 + '"caption": "%s",\n' % library_name
            sub_text += '\t' * 6 + '"id": "stino_library_%s",\n' % library_name
            sub_text += '\t' * 6 + '"command": "stino_import_library",\n'
            sub_text += '\t' * 6 + '"args": {"library_path": '
            sub_text += '"%s"}\n' % library_path
            sub_text += '\t' * 5 + '}'
        sub_texts.append(sub_text)
    text += sep_text.join(sub_texts)

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('libraries', text)


def update_install_library_menu(arduino_info):
    """."""
    libraries_info = arduino_info.get('libraries', {})
    lib_cats = libraries_info.get('categorys', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Install Library",\n'
    text += '\t' * 4 + '"id": "stino_install_library",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_install_library",\n'
    text += '\t' * 6 + '"command": "stino_refresh_install_library"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for lib_cat in lib_cats:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % lib_cat
        text += '\t' * 6 + '"id": "stino_lib_cat_%s",\n' % lib_cat
        text += '\t' * 6 + '"children":\n'
        text += '\t' * 6 + '[\n'
        text += '\t' * 7 + '{"caption": "-"}'

        cat_info = libraries_info.get(lib_cat, {})
        names = cat_info.get('names', [])
        for name in names:
            text += ',\n'
            text += '\t' * 7 + '{\n'
            text += '\t' * 8 + '"caption": "%s",\n' % name
            text += '\t' * 8 + '"id": "stino_lib_cat_name_%s",\n' % name
            text += '\t' * 8 + '"children":\n'
            text += '\t' * 8 + '['
            text += '\t' * 9 + '{"caption": "-"}'

            name_info = cat_info.get(name, {})
            versions = name_info.get('versions', [])
            for version in versions:
                text += ',\n'
                text += '\t' * 9 + '{'
                text += '\t' * 10 + '"caption": "%s",\n' % version
                text += '\t' * 10 + '"id": '
                text += '"stino_lib_cat_name_ver_%s",\n' % version
                text += '\t' * 10 + '"command": "stino_install_lib",\n'

                arg_text = '"args": {"category": "%s", ' % lib_cat
                arg_text += '"name": "%s", ' % name
                arg_text += '"version": "%s"}\n' % version
                text += '\t' * 10 + arg_text
                text += '\t' * 9 + '}'

            text += '\n' + '\t' * 8 + ']'
            text += '\t' * 7 + '}'

        text += '\n' + '\t' * 6 + ']\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('install_library', text)


def update_install_platform_menu(arduino_info):
    """."""
    packages_info = arduino_info.get('packages', {})
    package_names = packages_info.get('names', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Install Platform",\n'
    text += '\t' * 4 + '"id": "stino_install_platform",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_install_platform",\n'
    text += '\t' * 6 + '"command": "stino_refresh_install_platform"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Add Package",\n'
    text += '\t' * 6 + '"id": "stino_add_package",\n'
    text += '\t' * 6 + '"command": "stino_add_package"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Add Arduino IDE",\n'
    text += '\t' * 6 + '"id": "stino_add_ide",\n'
    text += '\t' * 6 + '"command": "stino_add_ide"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for package_name in package_names:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % package_name
        text += '\t' * 6 + '"id": "stino_package_%s",\n' % package_name
        text += '\t' * 6 + '"children":\n'
        text += '\t' * 6 + '[\n'
        text += '\t' * 7 + '{"caption": "-"}'

        package_info = packages_info.get(package_name, {})
        platforms_info = package_info.get('platforms', {})
        platform_names = platforms_info.get('names', [])
        for platform_name in platform_names:
            text += ',\n'
            text += '\t' * 7 + '{\n'
            text += '\t' * 8 + '"caption": "%s",\n' % platform_name
            text += '\t' * 8 + '"id": "stino_platform_%s",\n' % platform_name
            text += '\t' * 8 + '"children":\n'
            text += '\t' * 8 + '['
            text += '\t' * 9 + '{"caption": "-"}'

            platform_info = platforms_info.get(platform_name, {})
            versions = platform_info.get('versions', [])
            for version in versions:
                text += ',\n'
                text += '\t' * 9 + '{'
                text += '\t' * 10 + '"caption": "%s",\n' % version
                text += '\t' * 10 + '"id": "stino_platform_%s",\n' % version
                text += '\t' * 10 + '"command": "stino_install_platform",\n'

                arg_text = '"args": {"package_name": "%s", ' % package_name
                arg_text += '"platform_name": "%s", ' % platform_name
                arg_text += '"version": "%s"}\n' % version
                text += '\t' * 10 + arg_text
                text += '\t' * 9 + '}'

            text += '\n' + '\t' * 8 + ']'
            text += '\t' * 7 + '}'

        text += '\n' + '\t' * 6 + ']\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('install_platform', text)


def update_platform_menu(arduino_info):
    """."""
    packages_info = arduino_info.get('installed_packages', {})
    package_names = packages_info.get('names', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Platform",\n'
    text += '\t' * 4 + '"id": "stino_platform",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_platforms",\n'
    text += '\t' * 6 + '"command": "stino_refresh_platforms"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for package_name in package_names:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % package_name
        text += '\t' * 6 + '"id": "stino_package_%s",\n' % package_name
        text += '\t' * 6 + '"children":\n'
        text += '\t' * 6 + '[\n'
        text += '\t' * 7 + '{"caption": "-"}'

        package_info = packages_info.get(package_name, {})
        platforms_info = package_info.get('platforms', {})
        platform_names = platforms_info.get('names', [])
        for platform_name in platform_names:
            text += ',\n'
            text += '\t' * 7 + '{\n'
            text += '\t' * 8 + '"caption": "%s",\n' % platform_name
            text += '\t' * 8 + '"id": "stino_platform_%s",\n' % platform_name
            text += '\t' * 8 + '"command": "stino_select_platform",\n'

            arg_text = '"args": {"package_name": "%s", ' % package_name
            arg_text += '"platform_name": "%s"},\n' % platform_name
            text += '\t' * 8 + arg_text
            text += '\t' * 8 + '"checkbox": true\n'
            text += '\t' * 7 + '}'

        text += '\n' + '\t' * 6 + ']\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('platform', text)


def update_version_menu(arduino_info):
    """."""
    package_infos = arduino_info.get('installed_packages', {})
    sel_package = arduino_info['selected'].get('package')
    sel_platform = arduino_info['selected'].get('platform')
    versions = selected.get_platform_versions(package_infos, sel_package,
                                              sel_platform)

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Version",\n'
    text += '\t' * 4 + '"id": "stino_platform_version",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_platform_versions",\n'
    text += '\t' * 6 + '"command": "stino_refresh_platform_versions"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Check Toolchain",\n'
    text += '\t' * 6 + '"id": "stino_check_tools",\n'
    text += '\t' * 6 + '"command": "stino_check_tools"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for version in versions:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % version
        text += '\t' * 6 + '"id": "stino_version_%s",\n' % version
        text += '\t' * 6 + '"command": "stino_select_version",\n'
        text += '\t' * 6 + '"args": {"version": "%s"},\n' % version
        text += '\t' * 6 + '"checkbox": true\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('version', text)


def update_platform_example_menu(arduino_info):
    """."""
    example_paths = []
    library_paths = []
    platform_path = selected.get_sel_platform_path(arduino_info)
    if platform_path:
        examples_path = os.path.join(platform_path, 'examples')
        example_paths = glob.glob(examples_path + '/*')
        example_paths = [p for p in example_paths if os.path.isdir(p)]

        libraries_path = os.path.join(platform_path, 'libraries')
        library_paths = glob.glob(libraries_path + '/*')
        library_paths = [p for p in library_paths if os.path.isdir(p)]

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Open Platform Example",\n'
    text += '\t' * 4 + '"id": "stino_platform_examples",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_platform_examples",\n'
    text += '\t' * 6 + '"command": "stino_refresh_platform_examples"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'
    text += get_example_menu_text(5, example_paths)
    text += ',' + '\t' * 5 + '{"caption": "-"}'
    text += get_example_menu_text(5, library_paths)
    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('platform_examples', text)


def update_platform_library_menu(arduino_info):
    """."""
    library_paths = []
    platform_path = selected.get_sel_platform_path(arduino_info)
    if platform_path:
        libraries_path = os.path.join(platform_path, 'libraries')
        library_paths = glob.glob(libraries_path + '/*')
        library_paths = [p for p in library_paths if os.path.isdir(p)]

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Import Platform Library",\n'
    text += '\t' * 4 + '"id": "stino_import_platform_library",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_platform_libraries",\n'
    text += '\t' * 6 + '"command": "stino_refresh_platform_libraries"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for library_path in library_paths:
        library_path = library_path.replace('\\', '/')
        library_name = os.path.basename(library_path)
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % library_name
        text += '\t' * 6 + '"id": "stino_library_%s",\n' % library_name
        text += '\t' * 6 + '"command": "stino_import_library",\n'
        text += '\t' * 6 + '"args": {"library_path": "%s"}\n' % library_path
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('platform_libraries', text)


def update_board_menu(arduino_info):
    """."""
    board_names = arduino_info['boards'].get('names', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Board",\n'
    text += '\t' * 4 + '"id": "stino_board",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_boards",\n'
    text += '\t' * 6 + '"command": "stino_refresh_boards"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for board_name in board_names:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % board_name
        text += '\t' * 6 + '"id": "stino_board_%s",\n' % board_name
        text += '\t' * 6 + '"command": "stino_select_board",\n'
        text += '\t' * 6 + '"args": {"board_name": "%s"},\n' % board_name
        text += '\t' * 6 + '"checkbox": true\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('board', text)


def update_board_options_menu(arduino_info):
    """."""
    sel_board = arduino_info['selected'].get('board')
    board_info = arduino_info['boards'].get(sel_board, {})
    options = board_info.get('options', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Board Options",\n'
    text += '\t' * 4 + '"id": "board_options",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_board_options",\n'
    text += '\t' * 6 + '"command": "stino_refresh_board_options"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for option in options:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % option
        text += '\t' * 6 + '"id": "stino_board_%s",\n' % option
        text += '\t' * 6 + '"children":\n'
        text += '\t' * 6 + '[\n'
        text += '\t' * 7 + '{"caption": "-"}'

        items_info = board_info.get(option, {})
        names = items_info.get('names', [])
        for name in names:
            text += ',\n'
            text += '\t' * 7 + '{\n'
            text += '\t' * 8 + '"caption": "%s",\n' % name
            text += '\t' * 8 + '"id": "stino_board_option_%s",\n' % name
            text += '\t' * 8 + '"command": "stino_select_board_option",\n'

            arg_text = '"args": {"option": "%s", ' % option
            arg_text += '"value": "%s"},\n' % name
            text += '\t' * 8 + arg_text
            text += '\t' * 8 + '"checkbox": true\n'
            text += '\t' * 7 + '}'

        text += '\n' + '\t' * 6 + ']\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('board_options', text)


def update_programmer_menu(arduino_info):
    """."""
    programmer_names = arduino_info['programmers'].get('names', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Programmer",\n'
    text += '\t' * 4 + '"id": "stino_programmer",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_programmers",\n'
    text += '\t' * 6 + '"command": "stino_refresh_programmers"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for programmer_name in programmer_names:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % programmer_name
        text += '\t' * 6 + '"id": "stino_programmer_%s",\n' % programmer_name
        text += '\t' * 6 + '"command": "stino_select_programmer",\n'
        text += '\t' * 6
        text += '"args": {"programmer_name": "%s"},\n' % programmer_name
        text += '\t' * 6 + '"checkbox": true\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('programmer', text)


def update_serial_menu(arduino_info):
    """."""
    serial_ports_info = arduino_info.get('serial_ports', {})
    serial_ports = serial_ports_info.get('names', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Serial Port",\n'
    text += '\t' * 4 + '"id": "serial_port",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_serials",\n'
    text += '\t' * 6 + '"command": "stino_refresh_serials"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for serial_port in serial_ports:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % serial_port
        text += '\t' * 6 + '"id": "stino_serial_%s",\n' % serial_port
        text += '\t' * 6 + '"command": "stino_select_serial",\n'
        text += '\t' * 6
        text += '"args": {"serial_port": "%s"},\n' % serial_port
        text += '\t' * 6 + '"checkbox": true\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('serial', text)


def update_language_menu(arduino_info):
    """."""
    languages_info = arduino_info.get('languages', {})
    languages = languages_info.get('names', [])

    text = '\t' * 0 + '[\n'
    text += '\t' * 1 + '{\n'
    text += '\t' * 2 + '"caption": "Arduino",\n'
    text += '\t' * 2 + '"mnemonic": "A",\n'
    text += '\t' * 2 + '"id": "arduino",\n'
    text += '\t' * 2 + '"children":\n'
    text += '\t' * 2 + '[\n'
    text += '\t' * 3 + '{\n'
    text += '\t' * 4 + '"caption": "Language",\n'
    text += '\t' * 4 + '"id": "stino_language",\n'
    text += '\t' * 4 + '"children":\n'
    text += '\t' * 4 + '[\n'
    text += '\t' * 5 + '{\n'
    text += '\t' * 6 + '"caption": "Refresh",\n'
    text += '\t' * 6 + '"id": "stino_refresh_languages",\n'
    text += '\t' * 6 + '"command": "stino_refresh_languages"\n'
    text += '\t' * 5 + '},\n'
    text += '\t' * 5 + '{"caption": "-"}'

    for language in languages:
        text += ',\n'
        text += '\t' * 5 + '{\n'
        text += '\t' * 6 + '"caption": "%s",\n' % language
        text += '\t' * 6 + '"id": "stino_language_%s",\n' % language
        text += '\t' * 6 + '"command": "stino_select_language",\n'
        text += '\t' * 6
        text += '"args": {"language": "%s"},\n' % language
        text += '\t' * 6 + '"checkbox": true\n'
        text += '\t' * 5 + '}'

    text += '\n' + '\t' * 4 + ']\n'
    text += '\t' * 3 + '}\n'
    text += '\t' * 2 + ']\n'
    text += '\t' * 1 + '}\n'
    text += '\t' * 0 + ']\n'

    write_menu('language', text)
