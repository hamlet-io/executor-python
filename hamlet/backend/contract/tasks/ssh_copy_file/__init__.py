import io
from fabric import Connection
from paramiko import RSAKey
from invoke.exceptions import UnexpectedExit
from socket import timeout as socket_timeout

from hamlet.backend.contract.tasks.exceptions import TaskFailureException


def get_connect_args(password, ssh_key):
    connect_kwargs = {"allow_agent": False, "look_for_keys": False}

    if password is not None:
        connect_kwargs["password"] = password

    if ssh_key is not None:

        if isinstance(ssh_key, str):
            private_key = RSAKey.from_private_key(io.StringIO(ssh_key))
        else:
            private_key = RSAKey.from_private_key(ssh_key)

        connect_kwargs["pkey"] = private_key

    return connect_kwargs


def run(
    Host,
    Port,
    Username,
    Password=None,
    SSHKey=None,
    Direction=None,
    RemotePath=None,
    LocalPath=None,
    BastionHost=None,
    BastionPort=None,
    BastionUsername=None,
    BastionPassword=None,
    BastionSSHKey=None,
    env={},
):
    """
    Copy a file betwen a remote host and local host over ssh
    """

    gateway_connection = None

    if BastionHost is not None:
        gateway_connection = Connection(
            host=BastionHost,
            port=BastionPort,
            user=BastionUsername,
            connect_kwargs=get_connect_args(BastionPassword, BastionSSHKey),
            connect_timeout=10,
        )

    with Connection(
        host=Host,
        user=Username,
        port=Port,
        connect_kwargs=get_connect_args(Password, SSHKey),
        connect_timeout=10,
        gateway=gateway_connection,
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
