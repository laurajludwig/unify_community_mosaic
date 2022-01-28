import param 
import panel as pn
from panel.template.base import _base_config
import svgwrite
import cloudconvert
import os

pn.extension(sizing_mode='stretch_width')
API_KEY = os.environ.get('CLOUDCONVERT_API_KEY')
cloudconvert.configure(api_key = API_KEY, sandbox = False)
#cloudconvert.default()

live_dict = {"Seattle": "#1DC2BB",
               "San Francisco": "#143250",
               "Silicon Valley": "#2966A3",
               "Salt Lake": "#FF9233",
               "Chicago": "#C0D461",
               "Dallas": "#B72A33",
               "Dakotas": "#6E5577"}
role_dict = {"Seattle": "#1DC2BB",
             "San Francisco": "#143250",
             "Silicon Valley": "#2966A3",
             "Chicago": "#C0D461",
             "Dallas": "#B72A33",
             "National": "#FCED1E",
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
                "Power Apps": ["TE",9]}
inter_func_dict = {"People Team":1, 
                   "Talent Acquisition":2,
                   "Business Development": 3,
                   "Operations":4,
                   "Finance": 5,
                   "Brand/Marketing":6 ,
                   "Service Line Support": 7,
                   "Industry Vertical Support": 7,
                   "Practice Director": 8, 
                   "Practice Manager": 8, 
                   "Account Director": 9,
                   "Account Manager": 9,
                   "Industry Director": 10, 
                   "Industry Manager": 10, 
                   "Advocate Director":11}
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

class AutoStart(param.Parameterized):
    name_input = param.String(label= "My name is (first and last)")
    market_input = param.Selector(label="I live in", objects=list(live_dict.keys()))
    selected = param.Selector(objects=role_options)

    def panel(self):
        return pn.Column(pn.widgets.TextInput.from_param(self.param.name_input), pn.layout.VSpacer(), \
                         "I live in", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.market_input, button_type="success"), max_width=600, align='center'), pn.layout.Divider(), \
                         "Some Unifiers consult with their clients. Other Unifiers are internal and support our consultants (e.g., finance , operations, and people team). Then there are Unifiers who are hybrids and both consult as well as help shape the business (i.e., via leadership on practices, accounts, industries, or in an advocate role).",\
                         "Which one are you?", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.selected, button_type="success"), max_width=600, align='center'))

class ConsultantQuestions(AutoStart):
    client_input = param.Selector(objects=list(role_dict.keys())[:-2]+['Between engagements'])
    practice_input = param.Selector(objects=sorted(list(service_line_dict.keys())))
    industry_input = param.Selector( objects=list(industry_dict.keys())[:3])
    
    def panel(self):
        return pn.Column("My client work is in", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.client_input, button_type="success"), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "My primary practice is", pn.Row(pn.widgets.Select.from_param(self.param.practice_input, name=""),max_width=400, align='center'), pn.layout.VSpacer(), \
                         "If you specialize in one of our industry verticals, which one?", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.industry_input, button_type="success"), max_width=400, align='center'))
                         
    
    @param.output('result')
    def output(self):
        consult_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "client_market": self.client_input,
                       "practice_input": self.practice_input,
                       "industry_input": self.industry_input, 
                       "internal_role_input": "",
                       "internal_market_input": "", 
                       "internal_func_input": ""}
        return consult_dict

class InternalQuestions(AutoStart):
    internal_func_input = param.Selector(objects=list(inter_func_dict.keys())[:7])
    internal_market_input = param.Selector(objects=list(role_dict.keys())[:-1])
   
    def panel(self):    
        return pn.Column("As an internal Unifier, which internal function are you part of?", pn.Row(pn.widgets.Select.from_param(self.param.internal_func_input,name=""), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "I support ", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.internal_market_input, button_type="success"), max_width=600, align='center'))
    
    @param.output('result')
    def output(self):
        internal_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "client_market": "",
                       "practice_input": "",
                       "industry_input": "Neither", 
                       "internal_role_input": "",
                       "internal_market_input": self.internal_market_input, 
                       "internal_func_input": self.internal_func_input}
        return internal_dict

class HybridQuestions(AutoStart):
    client_input = param.Selector(objects=list(role_dict.keys())[:-2]+['Between engagements'])
    practice_input = param.Selector(objects=sorted(list(service_line_dict.keys())))
    industry_input = param.Selector(objects= list(industry_dict.keys())[:3])
    internal_func_input = param.Selector(objects=["None"]+list(inter_func_dict.keys())[:8])
    hybrid_role_input = param.ListSelector(objects=list(inter_func_dict.keys())[8:])
    internal_market_input = param.Selector(objects=list(role_dict.keys())[:-1])
    
    def panel(self): 
        return pn.Column("My client work is in", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.client_input, button_type="success"), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "My primary practice is", pn.Row(pn.widgets.Select.from_param(self.param.practice_input, name=""), max_width=600, align='center'), pn.layout.VSpacer(), \
                         "If you specialize in one of our industry verticals, which one?", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.industry_input, button_type="success"), max_width=400, align='center'), pn.layout.Divider(),\
                        "As an internal Unifier, which internal function are you part of?", pn.Row(pn.widgets.Select.from_param(self.param.internal_func_input, name=""), max_width=600, align='center'),
                        "As a consultant, I am also a ", pn.Row(pn.widgets.CheckButtonGroup.from_param(self.param.hybrid_role_input, button_type="success"),  align='center'),
                        "My internal role supports ", pn.Row(pn.widgets.RadioButtonGroup.from_param(self.param.internal_market_input, button_type="success"), max_width=600, align='center'))
    
    @param.output('result')
    def output(self):
        hybrid_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
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
            fill_op_list = [0.0, 0.0, 0.0, 0.0]
            if "Practice Director" in internal_role or "Practice Manager" in internal_role:
                fill_op_list[0] = 1.0
            if "Account Director" in internal_role or "Account Manager" in internal_role:
                fill_op_list[1] = 1.0 
            if "Industry Director" in internal_role or "Industry Manager" in internal_role:
                fill_op_list[2] = 1.0 
            if "Advocate Director" in internal_role:
                fill_op_list[3] = 1.0 

            for i in range(4):
                dwg.add(dwg.circle(center=(162.5+(i*25) ,150), r=10, style="fill:#143250; fill-opacity:"+str(fill_op_list[i])+";stroke:#143250;stroke-width:2"))

        if industry!="Neither" :
            dwg.add(dwg.line(start=(100,170), end=(300, 170), style="stroke:#143250;stroke-width:2;stroke-dasharray:"+str(industry_dict[industry])))
            dwg.add(dwg.line(start=(100,228), end=(300, 228), style="stroke:#143250;stroke-width:2;stroke-dasharray:"+str(industry_dict[industry])))

        #sequence for drawing center-out
        c_out = [178, 160, 196, 142, 214, 124, 232, 106, 250]

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
        dwg.embed_google_web_font(name="Amatic SC", uri='https://fonts.googleapis.com/css2?family=Amatic+SC')
        dwg.embed_stylesheet(""".amatic45 {font: 45px "Amatic SC"}""")
        paragraph = dwg.add(dwg.g(class_="amatic45", ))
        paragraph.add(dwg.text(name, insert=(200,200), text_anchor='middle', dominant_baseline='middle', style="fill:#FFFFFF" )) 
        dwg.save(pretty=True)
        
        #send svg to cloud convert api to return png
        upload_job = cloudconvert.Job.create(payload={
            'tasks': {
                'upload-my-file': {
                    'operation': 'import/upload'
                },
                'convert-my-file': {
                    'operation': 'convert',
                    'input': 'upload-my-file',
                    'input_format': 'svg',
                    'output_format': 'png',
                    'engine': 'inkscape',
                    'pixel_density': 300
                },
                'export-png': {
                    'operation': 'export/url',
                    'input': 'convert-my-file'
                }
            }
        })
        
        res = cloudconvert.Task.upload(file_name=my_filename, task=cloudconvert.Task.find(id=upload_job['tasks'][0]['id']))
        resp = cloudconvert.Task.wait(id=upload_job['tasks'][2]['id'])
        file = resp.get('result').get('files')[0]
        download = cloudconvert.download(filename=file['filename'], url=file['url'])
        png_filename = name+'.png'
        download_button = pn.widgets.FileDownload(file=png_filename, sizing_mode='scale_width', max_width=400, align='center')
        
        return pn.Column(pn.pane.SVG(my_filename, width=400, height=400, align='center'), download_button, \
                      pn.layout.VSpacer(),\
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
