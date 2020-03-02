from pysystem import commands
import pysystem.exceptions
import traceback


class Terminal:
    def __init__(self, system):
        self.system = system
        self.current_folder = system.root_folder
        self.input_history = []
        self.terminal_commands = {
            'exit': None,
            'history': None,
            'cat': commands.cat,
            'touch': commands.touch,
            'mkdir': commands.mkdir,
            'cd': commands.cd,
            'ls': commands.ls,
            'echo': commands.echo,
            'rm': commands.rm,
            'del': commands.rm,
            'tree': commands.tree,
            'clear': commands.clear
        }

    def interpret(self):
        while True:
            terminal_input = input(self.current_folder.get_path() + '> ')
            for terminal_command in terminal_input.split('&'):
                terminal_command = terminal_command.strip().split(' ')
                self.input_history.append(terminal_input)
                if terminal_command[0] == 'exit':
                    print('Exiting...')
                    return
                elif terminal_command[0] == 'help':
                    print('Available commands:\n\t' + '\n\t'.join(self.terminal_commands.keys()))
                elif terminal_command[0] == 'history':
                    print('Input history:\n\t' + '\n\t'.join(self.input_history))
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
                    print("'{}' is not recognized as an internal or external command.".format(terminal_command[0]))


def interpret(system):
    terminal = Terminal(system)
    terminal.interpret()
