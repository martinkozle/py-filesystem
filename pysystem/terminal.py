from pysystem import commands
import pysystem.exceptions
import traceback


class Terminal:
    def __init__(self, system):
        self.system = system
        self.current_folder = system.root_folder
        self.terminal_commands = {
            'exit': None,
            'cat': commands.cat,
            'touch': commands.touch,
            'mkdir': commands.mkdir,
            'cd': commands.cd,
            'ls': commands.ls,
            'echo': commands.echo,
            'rm': commands.rm,
            'del': commands.rm
        }

    def interpret(self):
        while True:
            terminal_input = input(self.current_folder.get_path() + '> ').split('&')
            for terminal_command in terminal_input:
                terminal_command = terminal_command.strip().split(' ')
                if terminal_command[0] == 'exit':
                    print('Exiting...')
                    return
                if terminal_command[0] == 'help':
                    print('Available commands:\n\t' + '\n\t'.join(self.terminal_commands.keys()))
                elif terminal_command[0] in self.terminal_commands:
                    try:
                        print(self.terminal_commands[terminal_command[0]](self.system, self, *terminal_command))
                    except pysystem.exceptions.PySystemException as err:
                        print(err)
                        break
                    except Exception as err:
                        print('Fatal error: {}'.format(err))
                        print(traceback.format_exc())
                        break
                else:
                    print("'{}' is not recognized as an internal or external command.".format(terminal_input[0]))


def interpret(system):
    terminal = Terminal(system)
    terminal.interpret()
