import datetime
import cgi
from bson.objectid import ObjectId
from helper_functions import *

from extract_docx import Doc
import os
import base64
class Molecule:

    def __init__(self, default_config):
        self.path = default_config['MOLECULES_PATH']
        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def get_molecules(self, limit, skip, tag=None, search=None):
        self.response['error'] = None
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}]}
        try:

            self.response['data'] = []
            folders=filter(os.path.isdir,map(lambda x: os.path.join(self.path,x), os.listdir(self.path)))


            for folder in folders:
                docfile_name = filter(lambda s:re.findall(r'^[^\~].*\.docx?$',s),os.listdir(folder))[0]
                docfile_name=os.path.join(folder,docfile_name)
                # docfile_name = os.popen('ls \"'+folder+'/*.doc*\"|head -1').read().strip()
                doc=Doc(docfile_name)
                self.response['data'].append({
                    'title': os.path.basename(folder),
                    'body': doc.text,
                    'image': doc.image
                })

        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response



    def get_molecule_by_name(self, name):
        self.response['error'] = None
        try:

            folder=os.path.join(self.path,name)
            docfile_name = os.popen("ls "+folder+"/*.doc*|head -1").read().strip()

            doc=Doc(docfile_name)

            self.response['data']={
                'title': os.path.basename(folder),
                'body': doc.text,
                'image': doc.image
            }

        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Molecule not found..'

        return self.response

    def get_total_count(self, tag=None, search=None):
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}]}

        return len(filter(os.path.isdir,map(lambda x: os.path.join(self.path,x), os.listdir(self.path))))




    @staticmethod
    def print_debug_info(msg, show=False):
        if show:
            import sys
            import os

            error_color = '\033[32m'
            error_end = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                     'line': sys.exc_info()[2].tb_lineno,
                     'details': str(msg)}

            print error_color
            print '\n\n---\nError type: %s in file: %s on line: %s\nError details: %s\n---\n\n'\
                  % (error['type'], error['file'], error['line'], error['details'])
            print error_end
