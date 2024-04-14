import dash
from dash import dcc, html
from data_processing import WordCountProcessor
from UI.layout_graphs import (
    get_corpora_statistics_graphs,
    get_original_filtered_data_graphs
)
from UI.layout_stats import get_corpora_statistics_layout
from UI.layout_utils import metadata_options

# Initialize Dash app
app = dash.Dash(__name__)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Initialize WordCountProcessor and read word count files
word_count_processor = WordCountProcessor('wordcounts')
word_count_df = word_count_processor.read_word_count_files()

# Calculate dataset statistics
datasets_by_lang_df = word_count_df.value_counts('language').reset_index()
datasets_by_lang_df.columns = ['language', 'count']
datasets_by_documents_df = word_count_df.groupby('language')['num_documents'].sum().reset_index()
datasets_by_wordcount_df = word_count_df.groupby('language')['num_words'].sum().reset_index()
datasets_by_charcount_df = word_count_df.groupby('language')['num_chars'].sum().reset_index()

# Define metadata tables
metadata_table_before = html.Div(id='metadata-values-table-before-container',
                                 style={"margin-top": "20px", "margin-left": "30px", "width": "48%"})
metadata_table_after = html.Div(id='metadata-values-table-after-container',
                                style={"margin-top": "20px", "margin-left": "30px", "width": "48%"})

# Define app layout
app.layout = html.Div(
    children=[
        html.H1("Visualization of Document Quality Criteria - VIDOQ",
                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        # Display corpus statistics graphs
        get_corpora_statistics_graphs(datasets_by_lang_df, datasets_by_documents_df,
                                      datasets_by_wordcount_df, datasets_by_charcount_df),
        html.Div([
            html.H2("Corpus Statistics"),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        html.Div([
            html.Div([
                html.H3("Select Sample Size"),
                dcc.Dropdown(
                    id="sample-size-dropdown",
                    options=[
                        {"label": 'All', "value": 'All'} if i == 6 else {"label": str(10 ** i), "value": i}
                        for i in range(1, 7)
                    ],
                    value='All',  
                    style={"width": "85%"}
                ),
            ], style={'width': '20%', 'display': 'inline-block', 'margin': '30px'}),

            html.Div([
                html.H3("Select Corpus"),
                dcc.Dropdown(
                    id="Dataset",
                    options=[
                        {"label": "multi_un", "value": "option1"},
                    ],
                    value=None,  # Set default value to None
                    style={"width": "85%"},
                ),
            ], style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                html.H3("Select Meta Data"),
                dcc.Dropdown(
                    id="Meta Data",
                    options=metadata_options,
                    value=None,  # Set default value to None
                    style={"width": "85%"},
                ),
            ], style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                html.H3("Select Visualization Type"),
                dcc.Dropdown(
                    id="viz-dropdown",
                    options=[
                        {"label": "Line Plot", "value": "line"},
                        {"label": "Bar chart", "value": "bar"},
                        {"label": "Histogram", "value": "histogram"},
                    ],
                    value=None,  # Set default value to None
                    style={"width": "85%"},
                ),
            ], style={'width': '20%', 'display': 'inline-block'}),
            get_corpora_statistics_layout(datasets_by_lang_df, datasets_by_documents_df,
                                          datasets_by_wordcount_df, datasets_by_charcount_df),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Select a filter criterion")
                    ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
                    html.Button('Expand', id='filter-overlay', n_clicks=0, style={"display": "inline-block",
                                                                                   "align": "center"}),
                    html.Button('Reset', id='reset-overlay', n_clicks=0,
                                style={"display": "inline-block", "align": "center", 'margin-left': '10px'}),
                ], style={'width': '100%', 'display': 'inline-block'}),
                html.Div(id="container-filter", children=[
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id="MetaData_filter",
                                options=metadata_options,
                                value=None,  # Set default value to None
                                placeholder="Select Metadata",
                                style={"width": "80%"},
                            ),
                        ], style={"width": "30%", 'display': 'inline-block', 'vertical-align': 'top'}),

                        html.Div([
                            dcc.Dropdown(
                                id="relation-dropdown",
                                options=[
                                    {"label": "Greater Than", "value": "<"},
                                    {"label": "Less Than", "value": ">"},
                                    {"label": "Greater Than Equals", "value": "<="},
                                    {"label": "Less Than Equals", "value": ">="},
                                    {"label": "Equal To", "value": "=="},
                                ],
                                value=None,
                                placeholder="Select lower criteria",
                                style={"width": "95%"},
                            )
                        ], style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}),
                        html.Div([
                            dcc.Input(id='input-on-filter', type='text', style={'height': '100%'}),
                        ], style={'width': '20%', 'height': '30px', 'display': 'inline-block',
                                  'vertical-align': 'top'}),
                        html.Div([
                            dcc.Dropdown(
                                id="upperrange-relation-dropdown",
                                style={"width": "95%"},
                                value=None,
                                placeholder="Select upper criteria",
                                disabled=False
                            )
                        ], style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}),
                        html.Div([
                            dcc.Input(id='upperrange-input-on-filter', type='text', style={'height': '100%'},
                                      disabled=False),
                        ], style={'width': '20%', 'height': '30px', 'display': 'inline-block',
                                  'vertical-align': 'top'})
                    ], style={'width': '100%', 'height': '60px', 'margin-top': '20px',
                              'position': 'relative', 'display': 'inline-block'}),
                ], style={'display': 'none', 'margin': 'auto', 'width': '350px', 'padding-top': '20px'})
            ], style={'padding': '20px', 'margin': '30px', 'background-color': '#f2f2f2'}),

            # Display original and filtered data graphs
            get_original_filtered_data_graphs(),
        ]
        )
    ]
)
