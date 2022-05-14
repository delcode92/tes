
import sys
from xml.etree import ElementTree
# from modules.utils.Validation import attributeValidation

class translateHandling:
    
    def __init__(self) -> None:
        pass 

    def customAttribute(self=None, element:ElementTree=None, speciaL_attrib:list=None): 
        ...
        
        # self.getWhatToDo(element)


        # self.createXMLString(element, child_len)

        '''

            # get tag and its attribute
            if attr_len and child_len:
                self.attrs = self.attributesToStr(child)

                # if self.attrs[1] == 0 -> return just attributes
                # if self.attrs[1] == 1 -> return new element from props
                if self.attrs[1] == 1:
                    self.str_buffer = f"{self.str_buffer}{self.attrs[0]} " 
                elif self.attrs[1] == 0: 
                    self.str_buffer = f"{self.str_buffer}<{child.tag} {self.attrs[0]}> " 
                
            elif not attr_len and child_len:
                default_attr = self.checkDefaultAttribute(child.tag, "")
                self.str_buffer = f"{self.str_buffer}<{child.tag} {default_attr}> " 

            elif attr_len and not child_len:
                self.attrs = self.attributesToStr(child)

                if self.attrs[1] == 1:
                    self.str_buffer = f"{self.str_buffer} {self.attrs[0]}" 
                elif self.attrs[1] == 0: 
                    self.str_buffer = f"{self.str_buffer}<{child.tag} {self.attrs[0]}/> "

            elif not attr_len and not child_len:
                default_attr = self.checkDefaultAttribute(child.tag, "")
                self.str_buffer = f"{self.str_buffer}<{child.tag} {default_attr}/>" 
            
            # jika ada child maka recursive lagi
            if child_len:
                self.createXMLString(child, child_len)


        if rootLength and (rootLength==loop) and (root.tag != "main"):
            self.str_buffer = f"{self.str_buffer}</{root.tag}>"

    
        '''

    

    def standardAttribute(self=None, element:ElementTree=None):
        ...
        # self.getWhatToDo(element)

    def getWhatToDo(self=None, element:ElementTree=None):
        
        child_len = len(element)
        attr_len = len(element.attrib)
        
        if attr_len and child_len:
            ...
        elif not attr_len and child_len:
            ...
        elif attr_len and not child_len:
            ...
        elif not attr_len and not child_len:
            ...

            
        if child_len:
            ...

    def propsToElements(self, element:ElementTree) -> str:
        ...
        

    #     new_element = ""
        