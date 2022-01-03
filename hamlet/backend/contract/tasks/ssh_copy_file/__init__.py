import io
from fabric import Connection
from paramiko import RSAKey
from invoke.exceptions import UnexpectedExit
from socket import timeout as socket_timeout

from hamlet.backend.contract.tasks.exceptions import TaskFailureException


def run(
    Host,
    Port,
    Username,
    Password=None,
    SSHKey=None,
    Direction=None,
    RemotePath=None,
    LocalPath=None,
    env={},
):
    """
    Copy a file betwen a remote host and local host over ssh
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

    with Connection(
        host=Host,
        user=Username,
        port=Port,
        connect_kwargs=connect_kwargs,
        connect_timeout=10,
    ) as ssh_con:

        try:
            if Direction == "LocalToRemote":
                ssh_con.put(LocalPath, RemotePath)
                print(f"\n{LocalPath} -> ssh://{Host}:{RemotePath}\n")

            if Direction == "RemoteToLocal":
                ssh_con.get(RemotePath, LocalPath)
                print(f"\nssh://{Host}:{RemotePath} -> {LocalPath}\n")

        except socket_timeout as e:
            raise TaskFailureException(str(e))
        except UnexpectedExit:
            pass

    return {}
