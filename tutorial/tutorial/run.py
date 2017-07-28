# -*- coding: utf-8 -*-


from scrapy import cmdline
import os


target_path = 'D:\\proj\\pyprj\\spider_img'
list_file = [x for x in os.listdir(target_path)]
for f in list_file:
    abs_f = os.path.join(target_path, f)
    os.remove(abs_f)

name = '192tt'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
