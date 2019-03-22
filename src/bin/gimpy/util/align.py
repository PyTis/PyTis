"""
The idea of this tool is to help align the input from a map, better to a grid.
Instead of changing the file, this will simply be used to change the
information about a map once it has been read.

Example.  XML tool reads map into an array, you would hand this tool that
array, and it would hand you back a similar array with things simply aligned
better.  Then if you want you can write a tool that re-writes your map as
xml with the array this tool gives back to you. :)

How does it work?  This tool takes in a list of dictionaries.
In each dictionary there must be a key called "coords."
coords is represented as a 4 element touple, x,y start x,y end.

    map_source = XMLGetter(file.map)
    aligner = Align(source=map_source)
    better_souce = aligner.newSouce(gride_size=10, grid_offset=0, xrange=3, yrange=3)

    For each element in the source,
        if the element's xstart is within the xrange,
            shift that element's x posisions to the closest gridline.
        if the element's ystart is within the yrange,
            shift that element's y posisions to the closest gridline.

"""

class Align(object):
    def Align(self, source):
        self.original_source = source

    def newSource(self, grid_size, grid_offset, xrange, yrange):
        pass