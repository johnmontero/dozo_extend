# -*- coding: utf-8 -*-
import io
import os
import datetime
import logging

import yaml
from PIL import Image, ImageDraw, ImageFont

from dozo.config    import get_config_value
from dozo.commands  import BaseCommand, CommandError

logging.basicConfig(
        format='%(asctime)-15s - %(levelname)-4s : %(message)s',
        level=logging.INFO
    )

log = logging.getLogger('compose')

isFILE = (lambda filename: os.path.isfile(filename))


class Command(BaseCommand):
    """
    Compose a image use PIL.
    """
    
    # command information
    usage = '--compose filename'
    summary = __doc__.strip().splitlines()[0].rstrip('.')

 
    def get_settings(self, filename):
        """ Read file settings 
        """
        with io.open(filename) as f:
            settings = yaml.load(f)

        return settings

    def handle(self):
        """ 
        """
        filename = self.args.get_value('--compose')
        if filename is None:
            print "Please use option:"
            print "   dozo %s" % self.usage
            return
        
        log.info("=== Starting composition ===")
     
        if not isFILE(filename):
            raise CommandError("\n{0} not exist.\n".format(filename))
       
        settings = self.get_settings(filename)

        for key in ["left-margin", "font", "centering", "background", "text" ,"output-file"]:
            if key not in settings.keys():
                raise CommandError("\n{0} does not exist.\n".format(key))

        fimage = "{0}/{1}".format(  settings["background"]["path"],
                                    unicode(settings["background"]["image"],"utf-8") )

        if not isFILE(fimage):
            raise CommandError("\n{0} not exist.\n".format(fimage))
       
        
        ffont = "{0}/{1}".format(  settings["font"]["path"],
                                   settings["font"]["name"] )

        if not isFILE(ffont):
            raise CommandError("\n{0} not exist.\n".format(ffont))

       
        sizefont = settings["font"]["size"]
        font = ImageFont.truetype(ffont, sizefont, encoding='unic')
        
        leftrow = settings["left-margin"]["row"]
        leftcol = settings["left-margin"]["column"]
        spacing = settings["font"]["spacing"]

        im = Image.open(fimage)
        draw = ImageDraw.Draw(im)
        W, H = im.size
        
        for (col, row, text, align, fill) in settings["text"]:  
            if align == "C":    
                #w, h = draw.textsize(unicode(text,'utf-8'))
                #col = ((W-100)-w)/2
                pass
            else:
                col = col+leftcol

            draw.text( (col,(row*spacing)+leftrow), text, font=font, fill=fill)
        
        del draw

        log.info("Composition of image recording")
        im.save(settings["output-file"])