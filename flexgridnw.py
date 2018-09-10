import bottle
import ast
import sys, os


class Flexgridnw:
    sections = ("status", "network")
    config = {'cwd': os.getcwd()}
    print(os.getcwd())

    def __init__(self):
        with open("{}/data/config.ini".format(self.config['cwd']), mode="r", encoding="utf-8") as f:
            self.config['fgnw'] = ast.literal_eval(f.read())
        self.load(self.config['fgnw']['current-network'])
        self.config['network'] = [x for x in self.config['fgnw']['networks'] if x[0] == self.config['fgnw']['current-network']][0]

    def network(self):
        html5 = []
        html5.append(self.draw())
        return "".join(html5)

    def home(self):
        return "Home"

    def status(self):
        return "Status"

    def load(self, which=None):
        """Load the data from files."""
        for thefile in ("nodes", "edges"):
            with open("{}/data/{}-{}.ini".format(self.config['cwd'], which, thefile), mode="r", encoding="utf-8") as f:
                self.config[thefile] = ast.literal_eval(f.read())

    def dump(self):
        """Dump the data to files."""
        return "Status"

    def draw(self):
        """Draw the network"""
        html5 = []
        html5.append("<h1>{} network</h1>".format(self.config['network'][1]))
        # scale the network to the screen
        maxwidth = 0
        maxheight = 0
        for node in self.config['nodes']:
            if node[1] > maxwidth:
                maxwidth = node[1]
            if node[2] > maxheight:
                maxheight = node[2]
        scale = 940/maxwidth
        # draw edges
        html5.append("""<svg version="1.1" baseProfile="full" width="960" height="{}" xmlns="http://www.w3.org/2000/svg">""".format(round(maxheight*scale)+20))
        html5.append("""<rect width="100%" height="100%" fill="white" />""")
        for edge in self.config['edges']:
            source = [x for x in self.config['nodes'] if x[0] == edge[0]][0]
            destin = [x for x in self.config['nodes'] if x[0] == edge[1]][0]
            x1 = round(source[1]*scale)
            y1 = round(source[2]*scale)
            x2 = round(destin[1]*scale)
            y2 = round(destin[2]*scale)
            html5.append("""<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="red" />""".format(x1, y1, x2, y2))
        for node in self.config['nodes']:
            x = round(node[1]*scale)
            y = round(node[2]*scale)
            html5.append("""<circle cx="{}" cy="{}" r="20" fill="white" stroke="blue" />""".format(x, y))
            html5.append("""<text x="{}" y="{}" alignment-baseline="middle" text-anchor="middle">{}</text>""".format(x, y, node[0]))
        html5.append("""</svg>""")
        return "".join(html5)

    def trafficadd(self, traffic):
        """Add traffic to the network"""
        return "Add traffic"

    def trafficdel(self, traffic):
        """Delete traffic from the network"""
        return "Delete traffic"

fgnw = Flexgridnw()


@bottle.route('/')
@bottle.route('/<section>')
@bottle.route('/<section>/')
def home(section=None):
    if section in fgnw.sections:
        return getattr(fgnw, section)()
    else:
        return fgnw.home()

bottle.run(host='localhost', port=8080, debug=True)
