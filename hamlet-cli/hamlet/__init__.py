# Here we controll modules loading order
# We can do it in command.__init__ but I guess this is a little bit more explicit
import hamlet.command  # noqa
import hamlet.command.generate  # noqa
import hamlet.command.entrance  # noqa
import hamlet.command.engine  # noqa
import hamlet.command.test  # noqa
import hamlet.command.manage  # noqa
import hamlet.command.run  # noqa
import hamlet.command.query  # noqa
import hamlet.command.visual  # noqa
import hamlet.command.deploy  # noqa
import hamlet.command.schema  # noqa
import hamlet.command.setup  # noqa
import hamlet.command.component # noqa
