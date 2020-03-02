import pysystem.file
import pysystem.terminal
import pickle


class System:
    def __init__(self, system_name):
        self.system_file_name = system_name + '.pysy'
        self.root_folder = pysystem.file.Folder("py:")

    def run(self):
        pysystem.terminal.interpret(self)

    def save(self):
        with open(self.system_file_name, 'wb') as system_file:
            pickle.dump(self.root_folder, system_file)

    def load(self):
        with open(self.system_file_name, 'rb') as system_file:
            self.root_folder = pickle.load(system_file)
