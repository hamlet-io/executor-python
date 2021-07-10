from hamlet.command import root


@root.group("query", context_settings=dict(max_content_width=240), deprecated=True)
def query_group():
    """
    Base command used to set blueprint generation options

    DEPRECATED: the query command group has been replaced by the component group ( hamlet component )

        run hamlet component --help for the new commands
    """
    pass
