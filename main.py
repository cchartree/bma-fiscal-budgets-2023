import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

disp = pd.read_csv('/home/cchartree/static/BMA Fiscal Budgets 2023 for deployment.csv')
disp['All_Categories'] = 1

list_topics = [
      'Generic_Administrations'
    , 'Maintenances'
    , 'Projects'
    , 'Communities'
    , 'Floods'
    , 'District_Offices'
    , 'Human_Resources'
    , 'Revenues'
    , 'Trainings'
    , 'Public_Relations'
    , 'Welfares'
    , 'Waste_Water_Treatments'
    , 'Hygienic_Foods'
    , 'Non-smoking_Zones'
    , 'Cleanings'
    , 'Disease_Controls'
    , 'Law_Enforcements'
    , 'Green_Zones'
    , 'Traffic_Managements'
]

list_keywords = [
      r'งานบริหารท'
    , r'รุงรักษา|งานดูแล|ปรับปรุง'
    , r'โครงการ'
    , r'พัฒนาชุมชน'
    , r'งานระบาย|ญหาน'
    , r'กงานเขต'
    , r'บุคลากร|บุคคล'
    , r'บรายได'
    , r'อบรม|หลักสูตร'
    , r'ประชาสัมพ'
    , r'สวัสดิการ'
    , r'บัดน(.*)เสีย'
    , r'อาหารปลอดภ'
    , r'เขตปลอดบุหรี่'
    , r'ความสะอาด'
    , r'โรค'
    , r'บังคับใช(.*)กฎหมาย'
    , r'สวน(.*)สีเขียว'
    , r'จราจร'
]


list_topics2 = list_topics
list_topics2.append('All_Categories')
print(list_topics2)






# -------------------------------------------------------------

app.layout = html.Div([

    html.H1('BMA Budget Allocations for Fiscal Year 2023', style={'text-align': 'center'}),

    html.Br(),

    dcc.Graph(id='BudgetHBarA', figure={}),

    html.Br(),

    dcc.Graph(id='BudgetHBarB', figure={}),

    html.Br(),

    html.H5('Categories by keywords (choose all that apply):'),

    dcc.Dropdown(
        id='w_keywords',
        options=list_topics2,
        multi=True,
        value='All_Categories',
        style={'width': '50%'}
    ),

    html.Br(),

    html.H5('Top Ranks:'),

    dcc.Slider(
        id='w_topranks',
        value=20,
        min=5,
        max=200,
        step=1,
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Br(),

    html.H5('Minimum Budget (THB millions):'),

    dcc.Slider(
        id='w_minbudgets',
        value=0,
        min=0,
        max=5000,
        step=100,
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Br(),

    html.H5('Maximum Budget (THB millions):'),

    dcc.Slider(
        id='w_maxbudgets',
        value=20000,
        min=0,
        max=20000,
        step=100,
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Br(),

    html.H5('Category (in Thai) contains:'),

    dcc.Textarea(
        id='w_textsearch_h1',
        value=' ',
        style={'width': '50%'},
    ),

    html.Br(),

    html.H5('Detailed descriptions (in Thai) contains:'),

    dcc.Textarea(
        id='w_textsearch_raw',
        value=' ',
        style={'width': '50%'},
    )

    # html.Div(id='output_container', children=[]),

    # html.Br(),

    # dcc.Graph(id='BudgetHBarA', figure={}),

    # html.Br(),

    # dcc.Graph(id='BudgetHBarB', figure={})

])


# -------------------------------------------------------------

numcol = 'Budgets Mn'

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='BudgetHBarA', component_property='figure'),
     Output(component_id='BudgetHBarB', component_property='figure')],
    [Input(component_id='w_keywords', component_property='value'),
     Input(component_id='w_topranks', component_property='value'),
     Input(component_id='w_minbudgets', component_property='value'),
     Input(component_id='w_maxbudgets', component_property='value')
    #  ,Input(component_id='w_textsearch_h1', component_property='value')
    #  ,Input(component_id='w_textsearch_raw', component_property='value')
     ]
)

def update_graph(w_kw, w_top, w_min, w_max, w_text_h1, w_text_raw):
# def update_graph(w_kw, w_top, w_min, w_max):

    chains = '(' + ' == 1) | ('.join(w_kw) + ' == 1)'
    dfplot = disp.query(chains)
    dfplot2 = dfplot[
                          (dfplot['Raw2'].str.contains(w_text_raw))
                        & (dfplot['h1desc'].str.contains(w_text_h1))
                    ]

    container = ' '

    dfplota = dfplot2
    dfplota = dfplota[['h1desc', numcol]].groupby(['h1desc'], as_index=False)[numcol].agg('sum')
    dfplota = dfplota.sort_values(by=[numcol]).tail(w_top)
    dfplota = dfplota[
        (dfplota[numcol] >= w_min)
        & (dfplota[numcol] <= w_max)
        ]

    figa = px.bar(data_frame=dfplota, y='h1desc', x=numcol, orientation='h', width=1400, height=450)

    dfplotb = dfplot2
    dfplotb = dfplotb[['Raw2', numcol]].groupby(['Raw2'], as_index=False)[numcol].agg('sum')
    dfplotb = dfplotb.sort_values(by=[numcol]).tail(w_top)
    dfplotb = dfplotb[
        (dfplotb[numcol] >= w_min)
        & (dfplotb[numcol] <= w_max)
        ]

    figb = px.bar(data_frame=dfplotb, y='Raw2', x=numcol, orientation='h', width=1400, height=450)

    return container, figa, figb


if __name__ == '__main__':
    app.run_server(debug=True)
