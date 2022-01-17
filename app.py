import panel as pn
import svgwrite
import param
import os

pn.extension(sizing_mode="stretch_width")

market_dict = {"SEA": "#ADCCEA",
               "SF": "#FCED1E",
               "SV": "#C0D461",
               "CHI": "#DF747B",
               "DAL": "#FF9233",
               "SLC": "#5B98D6",
               "SD":"#FFBE85"}
direction_dict = {"North": 0,
                  "East": 90,
                  "South": 180,
                  "West": 270}
think_dict = {"Write/draw on paper": "paper", 
                  "Write/draw digitally":"digital",
                  "Talk": "talk", 
                  "Move": "move"}

class Generate(param.Parameterized):
    enter_button = param.Action(lambda x: x.param.trigger('enter_button'), label='Generate my portrait')
    reset_button = param.Action(lambda y: y.param.trigger('reset_button'), label='Reset form')
    
    data_entered = False
    
    @param.depends('enter_button', watch=True)
    def gather_data(self):
        self.data_entered = True
        
    @param.depends('reset_button', watch=True)
    def reset_form(self):
        os.remove('badge.svg')
        self.data_entered = False
        name_input.value = ""
        market_input.value = "SEA"
        direction_input.value = "North"
        pronounce_input.value = '\"day-ta"'
        role_input.value = "Analyst"
        think_input.value = "Write/draw on paper"
            
    @param.depends('data_entered', watch=True)
    def update_svg(self):
        if self.data_entered:
            #get and clean values from inputs 
            name = name_input.value 
            market = market_input.value
            direction = direction_input.value
            pronounce1 = pronounce_input.value
            role = role_input.value
            think1 = think_input.value

            if pronounce1=='\"day-ta"':
                pronounce="dayta"
            else:
                pronounce="dahta"
            think = think_dict[think1]
            dwg = svgwrite.Drawing('badge.svg', size=(300, 300), profile='full')

            #set a background shape
            dwg.add(dwg.rect(insert=(0,0), size=(300,300), fill="#143250"))

            #Build and add texture based on role type selected
            pattern = dwg.defs.add(dwg.pattern(insert=(0, 0), size=(5, 5), patternUnits="userSpaceOnUse"))
            if role=="Designer":
                pattern.add(dwg.circle(center=(2.5, 2.5),r=1, style="fill:#E6E6E6"))
            elif role=="Consultant":
                pattern.add(dwg.line(start=(0,0), end=(5,0), style="stroke:#E6E6E6; stroke-width:3"))
            elif role=="Analyst":
                pattern.add(dwg.line(start=(0,0), end=(5,0), style="stroke:#E6E6E6; stroke-width:3"))
                pattern.add(dwg.line(start=(0,0), end=(0,5), style="stroke:#E6E6E6; stroke-width:3"))               
            dwg.add(dwg.ellipse(center=(0,0), r=(180, 240), fill=pattern.get_paint_server()))

            if pronounce=="dayta":
                dwg.add(dwg.ellipse(center=(0,0), r=(180, 240), style="fill:none;stroke:#1DC2BB;stroke-width:6"))
                dwg.add(dwg.ellipse(center=(0,0), r=(192, 252), style="fill:none;stroke:#1DC2BB;stroke-width:6"))
            else: 
                dwg.add(dwg.ellipse(center=(0,0), r=(180, 240), style="fill:none;stroke:#1DC2BB;stroke-width:12"))

            #Build and add compass shape for geography
            dwg.add(dwg.path(d="M180 165 L222 207 L264 165 L222 99 Z", style="fill:"+market_dict[market], 
                             transform="rotate("+str(direction_dict[direction])+" 222 153)"))

            #Build and add bars for thinking question
            if think=="paper":
                for i in range(4):
                    dwg.add(dwg.line(start=(30+(i*24),300), end=(30+(i*24), 165),  style="fill:none;stroke:#9BF0EC;stroke-width:18"))
            elif think=="digital":
                for i in range(2):
                    dwg.add(dwg.line(start=(30+(i*24),300), end=(30+(i*24), 165),  style="fill:none;stroke:#9BF0EC;stroke-width:18"))
            elif think=="talk":
                for i in range(4):
                    dwg.add(dwg.line(start=(0, 270-(i*24)), end=(135, 270-(i*24)),  style="fill:none;stroke:#9BF0EC;stroke-width:18"))
            elif think=="move":
                for i in range(2):
                    dwg.add(dwg.line(start=(0, 270-(i*24)), end=(135, 270-(i*24)),  style="fill:none;stroke:#9BF0EC;stroke-width:18"))

            #Get google font and define for use
            dwg.embed_google_web_font(name="Amatic SC", uri='https://fonts.googleapis.com/css2?family=Amatic+SC')
            dwg.embed_stylesheet(""".amatic36 {font: 36px "Amatic SC"}""")
            paragraph = dwg.add(dwg.g(class_="amatic36", ))
            paragraph.add(dwg.text(name, insert=(150,240), style="fill:#E6E6E6", textLength="144", lengthAdjust="spacingAndGlyphs"))
            dwg.save(pretty=True)
            return pn.pane.SVG('badge.svg', width=300, height=300)
        else:
            return ""

#widgets
name_input = pn.widgets.TextInput(name='My name is:')
market_input = pn.widgets.DiscreteSlider(name='I\'m based in', options=['SEA','SF','SV','CHI','DAL','SLC','SD'])
direction_input = pn.widgets.RadioBoxGroup(name='To get to my market\'s office, I would travel: ', options=['North', 'South', 'East', 'West'], inline=True)
pronounce_input = pn.widgets.RadioBoxGroup(name='I pronounce it', options=['\"day-ta"', '\"dah-ta"'], inline=True)
role_input = pn.widgets.RadioBoxGroup(name='First and foremost, I consider myself a(n):', options=['Analyst', 'Consultant', 'Designer'], inline=True)
think_input = pn.widgets.RadioBoxGroup(name='When I think, I: ', options=['Write/draw on paper', 'Write/draw digitally', 'Talk', 'Move'], inline=True)

svg_pane = Generate()
svg_pane.reset_form
download_button = pn.widgets.FileDownload(file='badge.svg')


layout = pn.Row(pn.Column(name_input, 
                          'An important question: \"day-ta" or \"dah-ta">?', pronounce_input,
                          market_input, 
                          'To get to my market\'s office, I would travel:', direction_input,
                          'First and foremost, I consider myself a(n):', role_input, 
                          'When I think, I: ',think_input, 
                          pn.panel(svg_pane.param, show_name=False)),
                pn.Column(svg_pane.update_svg,  
                          download_button))

pn.template.FastListTemplate(
    title='Unify Data Analysis & Visualization Data Portait Builder', header_background="#143250", theme_toggle=False,
    main = ["Welcome to DA&V at Unify! We're excited that you've joined the team. To get to know you a bit better, generate your own data portrait below. We share these on our internal SharePoint site, so we can all get to know each other and how each of us works best. Please donwload a copy of your data portrait and share the file with your Practice Manager or greeter.",
            layout,
           ],main_max_width='900px',
            accent_base_color="#1DC2BB").servable();