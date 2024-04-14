from dash import html, dash_table

# Function to generate layout for metadata table before filtering
def metadata_table_before_layout(sampled_values_before, selected_metadata):
    return html.Div([
        html.H3("Data before filtering"),
        dash_table.DataTable(
            id='metadata-values-table-before',
            columns=[
                {"name": "Index", "id": "Index"},  # Column for index
                {"name": f"MetaData Field: {selected_metadata}", "id": "Values"}  # Column for metadata values
            ],
            data=[  # Data rows
                {"Index": index, "Values": round(value, 3)} for index, value in enumerate(sampled_values_before, start=1)
            ],
            style_data_conditional=[  # Conditional styling for data cells
                {'if': {'column_id': 'Values'}, 
                 'fontWeight': 'bold', 
                 },
            ],
            style_header_conditional=[  # Conditional styling for header cells
                {'if': {'column_id': 'Index'}, 
                 'fontWeight': 'bold',  
                 },
                {'if': {'column_id': 'Values'}, 
                 'fontWeight': 'bold', 
                 }
            ],
            style_table={'width': "50%"},  # Table width
            style_cell={'textAlign': 'left'},  # Cell text alignment
        )
    ])

# Function to generate layout for metadata table after filtering
def metadata_table_after_layout(sampled_values_after, original_metadata):
    return html.Div([
        html.H3("Data after filtering"),
        dash_table.DataTable(
            id='metadata-values-table-after',
            columns=[
                {"name": "Index", "id": "Index"},  # Column for index
                {"name": f"MetaData Field: {original_metadata}", "id": "Values"}  # Column for metadata values
            ],
            data=[  # Data rows
                {"Index": index, "Values": round(value, 3)} for index, value in enumerate(sampled_values_after, start=1)
            ],
            style_data_conditional=[  # Conditional styling for data cells
                {'if': {'column_id': 'Values'}, 
                 'fontWeight': 'bold',  
                 },
            ],
            style_header_conditional=[  # Conditional styling for header cells
                {'if': {'column_id': 'Index'},  
                 'fontWeight': 'bold', 
                 },
                {'if': {'column_id': 'Values'}, 
                 'fontWeight': 'bold',  
                 }
            ],
            style_table={'width': "50%"},  
            style_cell={'textAlign': 'left'},  
        )
    ])
