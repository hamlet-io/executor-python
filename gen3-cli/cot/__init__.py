# Here we controll modules loading order
# We can do it in command.__init__ but I guess this is a little bit more explicit
import cot.command  # noqa
import cot.command.generate
import cot.command.create  # noqa
# import cot.command.add  # noqa
import cot.command.manage  # noqa
import cot.command.run  # noqa
