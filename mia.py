#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template, static_file, error, request, redirect
from optparse import OptionParser
import os
import time


TEXT_TYPE = ['doc', 'docx', 'txt', 'rtf', 'odf', 'text', 'nfo']
AUDIO_TYPE = ['aac', 'mp3', 'wav', 'wma', 'm4p', 'flac']
IMAGE_TYPE = ['bmp', 'eps', 'gif', 'ico', 'jpg', 'jpeg', 'png', 'psd', 'psp', 'raw', 'tga', 'tif', 'tiff', 'svg']
VIDEO_TYPE = ['mv4', 'bup', 'mkv', 'ifo', 'flv', 'vob', '3g2', 'bik', 'xvid', 'divx', 'wmv', 'avi', '3gp', 'mp4', 'mov', '3gpp', '3gp2', 'swf', 'mpg', 'mpeg']
COMPRESS_TYPE = ['7z', 'dmg', 'rar', 'sit', 'zip', 'bzip', 'gz', 'tar', 'ace']
EXEC_TYPE = ['exe', 'msi', 'mse']
SCRIPT_TYPE = ['js', 'html', 'htm', 'xhtml', 'jsp', 'asp', 'aspx', 'php', 'xml', 'css', 'py', 'bat', 'sh', 'rb', 'java', 'sql']

path_local = "."

PAGE = u'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>{{path_dir}}</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
        <style>
            body
            {
                margin:50px 0;
                padding:0;
                text-align:center;
                font-family:"Lucida Sans Unicode","Lucida Grande",Sans-Serif;
            }
            .content
            {
                width:800px;
                margin:0 auto;
            }
            .path
            {
                text-align:left;
                padding:0 0 .3em .7em;
            }
            .line
            {
                border-bottom:2px solid #6b6b6b;
            }
            .footer
            {
                text-align:right;
                font-size:10px;
            }
            .alert {
                background-color: #FCF8E3;
                border: 1px solid #FBEED5;
                border-radius: 4px 4px 4px 4px;
                color: #C09853;
                margin-bottom: 18px;
                padding: 8px 35px 8px 14px;
                text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);
            }
            #fileTable
            {
                font-size:12px;
                background:#fff;
                width:800px;
                border-collapse:collapse;
                text-align:left;
            }
            #fileTable th
            {
                font-weight:normal;
                text-align:left;
                padding-left:1em;
                border-bottom:1px solid #ff1405;
                height:2.5em;
            }
            #fileTable td
            {
                border-bottom:1px solid #e0e0e0;
                color:#3c3c3c;
                height:25px;
                padding-left:1em;
            }
            #fileTable td.data
            {
                background-color:#ededed;
                width:12.5%;
            }
            #fileTable a
            {
                text-decoration:none;
                color:#3c3c3c
            }
            #fileTable a:hover
            {
                color:#555
            }
            i.icon
            {
                background:url(data:image/png;base64,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) no-repeat scroll 0 0 transparent;
                display:block;
                float:left;
                height:16px;
                margin:0 10px 0 0;
                width:16px;
            }
            i.icon.pdf
            {
                background-position:-0px -0px;
            }
            i.icon.folder
            {
                background-position:-16px -0px;
            }
            i.icon.script
            {
                background-position:-32px -0px;
            }
            i.icon.unknow
            {
                background-position:-48px -0px
            }
            i.icon.compress
            {
                background-position:-64px -0px;
            }
            i.icon.audio
            {
                background-position:-80px -0px;
            }
            i.icon.imagen
            {
                background-position:-96px -0px;
            }
            i.icon.text
            {
                background-position:-112px -0px;
            }
            i.icon.video
            {
                background-position:-128px -0px;
            }
            i.icon.exec
            {
                background-position:-144px -0px;
            }
        </style>
    </head>
    <body>
        <div class="content">
            %if error is None:
              <div class="path">
                PATH: {{path_dir}}
              </div>
             <div class="line"></div>
            <table id="fileTable">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Date</th>
                        <th>Size</th>
                    </tr>
                </thead>
                <tbody>
                %for file in to_html:
                    <tr>
                        <td>
                            <i class='icon {{file.iconType}}'></i>
                            %if file.iconType == 'folder':
                                <a href='{{file.folder}}/{{file.filename}}'>{{file.filename}}</a>
                            %else:
                                <a href='/download?file={{file.folder}}/{{file.filename}}'>{{file.filename}}</a>
                            %end
                        </td>
                        <td class='data'>
                            {{file.filesize}}
                        </td>
                        <td class='data'>
                            {{file.filedate}}
                        </td>
                    </tr>
                %end
                </tbody>
            </table>
            %else:
            <div class="alert">
                {{error}}
            </div>
            %end
            <div class="footer">
                Powered by <a href='https://github.com/herrerae/mia'>Mia</a>
            </div>
        </div>
    </body>
</html>

'''


@route('/')
@route('/index/')
def index_2():
    redirect('/index')


@route('/index')
@route('/index/:path#.+#')
def index(path=None):
    if path is None:
        return read_folder('')
    else:
        return read_folder(path)


@route('/download')
def download():
    filename = request.GET.get('file')
    return static_file(filename, root=path_local, download=filename)


@error(404)
def error404(error):
    return 'Nothing here, sorry'


@error(500)
def error500(error):
    return 'La carpeta no existe'


#------------------ UTILS -----------------------------


def read_folder(path):
    to_html = []
    if path == '':
        path_dir = path_local
    else:
        path_dir = path_local + '/' + path

    try:
        file_list = os.listdir(path_dir)
    except Exception:
        return template(PAGE, error="Folder/Directory not found, Please check the name", path_dir=path)
    for archivo in file_list:
        if archivo == 'mia_main.py' or archivo == 'bottle.py' or archivo == 'bottle.pyc':
            pass
        else:
            file_path = os.path.join(path_dir, archivo)
            if os.path.isdir(file_path) == True:
                cosa = HtmlFile('folder', request.fullpath, archivo, file_path)
                to_html.append(cosa)
            else:
                extension = os.path.splitext(archivo)[1].replace('.', '')
                if extension in TEXT_TYPE:
                    type_file = 'text'
                elif extension in AUDIO_TYPE:
                    type_file = 'audio'
                elif extension in IMAGE_TYPE:
                    type_file = 'imagen'
                elif extension in VIDEO_TYPE:
                    type_file = 'video'
                elif extension in COMPRESS_TYPE:
                    type_file = 'compress'
                elif extension in EXEC_TYPE:
                    type_file = 'exec'
                elif extension in SCRIPT_TYPE:
                    type_file = 'script'
                elif extension == 'pdf':
                    type_file = 'pdf'
                else:
                    type_file = 'unknow'
                cosa = HtmlFile(type_file, path, archivo, file_path)
                to_html.append(cosa)
    if path == '':
        path = 'index'
    else:
        path = 'index' + "/" + path
    return template(PAGE, to_html=to_html, path_dir=path, error=None)


def convert_bytes(path):
    '''
    Copy from http://www.5dollarwhitebox.org/drupal/node/84
    '''
    bytes = float(os.path.getsize(path))
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2f Tb' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2f Gb' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2f Mb' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2f Kb' % kilobytes
    else:
        size = '%.2f Byte' % bytes
    return size


def date_file(path):
    tiempo = time.gmtime(os.path.getmtime(path))
    return time.strftime("%d/%m/%Y-%H:%M:%S", tiempo)


def set_argument():
    parser = OptionParser(usage="Usage: %prog [options]", version="%prog 1.5")
    parser.add_option("-d", "--path", action="store", dest="path", default=".", help="Directory you want to share Ex. /home/hans/project/milleniun_falcon",)
    parser.add_option("-o", "--host", action="store", dest="host", default="localhost",  help="Server host. Defaul: localhost",)
    parser.add_option("-p", "--port", action="store", dest="port", default=8080, help="Server port. Defaul: 8080",)
    return parser


class HtmlFile(object):
    def __init__(self, iconType, folder, filename, file_path):
        self.iconType = iconType
        self.folder = folder.decode('cp1252')
        self.filename = filename.decode('cp1252')
        self.filesize = convert_bytes(file_path)
        self.filedate = date_file(file_path)

if __name__ == '__main__':
    (options, args) = set_argument().parse_args()
    debugMode = True
    port = options.port
    host = options.host
    path_local = options.path
    run(host=host, port=port, reloader=debugMode, debug=debugMode)
