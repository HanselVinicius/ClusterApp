import os

from flask import  redirect, url_for
from api.utils import createFile, getFile


class UploadEditedCsvController:

    def __init__(self,request,session,app,pcoaFromFileService):
            self.request = request
            self.session = session
            self.app = app        
            self.pcoaFromFileService = pcoaFromFileService


    def executeUploadEditedCsv(self):
        createFile(self.request,self.session,self.app)
        fullFilePath = getFile(self.session,self.app)
        fileId = self.session.get('fileId')

        if fullFilePath is None:
            return "FileId not found in session", 400
            
        file_path = os.path.join(self.app.config['UPLOADED_PATH'], fullFilePath)

        if not os.path.exists(file_path):
            return "File not found", 404    
        
        with open(file_path, 'rb') as file:
            pcoa = self.pcoaFromFileService._handleFile(file,fileId)
        return redirect(url_for('render_graph', pcoa=pcoa))
