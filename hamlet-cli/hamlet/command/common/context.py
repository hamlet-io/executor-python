import click
import functools


class Generation():
    '''Standard Generation context'''
    def __init__(self, generation_provider=None, generation_framework=None, generation_input_source=None):
        self.generation_provider = generation_provider
        self.generation_framework = generation_framework
        self.generation_input_source = generation_input_source


pass_generation = click.make_pass_decorator(Generation, ensure=True)


def generation_config(func):
    @functools.wraps(func)
    @click.option(
        '-p',
        '--generation-provider',
        help='plugins to load for output generation',
        default=['aws'],
        multiple=True,
        show_default=True
    )
    @click.option(
        '-f',
        '--generation-framework',
        help='output framework to use for output generation',
        default='cf',
        show_default=True
    )
    @click.option(
        '-i',
        '--generation-input-source',
        help='source of input data to use when generating the output',
        default='composite',
        show_default=True
    )
    @click.pass_context
    def decorator(ctx, generation_provider, generation_framework, generation_input_source, *args, **kwargs):
        ctx.obj = Generation(
            generation_provider=(
                generation_provider if generation_provider else ctx.obj.generation_provider
            ),
            generation_framework=(
                generation_framework if generation_framework else ctx.obj.generation_framework
            ),
            generation_input_source=(
                generation_input_source if generation_input_source else ctx.obj.generation_input_source
            ),
        )
        return func(*args, **kwargs)
    return decorator
