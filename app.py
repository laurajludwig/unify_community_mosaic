import param 
import panel as pn
from panel.template.base import _base_config
import svgwrite
import cairosvg
import os

pn.extension(sizing_mode='stretch_width')
css="""@import url("//fonts.googleapis.com/css?family=Amatic+SC")"""
config=_base_config(raw_css=[css])

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

        my_filename = name+'.png'
        dwg = svgwrite.Drawing(size=(400, 400), profile='full')
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
        dwg.defs.add(dwg.style('@font-face { font-family: "Amatic SC"; src: url(data:application/font-woff;charset=utf-8;base64, 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) format("woff2");} text { font-size: 45px; font-family: "Amatic SC", cursive; font-weight: 400;}   '))
        #dwg.embed_google_web_font(name="Amatic SC", uri='https://fonts.googleapis.com/css2?family=Amatic+SC')
        #dwg.embed_stylesheet(""".amatic45 {font: 45px "Amatic SC"}""")
        #paragraph = dwg.add(dwg.g(class_="amatic45", ))
        dwg.add(dwg.text(name, insert=(200,200), text_anchor='middle', dominant_baseline='middle', font_family='Amatic SC', font_size=45, style="fill:#FFFFFF" )) 
        cairosvg.svg2png(dwg.tostring(), write_to=my_filename)
        download_button = pn.widgets.FileDownload(file=my_filename, sizing_mode='scale_width', max_width=400, align='center')
        
        return pn.Column(pn.pane.PNG(my_filename, width=400, height=400, align='center'), download_button, \
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
            accent_base_color="#1DC2BB",
            config=config).servable();