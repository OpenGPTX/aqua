from dash import html, dash_table

def get_corpora_statistics_layout(datasets_by_lang_df, datasets_by_documents_df, datasets_by_wordcount_df, datasets_by_charcount_df):
    # Define placeholders for displaying metadata values
    metadata_table_before = html.Div(id='metadata-values-table-before-container', style={"margin-top": "20px", "margin-left": "30px", "width": "48%"})
    metadata_table_after = html.Div(id='metadata-values-table-after-container', style={"margin-top": "20px", "margin-left": "30px", "width": "48%"})

    # Define the layout structure
    layout = html.Div([
        html.Div([
            html.H2("Corpus Statistics"),  # Section title
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),

        html.Div(
            [
                # Summary statistics for the dataframe before filtering
                html.Div([
                    html.H3("Corpus Statistics Before Filtering"),  # Subsection title
                    # Dash DataTable for displaying statistics before filtering
                    dash_table.DataTable(
                        id="stats-table-before",
                        columns=[
                            {"name": "Statistic", "id": "Statistic"}, 
                            {"name": "Value", "id": "Value"},
                        ],
                        style_table={"width": "50%"}, 
                        style_cell={'textAlign': 'left'},
                        style_data_conditional=[ 
                            {
                                'if': {'column_id': 'Value'},
                                'fontWeight': 'bold', 
                            },
                        ],
                        style_cell_conditional=[  
                            {
                                'if': {'column_id': 'Statistic'},
                                'textAlign': 'left',  
                                'width': '40%', 
                            },
                        ],
                        style_header={'fontWeight': 'bold'} 
                    ),
                ],
                    style={"margin-top": "20px", "margin-left": "30px", "width": "48%",  # Set style properties
                           'display': 'inline-block'}  # Display inline
                ),
                # Summary statistics for after filtering
                html.Div([
                    html.H3("Corpus Statistics After Filtering"),  # Subsection title
                    # Dash DataTable for displaying statistics after filtering
                    dash_table.DataTable(
                        id="stats-table-after",
                        columns=[
                            {"name": "Statistic", "id": "Statistic"},  
                            {"name": "Value", "id": "Value"},
                        ],
                        style_table={"width": "50%"},  
                        style_cell={'textAlign': 'left'},  
                        style_data_conditional=[  
                            {
                                'if': {'column_id': 'Value'},
                                'fontWeight': 'bold',  
                            },
                        ],
                        style_cell_conditional=[  
                            {
                                'if': {'column_id': 'Statistic'},
                                'textAlign': 'left',  
                                'width': '40%', 
                            },
                        ],
                        style_header={'fontWeight': 'bold'}  
                    ),
                ], style={"margin-top": "20px", "margin-left": "30px", "width": "48%",  # Set style properties
                           'display': 'inline-block'}  # Display inline
                ),
            ], style={'display': 'flex', 'justify-content': 'space-between'}),  # Set flexbox properties

        # Placeholder for displaying metadata values
        html.Div([
            metadata_table_before,
            metadata_table_after
        ], style={'display': 'flex', 'justify-content': 'space-between'}) 
    ])

    return layout
