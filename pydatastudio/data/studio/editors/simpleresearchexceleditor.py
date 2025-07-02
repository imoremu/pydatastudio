'''
Created on 16 feb. 2021

@author: imoreno
'''
from pydatastudio import resource_manager

from string import Formatter
from datetime import datetime
from pydatastudio.data.studio.data_studio import AbstractResearchListener


class DataResearchExcelEditor(AbstractResearchListener):
    
    SAVE_DATA_KEY = "save"
    FILENAME_KEY = "name"
    SHEET_NAME = "sheet"
        
    def __init__(self, studio, configuracion):
        
        self.studio = studio
        self.configuracion = configuracion
        
        studio.add_research_listener(self)
        
    def _research_finished(self, research_name, **attrs):
        
        research = self.studio.knowledge[research_name]
        
        save_data = self.configuration[DataResearchExcelEditor.SAVE_DATA_KEY]       
        
        if save_data:
            
            filename = resource_manager.get_resource_path(self.configuration[DataResearchExcelEditor.FILENAME_KEY]) 
            sheetname = resource_manager.get_resource_path(self.configuration[DataResearchExcelEditor.SHEET_NAME]) 
            
            for research_item_name, research_item_data in research.items():                                    
                self.save_file(research_item_data, filename, sheetname, {"research" : research_item_name})
    
    def save_file(self, dataframe, file_input_name, sheetname, data=None):        
                    
        time_format = "%d_%m_%Y %H_%M_%S"        
        
        current_time = datetime.now().strftime(time_format)
        
        attrs = {"date": current_time}          
        
        if not data is None: 
            attrs.update(data)                               
    
        formatter = Formatter()
        
        output_file = formatter.format(file_input_name, **data)
    
        self.logger.info (f"Save file {output_file}")
        
        dataframe.to_excel(resource_manager.get_resource_path(output_file))
