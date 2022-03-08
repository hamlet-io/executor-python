import os
from hamlet.backend import query as query_backend


class DescribeContext:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


def query_occurrences_state(
    options, engine, query, query_params=None, sub_query_text=None
):
    query_args = {
        **options.opts,
        "generation_entrance": "occurrences",
        "output_filename": "occurrences-state.json",
        "use_cache": False,
    }
    query_result = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=query,
        query_params=query_params,
        sub_query_text=sub_query_text,
        engine=engine
    )

    return query_result
