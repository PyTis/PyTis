"""
This tool in an extention of the built in HTMLParser and is used for parsing
image maps represented in XML Format.
The three tags that it cares about are:
    img, map, and area

A normal file would be in order, similarly to.

    <image />
    <map>
        <areas />
        <areas />
    </map

Because someone could pass in many maps at once, or a corrupt file the "Map"
simply doesn't get added to the maps list until if finds the map close tag
is found by the parser.


Usage is simple:

    hp = MapHTMLParser()
    [hp.feed(line) for line in source]
    maps = hp.getMaps()

    m = maps[0] # if (and in most cases) only one map was fed in
    map = m['map']
    # map would contain the map tag's attributes, represented as a dictionary
    image = m['image']
    # image would contain the img tag's attributes, represented as a dictionary
    areas = m['areas']
    # areas would contain a list of dictionaries that represent each area tag
    # located in the map.

"""

from HTMLParser import HTMLParser

class MapHTMLParser(HTMLParser):
    current_map = {}
    current_image = {}
    current_areas = []
    maps = []

    def convertAttrs(self, attrs):
        d = {}
        for i in attrs: d[i[0]] = i[1]
        return d

    def handle_starttag(self, tag, attrs):
        if tag == 'img': self.handleImage(tag, attrs)
        if tag == 'map': self.handleMap(tag, attrs)
        if tag == 'area': self.handleArea(tag, attrs)
        return True

    def handle_endtag(self, tag):
        if tag == 'map':
            self.closeMap()
        return True

    def handleImage(self, tag, attrs):
        self.current_image = self.convertAttrs(attrs)
        return True

    def handleMap(self, tag, attrs):
        self.current_map = self.convertAttrs(attrs)
        return True

    def handleArea(self, tag, attrs):
        self.current_areas.append(self.convertAttrs(attrs))
        return True

    def closeMap(self):
        map = {
               'areas' : self.current_areas,
               'image' : self.current_image,
               'map' : self.current_map
               }
        self.maps.append(map)
        self.current_areas = []
        self.current_image = {}
        self.current_map = {}
        return True

    def getMaps(self):
        return self.maps