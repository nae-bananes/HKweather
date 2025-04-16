import plotly.express as px
from itertools import cycle
import plotly.graph_objects as go
import plotly.io as pio

def plot_forecast(pred_df, forecast_columns, timestamp_col, forecast_display_names=None):
    
    if forecast_display_names is None:
        forecast_display_names = forecast_columns
    else:
        assert len(forecast_columns) == len(forecast_display_names)
    
    mask = ~pred_df[forecast_columns[0]].isnull()
    colors = [c.replace("rgb", "rgba").replace(")", ", <alpha>)") for c in px.colors.qualitative.Dark2]
    act_color = colors[0]
    colors = cycle(colors[1:])
    dash_types = cycle(["dash", "dot", "dashdot"])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pred_df[mask][timestamp_col], y=pred_df[mask]['y'],
                             mode='lines', line=dict(color=act_color.replace("<alpha>", "0.3")),
                             name='Observed value (Y)'))
    
    for col, display_col in zip(forecast_columns, forecast_display_names):
        fig.add_trace(go.Scatter(x=pred_df[mask][timestamp_col], y=pred_df.loc[mask, col],
                                 mode='lines', line=dict(dash=next(dash_types), color=next(colors).replace("<alpha>", "1")),
                                 name=display_col))
    return fig

def format_plot(fig, legends = None, xlabel="Time", ylabel="Value", title="", font_size=15):
    if legends:
        names = cycle(legends)
        fig.for_each_trace(lambda t:  t.update(name = next(names)))
    fig.update_layout(
            autosize=False,
            width=900,
            height=500,
            title_text=title,
            title={
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
          #  titlefont={
          #      "size": 20
          #  },
            legend_title = None,
            legend=dict(
                font=dict(size=font_size),
                orientation="h",
                yanchor="bottom",
                y=0.98,
                xanchor="right",
                x=1,
            ),
            yaxis=dict(
                title_text=ylabel,
                #titlefont=dict(size=font_size),
                tickfont=dict(size=font_size),
            ),
            xaxis=dict(
                title_text=xlabel,
                #titlefont=dict(size=font_size),
                tickfont=dict(size=font_size),
            )
        )
    return fig