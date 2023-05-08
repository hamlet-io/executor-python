import click
import os
import subprocess
from shutil import copyfile

from hamlet.command import root as cli


def regenerate_autocompletion_files(shell_type: str, autocomplete_path: str) -> None:
    subprocess.check_call(
        f"_HAMLET_COMPLETE={shell_type}_source hamlet > {autocomplete_path}",
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    print(f"Regenerated {shell_type} completion file: {autocomplete_path}")


def autocomplete_fish(user_home_path: str, autocomplete_path: str) -> None:
    destination_path = os.path.join(
        user_home_path, ".config/fish/completions/hamlet.fish"
    )

    if os.path.isfile(destination_path):
        print("Autocompletion was previously set up. Skipping.")

    else:
        copyfile(
            autocomplete_path,
            destination_path,
        )


def autocomplete_bash_or_zsh(
    user_home_path: str, autocomplete_path: str, shell_type: str = "bash"
) -> None:
    autocomplete_path = autocomplete_path.replace(user_home_path, "~")

    autocompletion_string = f"# HAMLET-AUTOCOMPLETE\n. {autocomplete_path}"
    run_command_path = os.path.join(user_home_path, f".{shell_type}rc")

    with open(run_command_path, "r") as OH:
        if autocompletion_string in OH.readlines():
            print("Autocompletion was previously set up. Skipping.")

        else:
            with open(run_command_path, "a+") as OH:
                OH.write(f"\n{autocompletion_string}")


@cli.command()
@click.argument(
    "shell-type",
    type=click.Choice(["bash", "zsh", "fish"], case_sensitive=False),
    default="bash",
)
@click.option(
    "--regenerate",
    help="regenerates the autocompletion file",
    type=click.BOOL,
    default=False,
    is_flag=True,
)
def autocomplete(shell_type: str, regenerate: bool) -> None:
    """
    Enable autocomplete for the cli
    """
    user_home_path = os.path.expanduser("~")
    autocomplete_path = os.path.join(
        __path__[0], "scripts", f".hamlet-complete.{shell_type}"
    )

    if regenerate:
        regenerate_autocompletion_files(shell_type, autocomplete_path)

    if shell_type in ("bash", "zsh"):
        autocomplete_bash_or_zsh(user_home_path, autocomplete_path, shell_type)
    elif "fish" == shell_type:
        autocomplete_fish(user_home_path, autocomplete_path)

    click.secho(
        f"Autocomplete setup for {shell_type} open a new shell to complete the process",
        color="green",
    )
