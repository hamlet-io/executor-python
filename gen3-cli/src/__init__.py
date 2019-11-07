# Here we controll modules loading order
# We can do it in command.__init__ but I guess this is a little bit more explicit
import src.command  # noqa
import src.command.create  # noqa
import src.command.add  # noqa
import src.command.manage  # noqa
import src.command.run  # noqa
