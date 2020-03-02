import pysystem.exceptions
import pysystem.file


def get_file_at_path(root_folder, current_folder, target_path):
    new_target_folder = current_folder
    target_path = target_path.split('/')
    if len(target_path) == 1 and target_path[0] == '':
        return current_folder
    if target_path[0] == '':
        new_target_folder = root_folder
    for target_path_step in target_path:
        if type(new_target_folder) is not pysystem.file.Folder:
            raise pysystem.exceptions.InvalidDirectoryName()
        if target_path in ['.', '']:
            pass
        elif target_path_step == '..':
            if new_target_folder.parent is not None:
                new_target_folder = new_target_folder.parent
        else:
            target_folder = new_target_folder.get_sub_file(target_path_step)
            if target_folder is None:
                raise pysystem.exceptions.InvalidPathException()
            new_target_folder = target_folder
    return new_target_folder


def cat(system, terminal, *args):
    if len(args) < 2:
        raise pysystem.exceptions.InvalidCommandSyntaxException()
    target_file = get_file_at_path(system.root_folder, terminal.current_folder, args[1])
    try:
        return target_file.cat()
    except pysystem.exceptions.InvalidDirectoryOperationException:
        raise pysystem.exceptions.PySystemException("cat: '{}': Is a directory".format(target_file.name))


def _touch(system, terminal, target_path):
    location = get_file_at_path(system.root_folder, terminal.current_folder, '/'.join(target_path.split('/')[:-1]))
    new_file = pysystem.file.File(target_path.split('/')[-1])
    location.add_child(new_file)


def touch(system, terminal, *args):
    if len(args) < 2:
        raise pysystem.exceptions.InvalidCommandSyntaxException()
    _touch(system, terminal, args[1])
    return ""


def _mkdir(system, terminal, target_path):
    location = get_file_at_path(system.root_folder, terminal.current_folder, '/'.join(target_path.split('/')[:-1]))
    new_folder = pysystem.file.Folder(target_path.split('/')[-1])
    location.add_child(new_folder)


def mkdir(system, terminal, *args):
    if len(args) < 2:
        raise pysystem.exceptions.InvalidCommandSyntaxException()
    _mkdir(system, terminal, args[1])
    return ""


def cd(system, terminal, *args):
    if len(args) < 2:
        raise pysystem.exceptions.InvalidCommandSyntaxException()
    terminal.current_folder = get_file_at_path(system.root_folder, terminal.current_folder, args[1])
    return ""


def ls(system, terminal, *args):
    output = ''
    for file in terminal.current_folder.child_files.values():
        output += file.get_path(terminal.current_folder) + '\n'
    return output.strip()


def echo(system, terminal, *args):
    if '>' in args:
        echo_message = ' '.join(args[1:args.index('>')])
        if len(args) <= args.index('>') + 1 or len(args) > args.index('>') + 2:
            raise pysystem.exceptions.InvalidCommandSyntaxException()
        try:
            target_file = get_file_at_path(system.root_folder, terminal.current_folder, args[-1])
        except pysystem.exceptions.PySystemException:
            _touch(system, terminal, args[-1])
            target_file = get_file_at_path(system.root_folder, terminal.current_folder, args[-1])
        if type(target_file) is pysystem.file.File:
            target_file.contents = echo_message
    else:
        return ' '.join(args[1:])
    return ''


def rm(system, terminal, *args):
    if len(args) < 2:
        raise pysystem.exceptions.InvalidCommandSyntaxException()
    target_file = get_file_at_path(system.root_folder, terminal.current_folder, args[1])
    target_file.parent.remove_child(target_file)

def mv(system, terminal, *args):
    new_name = args[2].split('/')[-1]
    source_file = get_file_at_path(system.root_folder, terminal.current_folder, args[1])
    target_folder = get_file_at_path(system.root_folder, terminal.current_folder, '/'.join(args[2].split('/')[:-1]))
    source_file.parent.remove_child(source_file)
    target_folder.add_child(source_file)
    source_file.name = new_name
    return ''


def tree(system, terminal, *args):
    return terminal.current_folder.get_tree_structure()
