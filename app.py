import param 
import panel as pn
from panel.template.base import _base_config
import svgwrite
#import cloudconvert
import os

pn.extension(sizing_mode='stretch_width')
#API_KEY = os.environ.get('CLOUDCONVERT_API_KEY')
#cloudconvert.configure(api_key = API_KEY, sandbox = False)

live_dict = {"Seattle": "#1DC2BB",
               "San Francisco": "#143250",
               "Silicon Valley": "#2966A3",
               "Salt Lake": "#FF9233",
               "Chicago": "#C0D461",
               "Dallas": "#B72A33",
               "Dakotas": "#6E5577"}
role_dict = {"National": "#FCED1E",
             "Seattle": "#1DC2BB",
             "San Francisco": "#143250",
             "Silicon Valley": "#2966A3",
             "Chicago": "#C0D461",
             "Dallas": "#B72A33",
             "Between engagements": "#83ECE7"}
service_line_dict = {"Data Analysis & Visualization": ["DDI",1],
                "Data Science": ["DDI",2],
                "Data Engineering & Cloud Services": ["DDI",3],
                "Information Management": ["DDI",4],
                "Financial Insights": ["DDI",5],
                "Project & Program Management": ["BA",1],
                "Lean & Agile": ["BA",2],
                "Organizational Effectiveness": ["BA",3],
                "Strategy & Transformation": ["BA",4],
                "Business & Functional Analysis": ["BA",5],
                "Product Management": ["BA",6],
                "Marketing": ["BA",7],
                "Solution Architecture & Engineering": ["TE",1],
                "DevOps & Cloud Infrastructure": ["TE",2], 
                "Quality Engineering": ["TE",3],
                "Salesforce": ["TE",4],
                "Experience Design": ["TE",5],
                "Technical Solution Delivery": ["TE",6],
                "Enterprise Applications & Integration": ["TE",7],
                "Applied AI & Cognitive Services": ["TE",8],
                "Power Apps": ["TE",9],
                "Security, Privacy & Compliance": ["TE", 10]}
inter_func_dict = {"People Team":1, 
                   "Talent Acquisition":2,
                   "Business Development": 3,
                   "Operations":4,
                   "Finance": 5,
                   "Brand/Marketing":6 ,
                   "Service Line Support": 7,
                   "Industry Support": 7,
                   "Practices": 8, 
                   "Accounts": 9,
                   "Industries": 10, 
                   "Delivery":11, 
                   "Culture": 12}


industry_dict = {"Neither": "",
                 "Healthcare & Life Sciences": "2", 
                 "Energy & Utilities": "6",
                 "Telecommunications": "2 4 6 4", 
                 "Nonprofit": "2 2 2 2 6 2",
                 "High-Tech": "12 4",
                 "Financial Services": "4 8", 
                 "Product": "4 4 8 4", 
                 "Retail": "2 6"}
role_options = ['I consult with clients ONLY', 'I have an internal role ONLY', 'I consult AND have an internal role']
time_types = ["Morning Lark", "Afternoon Eagle", "Night Owl"]

class AutoStart(param.Parameterized):
    name_input = param.String(label= "My name is (first and last)")
    market_input = param.Selector(label="I live in", objects=list(live_dict.keys()))
    time_type = param.Selector(label="I am a", objects=time_types)
    selected = param.Selector(objects=role_options)

    def panel(self):
        return pn.Column(pn.widgets.TextInput.from_param(self.param.name_input), pn.layout.VSpacer(), \
                         "I live in", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.market_input, button_type="success"), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "People work best at different times of day. Tell us when you do your best work. I am a", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.time_type, button_type="success"), max_width=400, align='center'), pn.layout.Divider(), \
                         "Some Unifiers consult with their clients. Other Unifiers are internal and support our consultants (e.g., finance , operations, and people team). Then there are Unifiers who are hybrids and both consult as well as help shape the business (i.e., via leadership on practices, accounts, industries, or in an advocate role).",\
                         "Which one are you?", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.selected, button_type="success"), max_width=600, align='center'))

class ConsultantQuestions(AutoStart):
    client_input = param.Selector(objects=list(role_dict.keys())[1:])
    practice_input = param.Selector(objects=sorted(list(service_line_dict.keys())))
    industry_input = param.Selector( objects=list(industry_dict.keys())[:3])
    
    def panel(self):
        return pn.Column("My client work is in", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.client_input, button_type="success"), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "My primary practice is", pn.Row(pn.widgets.Select.from_param(self.param.practice_input, name=""),max_width=400, align='center'), pn.layout.VSpacer(), \
                         "Right now, Unify has 2 industry communities of practice. Do you belong to one?", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.industry_input, button_type="success"), max_width=400, align='center'))
                         
    
    @param.output('result')
    def output(self):
        consult_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "time_type": self.time_type,
                       "client_market": self.client_input,
                       "practice_input": self.practice_input,
                       "industry_input": self.industry_input, 
                       "internal_role_input": "",
                       "internal_market_input": "", 
                       "internal_func_input": ""}
        return consult_dict

class InternalQuestions(AutoStart):
    internal_func_input = param.Selector(objects=list(inter_func_dict.keys())[:7])
    internal_market_input = param.Selector(objects=["National"] + list(live_dict.keys()))
   
    def panel(self):    
        return pn.Column("As an internal Unifier, which internal function are you part of?", pn.Row(pn.widgets.Select.from_param(self.param.internal_func_input,name=""), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "I support ", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.internal_market_input, button_type="success"), max_width=600, align='center'))
    
    @param.output('result')
    def output(self):
        internal_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "time_type": self.time_type,
                       "client_market": "",
                       "practice_input": "",
                       "industry_input": "Neither", 
                       "internal_role_input": "",
                       "internal_market_input": self.internal_market_input, 
                       "internal_func_input": self.internal_func_input}
        return internal_dict

class HybridQuestions(AutoStart):
    client_input = param.Selector(objects=list(role_dict.keys())[1:])
    practice_input = param.Selector(objects=sorted(list(service_line_dict.keys())))
    industry_input = param.Selector(objects= list(industry_dict.keys())[:3])
    internal_func_input = param.Selector(objects=["None"]+list(inter_func_dict.keys())[:8])
    hybrid_role_input = param.ListSelector(objects=list(inter_func_dict.keys())[8:])
    internal_market_input = param.Selector(objects=["National"] + list(live_dict.keys()))
    
    def panel(self): 
        return pn.Column("My client work is in", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.client_input, button_type="success"), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "My primary practice is", pn.Row(pn.widgets.Select.from_param(self.param.practice_input, name=""), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "Right now, Unify has 2 industry communities of practice. Do you belong to one?", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.industry_input, button_type="success"), max_width=400, align='center'), pn.layout.Divider(),\
                        "As an internal Unifier, which internal function are you part of?", pn.Row(pn.widgets.Select.from_param(self.param.internal_func_input, name=""), max_width=600, align='center'),
                        "As a consultant, I lead and build communities in ", pn.Row(pn.widgets.CheckButtonGroup.from_param(self.param.hybrid_role_input, button_type="success"), max_width=600,  align='center'),
                        "My internal role supports ", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.internal_market_input, button_type="success"), max_width=600, align='center'))
    
    @param.output('result')
    def output(self):
        hybrid_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "time_type": self.time_type,
                       "client_market": self.client_input,
                       "practice_input": self.practice_input,
                       "industry_input": self.industry_input, 
                       "internal_role_input": self.hybrid_role_input,
                       "internal_market_input": self.internal_market_input, 
                       "internal_func_input": self.internal_func_input }
        return hybrid_dict
    
class DrawSVG(AutoStart):
    result = param.Dict()
    
    def panel(self):
        #get and clean values from inputs 
        name = self.result['name_input']
        live_market = self.result['live_input']
        time_type = self.result['time_type']
        client_market = self.result['client_market']
        practice = self.result['practice_input']
        industry = self.result['industry_input']
        internal_market = self.result['internal_market_input']
        internal_role = self.result['internal_role_input']
        internal_func = self.result['internal_func_input']

        try:
            service_line, sl_repeats = service_line_dict[practice]
        except:
            service_line, sl_repeats = "", 0
        try:
            int_repeats = inter_func_dict[internal_func]
        except:
            int_repeats = None           

        my_filename = name+'.svg'
        dwg = svgwrite.Drawing(my_filename, size=(400, 400), profile='full')
        dwg.add(dwg.rect(insert=(0,0), size=(400,400), fill=live_dict[live_market]))
        
        if time_type=="Afternoon Eagle":
            pattern = dwg.defs.add(dwg.pattern(insert=(0,0), size=(100, 100), patternUnits="userSpaceOnUse"))
            path = 'M11 18 c3.866 0 7 -3.134 7 -7 s-3.134 -7 -7 -7 -7 3.134 -7 7 3.134 7 7 7z m48 25 c3.866 0 7 -3.134 7 -7 s-3.134 -7 -7 -7 -7 3.134 -7 7 3.134 7 7 7z m-43 -7 c1.657 0 3 -1.343 3 -3 s-1.343 -3 -3 -3 -3 1.343 -3 3 1.343 3 3 3z m63 31 c1.657 0 3 -1.343 3 -3 s-1.343 -3 -3 -3 -3 1.343 -3 3 1.343 3 3 3z M34 90 c1.657 0 3 -1.343 3 -3 s-1.343 -3 -3 -3 -3 1.343 -3 3 1.343 3 3 3z m56 -76 c1.657 0 3 -1.343 3 -3 s-1.343 -3 -3 -3 -3 1.343 -3 3 1.343 3 3 3z M12 86 c2.21 0 4 -1.79 4 -4 s-1.79 -4 -4 -4 -4 1.79 -4 4 1.79 4 4 4z m28 -65 c2.21 0 4 -1.79 4 -4 s-1.79 -4 -4 -4 -4 1.79 -4 4 1.79 4 4 4z m23 -11 c2.76 0 5 -2.24 5 -5 s-2.24 -5 -5 -5 -5 2.24 -5 5 2.24 5 5 5z m-6 60 c2.21 0 4 -1.79 4 -4 s-1.79 -4 -4 -4 -4 1.79 -4 4 1.79 4 4 4z m29 22 c2.76 0 5 -2.24 5 -5 s-2.24 -5 -5 -5 -5 2.24 -5 5 2.24 5 5 5z M32 63 c2.76 0 5 -2.24 5 -5 s-2.24 -5 -5 -5 -5 2.24 -5 5 2.24 5 5 5z m57 -13 c2.76 0 5 -2.24 5 -5 s-2.24 -5 -5 -5 -5 2.24 -5 5 2.24 5 5 5z m-9 -21 c1.105 0 2 -.895 2 -2 s-.895 -2 -2 -2 -2 .895 -2 2 .895 2 2 2z M60 91 c1.105 0 2 -.895 2 -2 s-.895 -2 -2 -2 -2 .895 -2 2 .895 2 2 2z M35 41 c1.105 0 2 -.895 2 -2 s-.895 -2 -2 -2 -2 .895 -2 2 .895 2 2 2z M12 60 c1.105 0 2 -.895 2 -2 s-.895 -2 -2 -2 -2 .895 -2 2 .895 2 2 2z'
            pattern.add(dwg.path(d=path, style="fill:#FFFFFF; fill-opacity=0.8"))
        elif time_type=="Morning Lark":
            pattern = dwg.defs.add(dwg.pattern(insert=(0,0), size=(52, 26), patternUnits="userSpaceOnUse"))
            path = 'M10 10 c0 -2.21 -1.79 -4 -4 -4 c-3.314 0 -6 -2.686 -6 -6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 v2 c-3.314 0 -6 -2.686 -6 -6 0 -2.21 -1.79 -4 -4 -4 -3.314 0 -6 -2.686 -6 -6z m25.464 -1.95 l8.486 8.486 -1.414 1.414 -8.486 -8.486 1.414 -1.414z'
            pattern.add(dwg.path(d=path, style="fill:#FFFFFF; fill-opacity=0.8")) 
        elif time_type=="Night Owl":
            pattern = dwg.defs.add(dwg.pattern(insert=(0,0), size=(48, 64), patternUnits="userSpaceOnUse"))
            path ='M48 28 v-4 L36 12 24 24 12 12 0 24 v4 l4 4 -4 4 v4 l12 12 12 -12 12 12 12 -12 v-4 l -4 -4 4 -4z M8 32 l-6 -6 10 -10 10 10 -6 6 6 6 -10 10 L2 38 l6 -6z m12 0 l4 -4 4 4 -4 4 -4 -4z m12 0 l-6 -6 10 -10 10 10 -6 6 6 6 -10 10 -10 -10 6 -6z M0 16 L10 6 4 0 h4 l4 4 4 -4 h4 l-6 6 10 10 L34 6 l-6 -6 h4 l4 4 4 -4 h4 l-6 6 10 10 v4 L36 8 24 20 12 8 0 20 v-4z m0 32 l10 10 -6 6 h4l4 -4 4 4 h4 l-6 -6 10 -10 10 10 -6 6 h4 l4 -4 4 4 h4 l-6 -6 10 -10 v-4 L36 56 24 44 12 56 0 44 v4z'
            pattern.add(dwg.path(d=path, style="fill:#FFFFFF; fill-opacity=0.8"))
        
        dwg.add(dwg.rect(insert=(0,0), size=(400, 400), fill=pattern.get_paint_server()))
        dwg.add(dwg.circle(center=(200,200), r=190, fill="#FFFFFF"))

        #consulting glyph
        if client_market:
            dwg.add(dwg.path(d="M16,200 q124,-60 184,-184 q60,124 184,184 q-124,60 -184,184 q-60,-124 -184,-184 Z", style="fill:"+role_dict[client_market]+";fill-opacity:0.6"))

        #internal role glyph
        if internal_role or internal_func:
            dwg.add(dwg.path(d="M16,200 q124,-60 184,-184 q60,124 184,184 q-124,60 -184,184 q-60,-124 -184,-184 Z", 
                         style="fill:"+role_dict[internal_market]+";fill-opacity:0.6", transform="rotate(45 200 200)"))
        
        #hybrid role glyphs
        if internal_role:
            fill_op_list = [0.0, 0.0, 0.0, 0.0, 0.0]
            if "Practices" in internal_role:
                fill_op_list[0] = 1.0
            if "Accounts" in internal_role:
                fill_op_list[1] = 1.0 
            if "Industries" in internal_role:
                fill_op_list[2] = 1.0 
            if "Delivery" in internal_role:
                fill_op_list[3] = 1.0 
            if "Culture" in internal_role:
                fill_op_list[4] = 1.0

            for i in range(5):
                dwg.add(dwg.circle(center=(150+(i*25) ,150), r=10, style="fill:#143250; fill-opacity:"+str(fill_op_list[i])+";stroke:#143250;stroke-width:2"))

        if industry!="Neither" :
            dwg.add(dwg.line(start=(100,170), end=(300, 170), style="stroke:#143250;stroke-width:2;stroke-dasharray:"+str(industry_dict[industry])))
            dwg.add(dwg.line(start=(100,228), end=(300, 228), style="stroke:#143250;stroke-width:2;stroke-dasharray:"+str(industry_dict[industry])))

        #sequence for drawing center-out
        c_out = [178, 160, 196, 142, 214, 124, 232, 106, 250, 88]

        # get the shape path for service line
        if service_line=="DDI":
            s_path = " a20,20 0 0,1 40,0  a21,20.5 0 0,1 -20,20 a19.5,17.5 0 0,1 -19,-21"
        elif service_line == "BA":
            s_path = " q5,-7.5 20,-20 q20,17.5 20,20 q-12.5,17.5 -20,20 q-7.5,-10 -20,-20 Z"
        elif service_line == "TE":
            s_path = " m0,20 q17.5,-30 20,-40 q5,6 20,40 q-10,1.5 -20,0 q-12,-2 -20,0 Z"
        else:
            s_path=""

        #draw service line repeats
        for i in range(sl_repeats):
            dwg.add(dwg.path(d="M"+str(c_out[i])+" 260"+s_path, style="stroke:#143250;stroke-width:2; fill-opacity:0"))

        #draw internal function repeats
        if int_repeats:
            s_path = " l 10,-17.5 q10,1 20,0 q2.5,6 10,17.5 q-3.5,8 -10,17.5 q-7.5,-1 -20,0 q-2.5,-7.5 -10,-17.5"
            for i in range(int_repeats):       
                dwg.add(dwg.path(d="M"+str(c_out[i])+" 100"+s_path, style="stroke:#143250;stroke-width:2; fill-opacity:0", transform="rotate(10 "+str(c_out[i])+" 100)"))

        #Get google font and define for use
        dwg.embed_google_web_font(name="Amatic SC", uri='https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700')
        dwg.embed_stylesheet(""".amatic45 {font: 45px "Amatic SC"}""")
        paragraph = dwg.add(dwg.g(class_="amatic45", ))
        paragraph.add(dwg.text(name, insert=(100,215), style="fill:#FFFFFF;stroke:#000000;stroke-width:0.5", textLength="200", lengthAdjust="spacingAndGlyphs")) 
        dwg.save(pretty=True)
        
        #send svg to cloud convert api to return png
        #upload_job = cloudconvert.Job.create(payload={
        #    'tasks': {
        #        'upload-my-file': {
        #            'operation': 'import/upload'
        #        },
        #        'convert-my-file': {
        #            'operation': 'convert',
        #            'input': 'upload-my-file',
        #            'input_format': 'svg',
        #            'output_format': 'png',
        #            'engine': 'inkscape',
        #            'pixel_density': 300
        #        },
        #        'export-png': {
        #            'operation': 'export/url',
        #            'input': 'convert-my-file'
        #        }
        #    }
        #})
        
        #res = cloudconvert.Task.upload(file_name=my_filename, task=cloudconvert.Task.find(id=upload_job['tasks'][0]['id']))
        #resp = cloudconvert.Task.wait(id=upload_job['tasks'][2]['id'])
        #file = resp.get('result').get('files')[0]
        #download = cloudconvert.download(filename=file['filename'], url=file['url'])
        #png_filename = name+'.png'
        #download_button = pn.widgets.FileDownload(file=my_filename, sizing_mode='scale_width', max_width=400, align='center')
        
        return pn.Column(pn.pane.Markdown("""#### Take a look at your unique profile tile!"""), 
                         pn.pane.SVG(my_filename, width=400, height=400, align='center'), \
                          pn.layout.Divider(),\
                          pn.pane.Markdown(""" #### Decode your mosaic tile""", align='center'), \
                          pn.pane.PNG('assets/mosaic_tile_decoder.png', sizing_mode="scale_width", max_width=700, align='center'))

pipeline = pn.pipeline.Pipeline(ready_parameter='ready', debug=True)
pipeline.add_stage('Who are you?', AutoStart,  next_parameter='selected')
pipeline.add_stage("I consult with clients ONLY", ConsultantQuestions)
pipeline.add_stage("I have an internal role ONLY", InternalQuestions)
pipeline.add_stage("I consult AND have an internal role", HybridQuestions)
pipeline.add_stage("DrawSVG", DrawSVG)

pipeline.define_graph({'Who are you?':("I consult with clients ONLY", "I have an internal role ONLY", "I consult AND have an internal role"), 
                       "I consult with clients ONLY":'DrawSVG', 
                       "I have an internal role ONLY":'DrawSVG',
                       "I consult AND have an internal role":'DrawSVG'})

layout = pn.Column(pn.pane.Markdown(""" ### Tell us about yourself!""", sizing_mode="stretch_width"), \
                   pipeline.stage, pn.layout.VSpacer(), pn.layout.VSpacer(),\
                   pn.Row(pipeline.prev_button, pn.layout.HSpacer(), pipeline.next_button),align='center')

pn.template.FastListTemplate(
    title='Unify Community Mosaic', header_background="#143250", theme_toggle=False,
    main = ["Welcome to Unify Onboarding! We're excited that you've joined our firm. To get to know you a bit better, generate your own data mosaic tile below.",
            layout
           ], 
            main_max_width='1000px',
            sizing_mode="stretch_width", 
            logo="assets/unify_logo.png",
            favicon= "assets/favicon-32x32.png",
            accent_base_color="#1DC2BB").servable();