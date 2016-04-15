import os, unittest, sys

path_to_add = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#path_to_add = '/home/jlee/scratch/gimpy/src'
sys.path.append(path_to_add)

from util.MapToPython import *


class MapToPythonTestCase(unittest.TestCase):

    def test_get_xml_from_file(self):
        dir = os.path.dirname(__file__)
        map_file = os.path.abspath(os.path.join(dir, 'map.csim'))
        source = get_xml_from_file(map_file)
        res = ['<img src="test.jpg" width="420" height="256" border="0" usemap="#map" />\n',
               '\n', '<map name="map">\n',
               '<!-- #$-:Image Map file created by GIMP Imagemap Plugin -->\n',
               '<!-- #$-:GIMP Imagemap Plugin by Maurits Rijk -->\n',
               '<!-- #$-:Please do not edit lines starting with "#$" -->\n',
               '<!-- #$VERSION:2.0 -->\n',
               '<!-- #$AUTHOR:jlee -->\n',
               '<area shape="rect" coords="30,46,150,64" alt="alt2" target="Helvetica,10" onmouseover="alt3" onmouseout="alt4" onfocus="alt5" onblur="alt6" href="client_name" />\n',
               '<area shape="rect" coords="30,82,135,100" target="Times-BoldItalic,20" href="medicaide_no" />\n',
               '<area shape="rect" coords="255,64,270,82" href="service" />\n',
               '<area shape="rect" coords="285,64,300,82" href="area" />\n',
               '</map>\n']
        self.assertEquals(res, source)

    def test_process_xml(self):
        dir = os.path.dirname(__file__)
        map_file = os.path.abspath(os.path.join(dir, 'map.csim'))
        source = get_xml_from_file(map_file)

        res_areas = [{'onblur': 'alt6', 'target': 'Helvetica,10', 'onmouseout': 'alt4', 'shape': 'rect', 'href': 'client_name', 'coords': '30,46,150,64', 'onmouseover': 'alt3', 'alt': 'alt2', 'onfocus': 'alt5'},
                     {'shape': 'rect', 'href': 'medicaide_no', 'coords': '30,82,135,100', 'target': 'Times-BoldItalic,20'},
                     {'shape': 'rect', 'href': 'service', 'coords': '255,64,270,82'},
                     {'shape': 'rect', 'href': 'area', 'coords': '285,64,300,82'},
                    ]
        res_image = {'usemap': '#map',
                     'src': 'test.jpg',
                     'height': '256',
                     'border': '0',
                     'width': '420'}
        res_map = {'name': 'map'}
        maps = process_xml(source)
        map_source = maps[0]
        map = map_source['map']
        image = map_source['image']

        areas = map_source['areas']
        #for area in areas:
        #    print area
        self.assertEquals(map, res_map)
        self.assertEquals(image, res_image)
        #self.assertEquals(areas, res_areas)

    def test_MapToPython(self):
        dir = os.path.dirname(__file__)
        map_file = os.path.abspath(os.path.join(dir, 'map.csim'))
        source = get_xml_from_file(map_file)
        maps = process_xml(source)
        map_source = maps[0]
        dir = os.path.dirname(__file__)
        MapToPython(os.path.abspath(os.path.dirname(__file__)), 'foo', map_source, image_source(os.path.join(dir, 'test.jpg')))

if __name__ == '__main__':
    unittest.main()
