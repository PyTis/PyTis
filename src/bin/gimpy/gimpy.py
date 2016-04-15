#!/usr/bin/python2.4
"""

NAME
    gimPy

SYNOPSIS
    gimpy   [ -i argument ] [ -d argument ] [ -o argument ] [ -h ]
            [ --fontname argument ] [ --fontsize argument]

DESCRIPTION
    This tool uses python2.4  It creates report.py files.

    The input is the dpi of an image, the image and an image map
    (using the image name).

    The image map name is assumed. 'test.jpg' would look for 'test.csim' so
    make sure the maps are placed in the same path.

    Likewise the actual name of these report files is assumed.  The name
    of the image is used, then a .py file extensionis applied.

    When ran, using python and reportlab, these report.py files create PDF
    reports.

    The PDF Generator creates complete python files that can be used to
    generate that pdf.

USEAGE

    -i,--image
        Can be either a sigle image file, including the absolute path
        to that image, or a path and image extention.
            i.e "/home/john/test.jpg"
            or
            i.e. "/home/john/*.jpg"

    -d, --dpi
        dpi of image you are passing in.  Make sure you specify the dpi before
        the image.  Multiple images with multiple dpi settings can be input at
        once.  Therefore the dpi last input is applied to all images input
        there-after, until a different dpi setting is input.
            i.e.
            ./gimpy -d 600 -i test.jpg -d 300 -i /home/*.jpg

    -o, --outdir
        This only needs to be specified once.  This is the directory where the
        reports created should be placed.

    --fontsize
        Default font size in points. 12pt would be: --fontsize 12

    --fontname
        Default font family.  Make sure that it is a font family compliant with
        Report Lab and PDFs. Arial and Verdana are not.

EXAMPLE
    gimpy.py -d 600 -i /home/foo/*.jpg -d 300 /home/foo/*.png -o /home/myname/myproject

    The report files that are created can also be ran in 'test' mode by running
    them by themselves.  In this case, they use a default dict with the word "Test"
    as the value for everything.


EXAMPLE MAP FILE:

    <img src="test.jpg" width="420" height="256" border="0" usemap="#map" />
    <map name="map">
    <!-- #$-:Image Map file created by GIMP Imagemap Plugin -->
    <!-- #$-:GIMP Imagemap Plugin by Maurits Rijk -->
    <!-- #$-:Please do not edit lines starting with "#$" -->
    <!-- #$VERSION:2.0 -->
    <!-- #$AUTHOR:jlee -->
    <area shape="rect" coords="30,46,150,64""
        href="client_name" />
    <area shape="rect" coords="30,82,135,100" target="Verdana, 10"
        href="medicaide_no" />
    </map>


GIMP HELP:
    1. Canvas Size
        4.25 w - 5.5 h inches (gets a smaller file size)
        Click center button
    2. Scale
        300 px dpi
        5.5 inch  height
        ? width (whatever it tells you the width becomes
    3. Layor to Image
    4. Save as .png (smaller file size)

    5. Filters > Web > ImageMap
    6. ImageMap Mapping > Edit Map Info > Type = "CSIM"
        Use Rectangles Only

        href = entity
        coords = xstart, ystart, xend, yend
        target = font, fontsize

EXAMPLE USEAGE:
    DPI is VERY IMPORTANT!  Make sure you specifiy it.

    # Our canvas was half the size of a real page,
    # so we cut our canvas's dpi in half
    # DPI is required becuase gimp stores the image map
    # areas location in pixels.
    ./gimpy.py --dpi 150 --image report.jpg --outdir /foo
    # Generates /foo/report.py


    Single page
        from foo.report import report
        client = dict()
        x = report(ds=client)
        # Render closes the current (only) page
        # Then render saves the report as a temp file by calling the built in
        # canvas.save()
        x.render()

    OR multiple pages

        from foo.report import report
        canvas = canvas.Canvas(file_name, #(destination_file)
                    pagesize=(72 * 8.5, # page width
                        72 * 11) # page height
                    )
        for client in clients:
            x = new report(ds=client,my_canvas=canvas,file_name='ClientReport.pdf')
            canvas = x.draw()
        canvas.save()

LICENCE
    GPL

COPYRIGHT
    (c)2006 Zertis Technologies, LLC

AUTHOR
    jlee@zertis.net
"""

import glob, os, sys

from util.MapToPython import *

def show_help():
    print __doc__
    sys.exit(0)

def grab_input():

    get_dpi = False
    get_fontname = False
    get_fontsize = False
    get_image = False
    get_out_dir = False

    dpi = 150
    fontname = None
    fontsize = None
    images = []
    out_dir = None
    if len(sys.argv) < 2:
        show_help()
    for item in sys.argv:
        if 'gimpy.py' in item or 'bin/gimpy' in item:
            pass
        # Grabbing
        elif get_dpi == True:
            get_dpi = False # Reset
            dpi = item
        elif get_out_dir == True:
            get_out_dir = False
            out_dir = item
        elif get_image == True:
            get_image = False
            images.append((item,dpi))
        elif get_fontname == True:
            get_fontname = False
            fontname = item
        elif get_fontsize == True:
            get_fontsize = False
            fontsize = item
        # Test
        elif item == '--dpi' or item == '-d':
            # Next time through, we will grap the item as dpi
            get_dpi = True
        elif item == '-h' or item == '--help':
            show_help()
        elif item == '-i' or item == '--image':
            get_image = True
        elif item == '--fontname':
            get_fontname = True
        elif item == '--fontsize':
            get_fontsize = True
        elif item == '--outdir' or item == '-o':
            # Next time through, we will grap the item as out_dir
            get_out_dir = True
        else:
            print "%s is not a valid argument." % item
            show_help()
    return images, out_dir, fontname, fontsize

def make_report(image, out_dir=None, dpi=150, fontname=None, fontsize=None):
    if out_dir is None:
        out_dir = os.path.dirname(os.curdir)
    out_dir = os.path.abspath(out_dir)

    image_file = os.path.basename(image)
    image_name = os.path.splitext(image_file)[0]

    map_file = os.path.abspath(os.path.join(os.path.dirname(image), '%s.csim' % image_name))
    source = get_xml_from_file(map_file)
    maps = process_xml(source)
    source = maps[0]
    MapToPython(path=os.path.abspath(out_dir),
                   my_name=image_name,
                   map_source=source,
                   img_source=image_source(os.path.abspath(image)),
                   dpi=dpi,
                   fontname=fontname,
                   fontsize=fontsize
                   )

def run(items, out_dir, fontname, fontsize):
    """
    Run program on each image gathered from the input.
    items is a 2 element touple,
        image_file and dpi
        i.e. ("/home/john/test.jpg, 150)
            or
        image_path and dpi
        i.e. ("/home/john/*.jpg, 150)
    out_dir can be none.
    """
    for item in items:
        image = item[0]
        dpi = item[1]
        if os.path.isfile(image):
            try:
                assert os.path.isfile(image) == True
            except AssertionError:
                print "%s is not a valid image file." % image
                sys.exit(0)
            else:
                make_report(image, out_dir, dpi, fontname, fontsize)
        else:
            its = [(os.path.abspath(i),dpi)for i in glob.glob(image) if os.path.isfile(i)]
            run(its, out_dir, fontname, fontsize)

run(*grab_input())
