import io
from fabric import Connection
from paramiko import RSAKey
from invoke.exceptions import UnexpectedExit
from socket import timeout as socket_timeout

from hamlet.backend.contract.tasks.exceptions import TaskFailureException


def run(Host, Port, Username, Password=None, SSHKey=None, Command=None, env={}):
    """
    Run a command on a remote ssh host with an interactive shell
    """

    connect_kwargs = {"allow_agent": False, "look_for_keys": False}

    if Password is not None:
        connect_kwargs["password"] = Password

    if SSHKey is not None:

        if isinstance(SSHKey, str):
            private_key = RSAKey.from_private_key(io.StringIO(SSHKey))
        else:
            private_key = RSAKey.from_private_key(SSHKey)

        connect_kwargs["pkey"] = private_key

    print(f"\n---- SSH Session | host: {Host} | user: {Username} ----\n")

    with Connection(
        host=Host,
        user=Username,
        port=Port,
        connect_kwargs=connect_kwargs,
        connect_timeout=10,
    ) as ssh_con:
        try:
            ssh_con.run(Command, pty=True)
        except socket_timeout as e:
            raise TaskFailureException(str(e))
        except UnexpectedExit:
            pass

    print("\n---- SSH Session Complete ----\n")

    return {}
