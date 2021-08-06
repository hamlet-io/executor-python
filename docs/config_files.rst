CLI Config Files
==================

The hamlet cli config files provide a way to configure your hamlet workspace.

The files are based on the ini file syntax and are broken up into sections which define the type of configuration, each type then has an instance of this configuration section that you can reference in the cli

So to define profiles which set the common hamlet district properties you would add the following section

.. code-block:: ini

    [profile:my_profile]
        account = acct1
        tenant = tenant1
        product = product1

Then in the cli can reference the profile with `hamlet --profile my_profile`

config
-----------

The config file is the default configuration file to use when configuring hamlet and is used in most circumstances. It configures how you interact with your deployments and provides shortcuts to remove some of the required hamlet cli parameters

The following sections are supported in the config file

 .. autoclass:: hamlet.command.common.config.ConfigSchema
    :members:

engine
-----------

The engine configuration file

.. autoclass:: hamlet.backend.engine.loaders.user.EngineSchema
    :members:
