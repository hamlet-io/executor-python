import os

from hamlet.backend import query as query_backend

GET_PROPERTIES_ENVIRONMENT_QUERY = "Environment"


def get_automation_properties(engine=None, **kwargs):

    query_args = {
        **kwargs,
        "generation_entrance": "releaseinfo",
        "output_filename": "releaseinfo-config.json",
        "output_format": "default",
    }
    automation_properties = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=GET_PROPERTIES_ENVIRONMENT_QUERY,
        engine=engine
    )

    return automation_properties
