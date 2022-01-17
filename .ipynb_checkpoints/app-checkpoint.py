import param 
import panel as pn
import svgwrite
import os

css1 = '''
.bk.panel-button-group {
    background-color: #EDEDED; 
    border-color: #E0E0E0;
    }
.bk.panel-button-group:active {
    background-color:#BBECEA;
    border-color: #1DC2BB;
}
'''

css= '''
.bk-root .bk-input-group{{
    --accent-fill-hover: {#BBECEA};
    --accent-fill-active: {#BBECEA};
}}'''


pn.extension(raw_css=[css])

live_dict = {"Seattle": "#1DC2BB",
               "San Francisco": "#143250",
               "Silicon Valley": "#2966A3",
               "Salt Lake": "#FF9233",
               "Chicago": "#C0D461",
               "Dallas": "#B72A33",
               "Dakotas": "#FCED1E"}
role_dict = {"Seattle": "#1DC2BB",
               "San Francisco": "#143250",
               "Silicon Valley": "#FF9233",
               "Chicago": "#C0D461",
               "Dallas": "#B72A33",
               "National": "#FCED1E"}
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
                   "Service Line/Industry Leader": 7 }
role_options = ['I consult with clients', 'I have an internal role', 'I consult AND have an internal role']

class AutoStart(param.Parameterized):
    name_input = param.String(label= "My name is")
    market_input = param.Selector(label="I live in", objects=list(live_dict.keys()))
    selected = param.Selector(objects=role_options)

    def panel(self):
        return pn.Column(pn.widgets.TextInput.from_param(self.param.name_input), pn.layout.VSpacer(), \
                         "I live in", pn.widgets.RadioButtonGroup.from_param(self.param.market_input, css_classes=['bk-input-group']), pn.layout.VSpacer(), \
                         "At Unify,", pn.widgets.RadioButtonGroup.from_param(self.param.selected))
   
class ConsultantQuestions(AutoStart):
    client_input = param.Selector(objects=list(role_dict.keys()))
    practice_input = param.Selector(objects=list(service_line_dict.keys()))
    
    def panel(self):
        return pn.Column("My client work is in", pn.widgets.RadioButtonGroup.from_param(self.param.client_input), pn.layout.VSpacer(), \
                         "My primary practice is", pn.widgets.Select.from_param(self.param.practice_input, name=""))
    
    @param.output('result')
    def output(self):
        consult_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "client_market": self.client_input,
                       "practice_input": self.practice_input,
                       "internal_role_input": "",
                       "internal_market_input": "", 
                       "internal_func_input": ""}
        return consult_dict

class InternalQuestions(AutoStart):
    internal_func_input = param.Selector(objects=list(inter_func_dict.keys()))
    internal_market_input = param.Selector(objects=list(role_dict.keys()))
   
    def panel(self):    
        return pn.Column("My main function is", pn.widgets.Select.from_param(self.param.internal_func_input), pn.layout.VSpacer(), \
                         "I support: ", pn.widgets.RadioButtonGroup.from_param(self.param.internal_market_input))
    
    @param.output('result')
    def output(self):
        internal_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "client_market": "",
                       "practice_input": "",
                       "internal_role_input": "",
                       "internal_market_input": self.internal_market_input, 
                       "internal_func_input": self.internal_func_input}
        return internal_dict

class HybridQuestions(AutoStart):
    client_input = param.Selector(objects=list(role_dict.keys()))
    practice_input = param.Selector(objects=list(service_line_dict.keys()))
    hybrid_role_input = param.Selector(objects=['Practice Leadership', 'Account Leadership', 'Industry Leadership', 'Advocacy'])
    internal_market_input = param.Selector(objects=list(role_dict.keys()))
    
    def panel(self): 
        return pn.Column("My client work is in", pn.widgets.RadioButtonGroup.from_param(self.param.client_input), pn.layout.VSpacer(), \
                         "My primary practice is", pn.widgets.Select.from_param(self.param.practice_input, name=""), pn.layout.VSpacer(), \
                         "I mainly serve in ", pn.widgets.RadioButtonGroup.from_param(self.param.hybrid_role_input), pn.layout.VSpacer(), \
                         "I support ", pn.widgets.RadioButtonGroup.from_param(self.param.internal_market_input))
    
    @param.output('result')
    def output(self):
        hybrid_dict = {"name_input": self.name_input,
                       "live_input": self.market_input,
                       "client_market": self.client_input,
                       "practice_input": self.practice_input,
                       "internal_role_input": self.hybrid_role_input,
                       "internal_market_input": self.internal_market_input, 
                       "internal_func_input": "" }
        return hybrid_dict

class DrawSVG1(AutoStart):
    result = param.Dict()
    
    def panel(self):
        name = self.result['name_input']
        client_market_val = self.result['client_market']
        #client_col = role_dict['client_market]
        return pn.Column(client_market_val)
    
class DrawSVG(AutoStart):
    result = param.Dict()
    
    def panel(self):
        #get and clean values from inputs 
        name = self.result['name_input']
        live_market = self.result['live_input']
        client_market = self.result['client_market']
        practice = self.result['practice_input']
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
            internal_func = None           

        my_filename = name+'.svg'
        dwg = svgwrite.Drawing(my_filename, size=(400, 400), profile='full')
        dwg.add(dwg.rect(insert=(0,0), size=(400,400), fill=live_dict[live_market]))
        dwg.add(dwg.circle(center=(200,200), r=190, fill="#FFFFFF"))

        #consulting glyph
        if client_market:
            dwg.add(dwg.path(d="M16,200 q124,-60 184,-184 q60,124 184,184 q-124,60 -184,184 q-60,-124 -184,-184 Z", style="fill:"+role_dict[client_market]+";fill-opacity:0.6"))

        #internal role glyph
        if internal_role=="Practice Leadership":
            int_str_col = "#45E3DB"
        elif internal_role == "Account Leadership":
            int_str_col == "#FF9233"
        elif internal_role == "Industry Leadership":
            int_str_col = "#FCEF39"
        elif internal_role=="Advocacy":
            int_str_col = "#D1333E"
        else:
            int_str_col = "#FFFFFF"

        if internal_role:
            dwg.add(dwg.path(d="M16,200 q124,-60 184,-184 q60,124 184,184 q-124,60 -184,184 q-60,-124 -184,-184 Z", \
                             style="fill:"+role_dict[internal_market]+";fill-opacity:0.6;stroke:"+int_str_col, \
                             transform="rotate(45 200 200)"))

        # get the shape path for service line
        if service_line=="DDI":
            s_path = " a40,40 0 0,1 80,0  a42,41 0 0,1 -40,40 a39,35 0 0,1 -38,-42"
        elif service_line == "BA":
            s_path = " q10,-15 40,-40 q40,35 40,40 q-25,35 -40,40 q-15,-20 -40,-40 Z"
        elif service_line == "TE":
            s_path = " m0,40 q35,-60 40,-80 q10,12 40,80 q-20,3 -40,0 q-24,-4 -40,0 Z"
        else:
            s_path=""

        #draw service line repeats
        if service_line:
            for i in range(sl_repeats):
                if i<5:
                    path = "M"+str(50+(i*27.5))+" "+str(260+(i*20))
                else: 
                    path = "M"+str(50+(i*27.5))+" "+str(340-((i-4)*20))
                dwg.add(dwg.path(d=path+s_path, style="stroke:#143250;stroke-width:2; fill-opacity:0"))


        #draw internal function repeats
        if internal_func:
            s_path = " l 20,-35 q20,2 40,0 q5,12 20,35 q-7,16 -20,35 q-15,-2 -40,0 q-5,-15 -20,-35"
            for i in range(int_repeats):       
                path = "M"+str(60+(i*35))+" 100"
                dwg.add(dwg.path(d=path+s_path, style="stroke:#143250;stroke-width:2; fill-opacity:0", transform="rotate(10 "+str(100+(i*35))+" 100)"))

        #Get google font and define for use
        dwg.embed_google_web_font(name="Amatic SC", uri='https://fonts.googleapis.com/css2?family=Amatic+SC')
        dwg.embed_stylesheet(""".amatic45 {font: 45px "Amatic SC"}""")
        paragraph = dwg.add(dwg.g(class_="amatic45", ))
        paragraph.add(dwg.text(name, insert=(100,215), style="fill:#FFFFFF", textLength="200", lengthAdjust="spacingAndGlyphs"))
        dwg.save(pretty=True)    
        download_button = pn.widgets.FileDownload(file=my_filename)
        
        return pn.Column(pn.pane.SVG(my_filename, width=400, height=400), download_button)

        
        #return pn.Column(self.result.keys())

pipeline = pn.pipeline.Pipeline(ready_parameter='ready', debug=True)
pipeline.add_stage('Who are you?', AutoStart,  next_parameter='selected')
pipeline.add_stage("I consult with clients", ConsultantQuestions)
pipeline.add_stage("I have an internal role", InternalQuestions)
pipeline.add_stage("I consult AND have an internal role", HybridQuestions)
pipeline.add_stage("DrawSVG", DrawSVG)

pipeline.define_graph({'Who are you?':("I consult with clients", "I have an internal role", "I consult AND have an internal role"), 
                       "I consult with clients":'DrawSVG', 
                       "I have an internal role":'DrawSVG',
                       "I consult AND have an internal role":'DrawSVG'})



layout = pn.Column(pn.pane.Markdown(""" ### Tell us about yourself, Newnifier!"""), \
                   pipeline.stage, pn.layout.VSpacer(), pn.layout.VSpacer(),\
                   pn.Row(pipeline.prev_button, pn.layout.HSpacer(), pipeline.next_button),)

pn.template.FastListTemplate(
    title='Unify Community Mosaic', header_background="#143250", theme_toggle=False,
    main = ["Welcome to Unify Onboarding! We're excited that you've joined our firm. To get to know you a bit better, generate your own data mosaic tile below.",
            layout,
           ],main_max_width='1200px',
            accent_base_color="#1DC2BB").servable();