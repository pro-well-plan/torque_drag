import plotly.graph_objects as go


def tnd(tq_n_dg, plot_case='Force'):

    if plot_case == 'Force':
        fig = plot_sequence(tq_n_dg.force, tq_n_dg.depth, case='Force')

    else:
        fig = plot_sequence(tq_n_dg.torque, tq_n_dg.depth, case='Torque')

    return fig


def plot_sequence(data, depth, case='Force'):

    if case == 'Force':
        case_units = 'kN'
    else:
        case_units = 'kN*m'

    fig = go.Figure()

    values = []
    if len(data["lowering"]) > 0:
        fig.add_trace(go.Scatter(x=data["lowering"], y=depth,
                                 mode='lines',
                                 name='Lowering'))
        values += [min(data["lowering"]), max(data["lowering"])]
    if len(data["static"]) > 0:
        fig.add_trace(go.Scatter(x=data["static"], y=depth,
                                 mode='lines',
                                 name='Static'))
        values += [min(data["static"]), max(data["static"])]
    if len(data["hoisting"]) > 0:
        fig.add_trace(go.Scatter(x=data["hoisting"], y=depth,
                                 mode='lines',
                                 name='Hoisting'))
        values += [min(data["hoisting"]), max(data["hoisting"])]
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
                      xaxis_title=case + ', ' + case_units,
                      yaxis_title='Depth, m')

    return fig
