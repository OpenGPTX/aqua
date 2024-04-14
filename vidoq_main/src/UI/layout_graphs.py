from dash import html, dcc
from plots import pie_chart  

# Function to generate corpora statistics graphs
def get_corpora_statistics_graphs(datasets_by_lang_df, datasets_by_documents_df, datasets_by_wordcount_df, datasets_by_charcount_df):
    # Define graphs as a Div containing various statistical graphs
    graphs = html.Div([
        # Header
        html.H2("Corpora Statistics", style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        # Row containing pie charts for datasets by language and documents by language
        html.Div([
            dcc.Graph(figure=pie_chart(datasets_by_lang_df, 'language', 'count', 'Datasets by Language')),
            dcc.Graph(figure=pie_chart(datasets_by_documents_df, 'language', 'num_documents', 'Documents by Language')),
        ], style={"display": "flex", "flexDirection": "row", "width": "100%", 'justify-content': 'center', 'align-items': 'center'}),
        # Row containing pie charts for words by language and characters by language
        html.Div([
            dcc.Graph(figure=pie_chart(datasets_by_wordcount_df, 'language', 'num_words', 'Words by Language')),
            dcc.Graph(figure=pie_chart(datasets_by_charcount_df, 'language', 'num_chars', 'Characters by Language')),
        ], style={"display": "flex", "flexDirection": "row", "width": "100%", 'justify-content': 'center', 'align-items': 'center'}),
    ])
    return graphs

# Function to generate original and filtered data graphs
def get_original_filtered_data_graphs():
    # Define graphs as a Div containing original and filtered data graphs
    graphs = html.Div([
        html.Div([
            html.H2("Original Data"),
            dcc.Graph(id="before-viz-graph", style={"width": "100%", "height": "500px"}),
        ], style={"text-align": "center", "width": "49%"}),

        html.Div([
            html.H2("Filtered Data"),
            dcc.Graph(id="after-viz-graph", style={"width": "100%", "height": "500px"}),
            html.Label('filtered documents',id="filtered-data-count", style={"width": "100%", "text-align": "center", 'display': 'none'})
        ], style={"text-align": "center", "width": "49%"}),
    ], style={'display': 'flex', 'justify-content': 'space-between'})

    return graphs
