import dash
from UI.layout_main import app  # Importing the main layout
from dash.dependencies import Input, Output
from plots import line_plot, bar_plot, histogram_plot  # Importing plotting functions
from data_processing import MetaDataProcessor  # Importing data processing functions
import numpy as np
from UI.layout_tables import metadata_table_before_layout, metadata_table_after_layout  # Importing layout functions

# Dictionary defining options for dropdowns
options_dict = {
    '<': [{'label': 'Less Than', 'value': '<'}, {'label': 'Less Than Equals', 'value': '<='}],
    '<=': [{'label': 'Less Than Equals', 'value': '<='}],
    '>': [{'label': 'Greater Than', 'value': '>'}, {'label': 'Greater Than Equals', 'value': '>='}],
    '>=': [{'label': 'Greater Than', 'value': '>'}, {'label': 'Greater Than Equals', 'value': '>='}]
}

# Function to handle filter button click and toggle filter container visibility
def onclick_filter(n_clicks):
    if n_clicks % 2 != 0:
        return 'Collapse', {'display': 'block'}
    else:
        return 'Expand', {'display': 'none'}

# Function to update options for the upper range dropdown based on lower range selection
def update_upper_range_dropdown(lowerrange_relation_type):
    if lowerrange_relation_type is None or lowerrange_relation_type == '==':
        return [], True, True
    return [{'label': i['label'], 'value': i['value']} for i in options_dict[lowerrange_relation_type]], False, False

# Initializing the metadata processor with the dataset file
processor = MetaDataProcessor('datasets/multi_un/multi_un_de_M.jsonl')
#processor = MetaDataProcessor('datasets/meta.jsonl')

# Define callbacks for interactive components
app.callback(
    Output('filter-overlay', 'children'),
    Output('container-filter', 'style'),
    Input('filter-overlay', 'n_clicks'),
    prevent_initial_call=True
)(onclick_filter)

app.callback(
    Output('upperrange-relation-dropdown', 'options'),
    Output('upperrange-input-on-filter', 'disabled'),
    Output('upperrange-relation-dropdown', 'disabled'),
    Input('relation-dropdown', 'value'),
)(update_upper_range_dropdown)

@app.callback(
    [
        Output("before-viz-graph", "figure"),
        Output("stats-table-before", "data"),
        Output('metadata-values-table-before-container', 'children'),
    ],
    [
        Input("viz-dropdown", "value"),
        Input("sample-size-dropdown", "value"),
        Input("Meta Data", "value")
    ]
)
def update_graph(selected_value, sample_size, selected_metadata):
    # Retrieve the component that triggered the callback
    ctx = dash.callback_context
    triggered_component_id = ctx.triggered_id

    # Initialize the figure variable
    figure = {'data': []}

    if selected_metadata is None:
        return figure, [], []

    # Process data based on the selected sample size
    meta_data_sampled = processor.sample_meta_data(sample_size)

    # Reset the index and sort only the selected column
    meta_data_sampled_sorted = (
        meta_data_sampled.reset_index(drop=True)
        .sort_values(by=selected_metadata, ascending=True)
        .reset_index(drop=True)
        .reset_index(drop=False)
    )

    # Update figure based on selected visualization type
    if selected_value == "line":
        figure = line_plot(meta_data_sampled_sorted, selected_metadata)
    elif selected_value == "bar":
        figure = bar_plot(meta_data_sampled_sorted, selected_metadata)
    elif selected_value == "histogram":
        figure = histogram_plot(meta_data_sampled_sorted, selected_metadata)

    # Calculate summary statistics
    summary_stats = {
        "Minimum Value": round(np.min(meta_data_sampled_sorted[selected_metadata]), 3),
        "Maximum Value": round(np.max(meta_data_sampled_sorted[selected_metadata]), 3),
        "Mean": round(np.mean(meta_data_sampled_sorted[selected_metadata]), 3),
        "Median": round(np.median(meta_data_sampled_sorted[selected_metadata]), 3),
    }

    # Format summary statistics for DataTable
    summary_data = [{"Statistic": stat, "Value": value} for stat, value in summary_stats.items()]

    # Get the selected metadata values
    sampled_values_before = meta_data_sampled_sorted[selected_metadata].head(5).tolist()

    # Generate layout for metadata table before filtering
    metadata_table_before = metadata_table_before_layout(sampled_values_before, selected_metadata)
    return figure, summary_data, metadata_table_before

# Callback to update filtered data visualization and statistics
@app.callback(
    [
        Output('after-viz-graph', 'figure'),
        Output('upperrange-relation-dropdown', 'value'),
        Output('upperrange-input-on-filter', 'value'),
        Output('relation-dropdown', 'value'),
        Output('input-on-filter', 'value'),
        Output('stats-table-after', 'data'),
        Output('metadata-values-table-after-container', 'children'),
        Output("filtered-data-count", 'children'),
        Output('filtered-data-count', 'style')
    ],
    [
        Input('upperrange-relation-dropdown', 'value'),
        Input('upperrange-input-on-filter', 'value'),
        Input('relation-dropdown', 'value'),
        Input('input-on-filter', 'value'),
        Input('viz-dropdown', 'value'),
        Input('sample-size-dropdown', 'value'),
        Input('MetaData_filter', 'value'),
        Input("filtered-data-count", 'children'),
        Input('Meta Data', 'value'),
        Input('reset-overlay', 'n_clicks')
    ],
    prevent_initial_call=True
)
def update_filter_graph(
    upperrange_relation_type, upperrange_relation_value, lowerrange_relation_type,
    lowerrange_relation_value, selected_graph_type, sample_size, selected_metadata,
    filtered_label_text, original_metadata, reset_n_clicks
):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id.split('.')[0]

    if lowerrange_relation_value is None:
        return {'data': []}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, [], [], dash.no_update, dash.no_update  # Add an empty list for stats-table-after

    if triggered_id == 'reset-overlay':
        return {'data': []}, None, None, None, None, [], [], dash.no_update, {"width": "100%", "text-align": "center", 'display': 'none'}  # Add an empty list for stats-table-after

    # Process data based on the selected sample size
    meta_data_sampled = processor.sample_meta_data(sample_size)

    # Build the query for filtering
    query_parts = [f"{selected_metadata}{lowerrange_relation_type}{lowerrange_relation_value}"]
    if upperrange_relation_type is not None and upperrange_relation_value is not None:
        query_parts.append(f"{selected_metadata}{upperrange_relation_type}{upperrange_relation_value}")

    query = " & ".join(query_parts)
    query = f"not ({query})"

    # Filter the sampled data
    meta_data_sampled_filtered = meta_data_sampled.query(query)

    # Sort the sampled and filtered data
    meta_data_sampled_filtered = meta_data_sampled_filtered.sort_values(by=original_metadata).reset_index(drop=True)
    num_filtered_docs = len(meta_data_sampled_filtered)
    num_original_docs = len(meta_data_sampled)
    filtered_label_text = f"Filtered {num_filtered_docs} out of {num_original_docs} documents"
    filtered_label_style = {"width": "100%", "text-align": "center", 'display': 'block'}

    # Update figure based on selected graph type
    if selected_graph_type == "line":
        figure = line_plot(meta_data_sampled_filtered, original_metadata)
    elif selected_graph_type == "bar":
        figure = bar_plot(meta_data_sampled_filtered, original_metadata)
    elif selected_graph_type == "histogram":
        figure = histogram_plot(meta_data_sampled_filtered, original_metadata)

    # Create summary statistics for DataTable
    summary_stats_after = {
        "Minimum Value": np.min(meta_data_sampled_filtered[original_metadata]),
        "Maximum Value": np.max(meta_data_sampled_filtered[original_metadata]),
        "Mean": np.mean(meta_data_sampled_filtered[original_metadata]),
        "Median": np.median(meta_data_sampled_filtered[original_metadata]),
    }

    # Format summary statistics for DataTable
    summary_data_after = [{"Statistic": stat, "Value": round(value, 3)} for stat, value in summary_stats_after.items()]

    # Get the selected metadata values after filtering
    sampled_values_after = meta_data_sampled_filtered[original_metadata].head(5).tolist()

    # Generate layout for metadata table after filtering
    metadata_table_after = metadata_table_after_layout(sampled_values_after, selected_metadata)
    return figure, dash.no_update, dash.no_update, dash.no_update, dash.no_update, summary_data_after, metadata_table_after, filtered_label_text, filtered_label_style

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
