import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import mowidgets

    from dlt.helpers.marimo._widgets._rest_api_builder.client import app
    return app, mowidgets


@app.cell
async def _(app, mowidgets):
    client_widget = mowidgets.widgetize(app, data_access=True)
    await client_widget
    return (client_widget,)


@app.cell
def _(client_widget):
    client_widget.data["client_config"]
    return


if __name__ == "__main__":
    app.run()
