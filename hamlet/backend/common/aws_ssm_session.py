import json
import contextlib
import sys
import signal
import boto3
import errno
from subprocess import check_call


@contextlib.contextmanager
def ignore_user_entered_signals():
    """
    Ignores user entered signals to avoid process getting killed.
    """
    if sys.platform == "win32":
        signal_list = [signal.SIGINT]
    else:
        signal_list = [signal.SIGINT, signal.SIGQUIT, signal.SIGTSTP]
    actual_signals = []
    for user_signal in signal_list:
        actual_signals.append(signal.signal(user_signal, signal.SIG_IGN))
    try:
        yield
    finally:
        for sig, user_signal in enumerate(signal_list):
            signal.signal(user_signal, actual_signals[sig])


def invoke(
    session_id,
    stream_url,
    token_value,
    parameters,
    aws_access_key_id,
    aws_secret_access_key,
    aws_session_token,
    region_name,
    auth_profile_name="",
):
    """
    Invokes an SSM interactice session using session details
    that have been created in another process
    """

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )
    ssm = session.client("ssm")
    endpoint_url = ssm.meta.endpoint_url

    ssm_session = {
        "SessionId": session_id,
        "StreamUrl": stream_url,
        "TokenValue": token_value,
    }

    try:
        # ignore_user_entered_signals ignores these signals
        # because if signals which kills the process are not
        # captured would kill the foreground process but not the
        # background one. Capturing these would prevents process
        # from getting killed and these signals are input to plugin
        # and handling in there

        with ignore_user_entered_signals():
            # call executable with necessary input
            check_call(
                [
                    "session-manager-plugin",
                    json.dumps(ssm_session),
                    region_name,
                    "StartSession",
                    auth_profile_name,
                    json.dumps(parameters),
                    endpoint_url,
                ]
            )
        return 0

    except OSError as ex:
        if ex.errno == errno.ENOENT:
            # start-session api call returns response and starts the
            # session on ssm-agent and response is forwarded to
            # session-manager-plugin. If plugin is not present, terminate
            # is called so that service and ssm-agent terminates the
            # session to avoid zombie session active on ssm-agent for
            # default self terminate time
            ssm.terminate_session(SessionId=session_id)
            raise ValueError(
                (
                    "AWS Session manager plugin could not be found: "
                    "see https://docs.aws.amazon.com/systems-manager/"
                    "latest/userguide/session-manager-working-with-install-plugin.html"
                )
            )
