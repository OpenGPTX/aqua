import plotly.graph_objects as go

# Function to set axis title for the plot
def set_axis_title(fig, title):
    fig.update_layout(xaxis_title=title)
    return fig

# Function to create a line plot
def line_plot(meta_data_sampled_sorted, selected_metadata):
    fig = go.Figure(data=go.Scatter(x=meta_data_sampled_sorted.index, y=meta_data_sampled_sorted[selected_metadata], mode='lines'))
    return set_axis_title(fig, 'Documents')

# Function to create a bar plot
def bar_plot(meta_data_sampled_sorted, selected_metadata):
    fig = go.Figure(data=go.Bar(x=meta_data_sampled_sorted.index, y=meta_data_sampled_sorted[selected_metadata]))
    fig.update_traces(marker_color='blue', marker_line_color='blue', selector=dict(type="bar"))
    return set_axis_title(fig, 'Documents')

# Function to create a histogram plot
def histogram_plot(meta_data_sampled_sorted, selected_metadata):
    fig = go.Figure(data=go.Histogram(x=meta_data_sampled_sorted[selected_metadata], nbinsx=100))
    return set_axis_title(fig, 'Documents')

# Function to create a pie chart
def pie_chart(dataframe, names, values, title, textposition='inside', textinfo='percent+label'):
    fig = go.Figure(data=[go.Pie(labels=dataframe[names], values=dataframe[values])])
    fig.update_traces(textposition=textposition, textinfo=textinfo)
    fig.update_layout(
        title_text=title,
        title_font=dict(size=20, family='Arial', color='black'),
    )
    return fig
