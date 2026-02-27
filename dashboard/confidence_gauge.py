import plotly.graph_objects as go

def confidence_gauge(confidence):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'value': confidence * 100
            }
        },
        title={'text': "Prediction Confidence"}
    ))
    fig.update_layout(height=300)
    return fig
