import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import inspect
    import functools
    from typing import Any, get_args

    import marimo as mo

    from dlt.sources.rest_api import RESTAPIConfig, config_setup 
    from dlt.sources.rest_api.typing import Endpoint
    from dlt.sources.helpers.rest_client.typing import HTTPMethodBasic, HTTPMethodExtended
    return (
        Any,
        HTTPMethodBasic,
        HTTPMethodExtended,
        config_setup,
        get_args,
        inspect,
        mo,
    )


@app.cell
def _(Any, get_args, inspect, mo):
    def generate_component(key: str, type_: type | str, default: Any | None = None):
        default = None if default == inspect._empty else default
        # print(key, type_, default)
        try:
            for type_arg in get_args(type_):
                if type_arg is None:
                    continue
                return generate_component(key, type_arg, default=default)
        except Exception:
            pass

        # get_args() over a Literal will return objects instead of classes
        if isinstance(type_, str):
            return mo.ui.text(value=default if default else "")

        if issubclass(type_, str):
            return mo.ui.text(value=default if default else "")
        # NOTE remember that `issubclass(True, int) is True`
        elif issubclass(type_, int):
            if type_ is bool:
                return mo.ui.checkbox(value=default)

            return mo.ui.number(value=default)

        return mo.ui.button()
    return (generate_component,)


@app.cell
def _(inspect):
    def inspect_init_signature(class_: type) -> dict:
        sig = inspect.signature(class_.__init__)
        args = {k:v for k,v in sig.parameters.items() if k != "self"}
        return args
    return (inspect_init_signature,)


@app.cell
def _(generate_component, inspect_init_signature):
    def generate_components(class_: type) -> dict:
        components = {}
        if isinstance(class_, dict):
            for name, type_ in class_.items():
                components[name] = generate_component(name, type_)
        else:
            for name, value in inspect_init_signature(class_).items():
                component = generate_component(key=name, type_=value.annotation, default=value.default)
                components[name] = component
        return components
    return (generate_components,)


@app.cell
def _(config_setup, mo):
    # reuse from client.py
    def auth_form():
        select_auth = mo.ui.dropdown(
            options=config_setup.AUTH_MAP,
            label="Method",
            value="bearer",
        )
        return select_auth
    return (auth_form,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Path""")
    return


@app.cell
def _(mo):
    text_path = mo.ui.text(label="path")
    text_path
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Method""")
    return


@app.cell
def _(HTTPMethodBasic, HTTPMethodExtended, get_args, mo):
    _http_methods = [*get_args(HTTPMethodBasic), *get_args(HTTPMethodExtended)]

    select_http_method = mo.ui.dropdown(
        options=_http_methods,
        value=_http_methods[0],
        label="HTTP Method",
    )
    select_http_method
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Data selector""")
    return


@app.cell
def _(mo):
    text_data_selector = mo.ui.text(label="data selector")
    text_data_selector
    return (text_data_selector,)


@app.cell
def _(text_data_selector):
    data_selector = text_data_selector.value
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Incremental""")
    return


@app.cell
def _(mo):
    incremental_start = mo.ui.text(label="start")
    incremental_end = mo.ui.text(label="end")

    mo.vstack([incremental_start, incremental_end])
    return incremental_end, incremental_start


@app.cell
def _(incremental_end, incremental_start):
    incremental_config = {
        "start_param": incremental_start.value,
        "end_param": incremental_end.value,
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Auth""")
    return


@app.cell
def _(auth_form):
    endpoint_auth_method = auth_form()
    endpoint_auth_method
    return (endpoint_auth_method,)


@app.cell
def _(endpoint_auth_method, generate_components, mo):
    _components = generate_components(endpoint_auth_method.value)

    dict_auth_config = None
    if _components:
        dict_auth_config = mo.ui.dictionary(_components)

    dict_auth_config
    return (dict_auth_config,)


@app.cell
def _(dict_auth_config):
    auth_config = {}
    if getattr(dict_auth_config, "value", None):
        auth_config = dict_auth_config.value
    return


if __name__ == "__main__":
    app.run()
