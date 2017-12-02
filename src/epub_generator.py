# coding: utf-8
import os.path
import zipfile
from datetime import datetime

title = '测试'
author = 'daijiang'
publisher = '母鸡啊'
date = datetime.now().strftime('%Y-%d-%m')
desc = '弄着玩的'

# 0.创建目标epub文件
epub = zipfile.ZipFile('../output/my_ebook.epub', 'w')

# 1.mimetype文件
# 位置:根目录
epub.writestr("mimetype", "application/epub+zip")

# 2.container.xml的主要功能用于告诉阅读器，电子书的根文件（rootfile）的路径和打开放式，
# 一般来讲，该container.xml文件也不需要作任何修改，除非你改变了根文件的路径(OEBPS)和文件名称
# 位置:META_INF/container.xml
epub.writestr("META-INF/container.xml",
              '''<?xml version="1.0" encoding="utf-8" ?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles>
  <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
</rootfiles>
</container>''')

# 3.封面图片和描述文件
# 位置:OEBPS/cover.png 和 OEBPS/coverpage.xhtml
epub.write('../material/cover.png', 'OEBPS/images/cover.png')

epub.writestr('OEBPS/coverpage.xhtml', """<?xml version="1.0" encoding="utf-8" ?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>cover</title>
</head>
<body>
<div><img src="images/cover.png" alt="cover"/></div>
</body>
</html>""")


# 4.html章节文件
# 位置:OEBPS/Content.xml

navPoint = """<navPoint id="coverpage" playOrder="0"><navLabel><text>封面</text></navLabel><content src="coverpage.xhtml"/></navPoint>"""

manifest = """
<item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>
<item href="images/cover.png" id="cover" media-type="image/png"/>
<item href="coverpage.xhtml" id="coverpage" media-type="application/xhtml+xml"/>"""

spine = """<itemref idref="coverpage" linear="no"/>"""

html_files = ['../material/ch1.html', '../material/ch2.html']

for i, html in enumerate(html_files):
    basename = os.path.basename(html)

    navPoint += '<navPoint id="file_%s" playOrder="%s"><navLabel><text>%s</text></navLabel><content src="%s"/></navPoint>' \
                % (i+1, i+1, basename.split('.')[0], basename)
    manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>'\
                % (i+1, basename)
    spine += '<itemref idref="file_%s" />' % (i+1)

    epub.write(html, 'OEBPS/'+basename)


# 5.电子书的目录文件toc.ncx
# 位置:OEBPS/toc.ncx
epub.writestr('OEBPS/toc.ncx', """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
<head>
<meta name="dtb:uid" content=""/>
<meta name="dtb:depth" content="1"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle>
<text>{title}</text>
</docTitle>
<navMap>
{navPoint}
</navMap></ncx>""".format(title=title, navPoint=navPoint))

# 6.索引文件
# 位置:OEBPS/Content.opf
index_tpl = '''<?xml version="1.0" encoding="UTF-8" ?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
<metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uuid_id" opf:scheme="uuid"></dc:identifier>
<dc:title>{title}</dc:title>
<dc:creator opf:role="aut">{author}</dc:creator>
<dc:contributor opf:role="bkp">dj</dc:contributor>
<dc:publisher>{publisher}</dc:publisher>
<dc:date>{date}</dc:date>
<dc:subject>{subject}</dc:subject>
<dc:language>zh</dc:language>
<dc:description>{description}</dc:description>
<dc:rights></dc:rights>
<dc:contributor></dc:contributor>
<meta name="cover" content="cover"/>
</metadata>
<manifest>
{manifest}
</manifest>
<spine toc="ncx">
{spine}
</spine>
</package>'''

epub.writestr('OEBPS/Content.opf',
              index_tpl.format(title=title,
                               author=author,
                               publisher=publisher,
                               date=date,
                               subject='',
                               description=desc,
                               manifest=manifest,
                               spine=spine))


