from octopus.server.orientdb.orientdb_server_command import OrientDBServerCommand
from octopus.server.shell_manager import ShellManager


class OrientDBShellManager(ShellManager):
    def __init__(self, server_host, server_port):
        self.command = OrientDBServerCommand(server_host, server_port)

    def create(self, project_name):
        response = self.command.execute_get_command("/manageshells/create/{}".format(project_name))
        port = int(response)
        return port

    def list(self, project_name=None, shell_port=None):
        response = self.command.execute_get_command("/manageshells/list")
        if not response:
            return
        for shell in response.split('\n'):
            port, dbName, name, occupied = shell.split('\t')
            port = int(port)
            if (not project_name or name == project_name) and (not shell_port or port == shell_port):
                yield port, dbName, name, ('occupied' if occupied == 'true' else 'free')
