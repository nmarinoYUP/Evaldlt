import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import inspect
    import functools
    from typing import Any, get_args

    import marimo as mo

    from dlt.sources.rest_api import RESTAPIConfig, config_setup 
    from dlt.sources.rest_api.typing import Endpoint, ClientConfig
    from dlt.sources.helpers.rest_client.typing import HTTPMethodBasic, HTTPMethodExtended
    return Any, ClientConfig, config_setup, get_args, inspect, mo


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


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Client""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Base url""")
    return


@app.cell
def _(mo):
    text_base_url = mo.ui.text(label="base_url")
    text_base_url
    return (text_base_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Headers""")
    return


@app.cell
def _():
    headers = {}
    return (headers,)


@app.cell
def _(headers, headers_form):
    try:
        _key = headers_form.value.get("key")
        _value = headers_form.value.get("value")
    except AttributeError:
        _key = None
        _value = None

    if _key is not None and _value is not None:
        headers[_key] = _value
    return


@app.cell
def _(mo):
    _key, _value = "", ""
    _text_key = mo.ui.text(label="key", value=_key)
    _text_value = mo.ui.text(label="value", value=_value)

    headers_form = (
        mo.md("{key}: {value}")
        .batch(key=_text_key, value=_text_value)
        .form(
            submit_button_label="Add",
            clear_on_submit=True
        )
    )
    headers_form
    return (headers_form,)


@app.cell
def _(headers, headers_form, mo):
    headers_form
    headers_table = None
    if headers:
        headers_table = mo.ui.table(
            headers,
            selection="single"
        )

    headers_table
    return (headers_table,)


@app.cell
def _(headers_table):
    _key, _value = "", ""
    if getattr(headers_table, "value", None):
        _selected_header = headers_table.value[0]
        _key, _value = _selected_header["key"], _selected_header["value"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Auth""")
    return


@app.cell
def _(config_setup, mo):
    def auth_form():
        select_auth = mo.ui.dropdown(
            options=config_setup.AUTH_MAP,
            label="Method",
            value="bearer",
        )
        return select_auth
    return (auth_form,)


@app.cell
def _(auth_form):
    main_auth_method = auth_form()
    main_auth_method
    return (main_auth_method,)


@app.cell
def _(generate_components, main_auth_method, mo):
    _components = generate_components(main_auth_method.value)

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
    return (auth_config,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Paginator""")
    return


@app.cell(hide_code=True)
def _(config_setup, mo):
    _excluded_paginators = ["auto", "json_response"]
    _paginator_options = {k:v for k,v in config_setup.PAGINATOR_MAP.items() if k not in _excluded_paginators}

    select_paginator = mo.ui.dropdown(
        options=_paginator_options,
        label="Method",
        value="single_page",
    )
    select_paginator
    return (select_paginator,)


@app.cell
def _(generate_components, mo, select_paginator):
    _components = generate_components(select_paginator.value)

    dict_paginator_config = None
    if _components:
        dict_paginator_config = mo.ui.dictionary(_components)

    dict_paginator_config
    return (dict_paginator_config,)


@app.cell
def _(dict_paginator_config):
    if getattr(dict_paginator_config, "value", None):
        paginator_config = dict_paginator_config.value
    else:
        paginator_config = None
    return (paginator_config,)


@app.cell
def _(ClientConfig, auth_config, headers, paginator_config, text_base_url):
    client_config = ClientConfig(
        base_url=text_base_url.value,
        headers=headers,
        auth=auth_config,
        paginator=paginator_config,
    )
    return


if __name__ == "__main__":
    app.run()
