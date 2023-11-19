# 2023.11.16  19.00
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import skimage as ski
from skimage import data
# pip install scikit-image

from skimage.feature import Cascade
from skimage.filters import gaussian

dash.register_page(__name__, name='Image Face Analysis')

pics_file1 = './assets/test_pic_1.jpg'
pics_file2 = './assets/test_pic_2.jpg'
pics_file3 = './assets/test_pic_3.jpg'
pics_file4 = './assets/test_pic_4.jpg'
pics_file5 = './assets/test_pic_5.jpg'
pics_file6 = './assets/test_pic_6.jpg'
#pics_file = dash.get_asset_url('test_pic_1.jpg')

layout = dbc.Container([

    dbc.Row([ 
    #dcc.Markdown('# Life Expectancy Dashboard')
    html.Div('Face Recognization (with sci-kit learn) Dashboard', className="text-primary text-center fs-4")
    ]),
    #html.Div(html.Img(src=app.get_asset_url('logo.png'), style={'height':'10%', 'width':'10%'}))

    dbc.Row([

        dbc.Col(           
            dbc.Card([
            html.H6('Choose Face Image'),
            dcc.Dropdown(id='pic_dropdown', #options=[pics_file1, pics_file2, pics_file3], value=pics_file1
             options=[
                {'label': 'Face File 1', 'value': pics_file1},
                {'label': 'Face File 2', 'value': pics_file2},
                {'label': 'Face File 3', 'value': pics_file3},
                {'label': 'Face File 4', 'value': pics_file4},
                {'label': 'Face File 5', 'value': pics_file5},
                {'label': 'Face File 6', 'value': pics_file6}
            ], value=pics_file1)
            ], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "height": "90px"}), 
        width=5),

        dbc.Col(           
            dbc.Card([
            html.H6('Choose recog. min'),
            dcc.Dropdown(id='minsize_dropdown', options=[20,25,30,35,40,45,50,55,60], value=50)
            ], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "height": "90px"}), 
        width=2),

        dbc.Col( 
            dbc.Card( [
                html.H6('Select Gauss Blur (Privacy protection)'),
                dcc.Slider(id="gauss_slider", min=0, max=10, value=0, step=1),      
            ], style= {'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px',"font-size": "12px", "height": "90px"}),  
        width=5) #overflow=Auto           
   
    ], style={'margin-top':'20px'}),

    dbc.Row([
        dbc.Col(  
            dbc.Card([
                html.H6('Face Recognization Image'),
                dcc.Graph(id="graph-face-img", config={'displayModeBar': False}), #figure=fig
                dcc.Store(id='detected_rect'), 
                #html.Img(src=dash.get_asset_url('test_pic_1.jpg'), style={'height':'70%', 'width':'70%'}),
            ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}),
        width=12) 
    ], style={'margin-top':'20px'}),  #width=4) 

], fluid=True)

# ---------- Set Minsize & Gauss slider to default (50,0) when Pic dropdown changes ----------
@callback(
    Output("minsize_dropdown", "value"), # Set Minsize slider value -> 50
    Output("gauss_slider", "value"), # Set Gauss slider value -> 0
    Input("pic_dropdown", "value"))
def set_minsize(pic_dropdown):
    minsize_val = 50 
    slider_val = 0 
    return minsize_val, slider_val

# ---------- Set Gauss slider to default (0) when MInsize dropdown changes ----------
@callback(
    Output("gauss_slider", "value", allow_duplicate=True), # Set Gauss slider value -> 0
    Input("minsize_dropdown", "value"),
    prevent_initial_call=True)
def set_minsize(minsize_dropdown):
    slider_val = 0 
    return  slider_val

# ---------- Face recognization in pic (Cascade) ----------
@callback(
    Output("graph-face-img", "figure"),
    Output("detected_rect", "data"),
    Input("pic_dropdown", "value"),
    Input("minsize_dropdown", "value")
)
def on_load_train(pics_file, minsize_val):  
    img_file = ski.io.imread(pics_file)
    fig = px.imshow(img_file)
    trained_file = data.lbp_frontal_face_cascade_filename()
    detector = Cascade(trained_file)
    detected_rect = detector.detect_multi_scale(img=img_file, scale_factor=1.2, step_ratio=1, min_size=(minsize_val, minsize_val),  max_size=(120, 120))  
    return fig, detected_rect

# ---------- Red rect or Gauss Blur on faces in pic ----------
@callback(
    Output("graph-face-img", "figure", allow_duplicate=True),
    Input("pic_dropdown", "value"),
    Input("detected_rect", "data"),
    Input("gauss_slider", "value"),
    prevent_initial_call=True)
def on_style_change(pics_sel, detected_rect, gauss_value):

    img_file = ski.io.imread(pics_sel)
    fig = px.imshow(img_file)

    def getFaceRect(img, d):
        x, y = d['r'], d['c']
        width, height = d['r'] + d['width'], d['c'] + d['height']
        face = img[x:width, y:height]
        return face
    
    def mergeBlurryFace(original, gauss_img):
        x, y = d['r'], d['c']
        width, height = d['r'] + d['width'], d['c'] + d['height']
        original[x:width, y:height] = gauss_img 
        return original

    for d in detected_rect:
        face = getFaceRect(img_file, d)
        gaussian_face =  gaussian(face, sigma=gauss_value, preserve_range=True)
        resulting_image = mergeBlurryFace(img_file, gaussian_face)
       
    if gauss_value != 0:
        fig = px.imshow(resulting_image)
    else:
        fig = px.imshow(resulting_image)
        for d in detected_rect:
            fig.add_shape(type="rect",x0=d['c'], x1=d['c'] + d['width'], y0=d['r'], y1=d['r'] + d['height'],line_color="Red")

    fig.update_layout(margin=dict(l=10, r=10, t=0, b=10, pad=0))
  
    return fig
