import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "simple_white"


def assign_color(row):
    if row == 'face':
        return 'red'
    elif 'hand' in row:
        return 'dodgerblue'
    else:
        return 'green'


def assign_order(row):
    if row.type == 'face':
        return row.landmark_index + 101
    elif row.type == 'pose':
        return row.landmark_index + 30
    elif row.type == 'left_hand':
        return row.landmark_index + 80
    else:
        return row.landmark_index

def filter_group(group):
    if group[group.type == 'right_hand'].x.isnull().all():
        new_group = group[group.type != 'right_hand']
        if new_group[new_group.type == 'left_hand'].x.isnull().all():
             return pd.DataFrame(columns=group.columns)
        return group
    else:
        new_group = group[group.type != 'left_hand']
        if new_group[new_group.type == 'right_hand'].x.isnull().all():
             return pd.DataFrame(columns=group.columns)


def visualise2d_landmarks(parquet_df):
    connections = [  # right hand
        [0, 1, 2, 3, 4,],
        [0, 5, 6, 7, 8],
        [0, 9, 10, 11, 12],
        [0, 13, 14, 15, 16],
        [0, 17, 18, 19, 20],

        # pose
        [38, 36, 35, 34, 30, 31, 32, 33, 37],
        [40, 39],
        [52, 46, 50, 48, 46, 44, 42, 41, 43, 45, 47, 49, 45, 51],
        [42, 54, 56, 58, 60, 62, 58],
        [41, 53, 55, 57, 59, 61, 57],
        [54, 53],

        # left hand
        [80, 81, 82, 83, 84, ],
        [80, 85, 86, 87, 88],
        [80, 89, 90, 91, 92],
        [80, 93, 94, 95, 96],
        [80, 97, 98, 99, 100], ]


    frames = sorted(set(parquet_df.frame))
    first_frame = min(frames)
    parquet_df['color'] = parquet_df.type.apply(lambda row: assign_color(row))
    parquet_df['plot_order'] = parquet_df.apply(lambda row: assign_order(row), axis=1)
    first_frame_df = parquet_df[parquet_df.frame == first_frame].copy()
    first_frame_df = first_frame_df.sort_values(["plot_order"]).set_index('plot_order')


    frames_l = []
    for frame in frames:
        filtered_df = parquet_df[parquet_df.frame == frame].copy()
        filtered_df = filtered_df.sort_values(["plot_order"]).set_index("plot_order")
        traces = [go.Scatter(
            x=filtered_df['x'],
            y=filtered_df['y'],
            # z=filtered_df['z'],
            mode='markers',
            marker=dict(
                color=filtered_df.color,
                size=9))]

        for i, seg in enumerate(connections):
            trace = go.Scatter(
                    x=filtered_df.loc[seg]['x'],
                    y=filtered_df.loc[seg]['y'],
                    # z=filtered_df.loc[seg]['z'],
                    mode='lines',
            )
            traces.append(trace)
        frame_data = go.Frame(data=traces, traces = [i for i in range(17)])
        frames_l.append(frame_data)

    traces = [go.Scatter(
        x=first_frame_df['x'],
        y=first_frame_df['y'],
        # z=first_frame_df['z'],
        mode='markers',
        marker=dict(
            color=first_frame_df.color,
            size=9
        )
    )]
    for i, seg in enumerate(connections):
        trace = go.Scatter(
            x=first_frame_df.loc[seg]['x'],
            y=first_frame_df.loc[seg]['y'],
            # z=first_frame_df.loc[seg]['z'],
            mode='lines',
            line=dict(
                color='black',
                width=2
            )
        )
        traces.append(trace)
    fig = go.Figure(
        data=traces,
        frames=frames_l
    )

    # Layout
    fig.update_layout(
        width=1000,
        height=1800,
        scene={
            'aspectmode': 'data',
        },
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 100,
                                                  "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0}}],
                        "label": "▶",  # Using the Unicode character directly
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 10},  # Adjusted padding for clarity
                "font": {"size": 20},  # Adjusted font size for clarity
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
        ],
    )
    camera = dict(
        up=dict(x=0, y=-1, z=0),
        eye=dict(x=0, y=0, z=2.5)
    )
    fig.update_layout(scene_camera=camera, showlegend=False)
    fig.update_layout(xaxis = dict(visible=False),
            yaxis = dict(visible=False),
    )
    fig.update_yaxes(autorange="reversed")

    # fig.show()
    return fig

def visualiseavg_landmarks(parquet_df):
    connections = [  # right hand
        [0, 1, 2, 3, 4,],
        [0, 5, 6, 7, 8],
        [0, 9, 10, 11, 12],
        [0, 13, 14, 15, 16],
        [0, 17, 18, 19, 20],

        # pose
        [38, 36, 35, 34, 30, 31, 32, 33, 37],
        [40, 39],
        [52, 46, 50, 48, 46, 44, 42, 41, 43, 45, 47, 49, 45, 51],
        [42, 54, 56, 58, 60, 62, 58],
        [41, 53, 55, 57, 59, 61, 57],
        [54, 53],

        # left hand
        [80, 81, 82, 83, 84, ],
        [80, 85, 86, 87, 88],
        [80, 89, 90, 91, 92],
        [80, 93, 94, 95, 96],
        [80, 97, 98, 99, 100], ]

    first_frame_df = parquet_df.copy()
    first_frame_df['color'] = first_frame_df.type.apply(lambda row: assign_color(row))
    first_frame_df['plot_order'] = first_frame_df.apply(lambda row: assign_order(row), axis=1)
    first_frame_df = first_frame_df.groupby("plot_order").agg({'x':'mean', 'y':'mean', 'color':'first'}).reset_index()
    first_frame_df = first_frame_df.sort_values(["plot_order"]).set_index('plot_order')

    traces = [go.Scatter(
        x=first_frame_df['x'],
        y=first_frame_df['y'],
        # z=first_frame_df['z'],
        mode='markers',
        marker=dict(
            color=first_frame_df.color,
            size=9
        )
    )]
    for i, seg in enumerate(connections):
        trace = go.Scatter(
            x=first_frame_df.loc[seg]['x'],
            y=first_frame_df.loc[seg]['y'],
            # z=first_frame_df.loc[seg]['z'],
            mode='lines',
            line=dict(
                color='black',
                width=2
            )
        )
        traces.append(trace)
    fig = go.Figure(
        data=traces,
    )

    # Layout
    fig.update_layout(
        width=1000,
        height=1800)
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis = dict(visible=False),
                      yaxis = dict(visible=False),
                      )
    fig.update_yaxes(autorange="reversed")

    return fig