from xml.etree import ElementTree as ET
from modules.utils.Validation import elementValidation 
from modules.utils.translateHandling import translateHandling 

class Translate:
    
    def __init__(self, parserObj:object) -> None:
        
        self.str_buffer = ""
        self.attrs = ""
       
        self.validate = elementValidation()
        self.translateHandling = translateHandling()

        # root as ElemenTree object
        self.root = parserObj.root
        self.createXMLString( self.root, len(self.root) )

        '''

    


    def propsToElements(self, elem):

        
        
        

        if len(props_val):
            try:
                # convert props string to dictionary
                props_dict = ast.literal_eval(props_val)
            except:
                # exit system if props_val not suitable for literal_eval(), eg: "", " " ... etc
                sys.exit(f'<{elem.tag} props="{props_val}"/> --> props must in JSON format')
                
            # if props in JSON, translate to xml format
            if isinstance(props_dict, dict):
                
                # check if has name key
                name_val = props_dict.get("name", False)

                # check if name_val has value/content and it's a list
                if name_val:

                    if isinstance(name_val, list) is False:
                        sys.exit(f'<{elem.tag} props="{props_val}"/> --> "name": value --> value must in array format')            
            
                    new_element = ""

                    for name in name_val:
                        
                        # check if name type is string
                        if isinstance(name, str) is False:
                            sys.exit(f'"name":["content-1", "content-2", ...etc ] --> content must in string format')
                        
                        # create new element with name attribute
                        new_element = f'{new_element}<{elem.tag} name="{name}" '
                        atr = ""
                        for k,v in props_dict.items():
                            if k != "name":
                                
                                break_flag = 0
                                # issue - bagaimana jika nilainya bukan berupa list looping dibawah tidak akan jalan
                                # 
                                for value in v:
                                    
                                    # if find matching value, break from looping
                                    if break_flag==1:
                                        break
                                    
                                    if "@"+name in value:
                                        splitVal = value.split("@")
                                        atr = f'{atr}{k}="{splitVal[0]}" '
                                        break_flag= 1
                                    else:
                                        sys.exit(f"{value} don't have '@' reference")    

                        # check default attribute
                        atr = self.checkDefaultAttribute(elem.tag, atr)

                        # close tag />
                        new_element = f'{new_element}{atr}/>'
                else:
                    sys.exit(f'<{elem.tag} props="{props_val}"/> --> props must have "name" key , see more detail here https://delcode92.github.io#props_key')            
            else:
                # exit system if literal_eval() not error but the result is not a dictionary
                sys.exit(f'<{elem.tag} props="{props_val}"/> --> props must in JSON format')
        
        return new_element

    def attributesToStr(self, elem):
        attr = ""

        # 1) if has props attribute, ignore another attribute inside that element, because props is a shorthand to handle attributes
        # 2) ignore empty props --> props=""
        # 3) show error message if props content not in JSON format

        if "props" in elem.attrib:

            
                    
            return new_element_str,1

        elif "props" not in elem.attrib:

            for k,v in elem.attrib.items():
                attr = f'{attr}{k}="{v}" '

            attr = self.checkDefaultAttribute(elem.tag, attr)    
            return attr,0'''



    def createXMLString(self, root:ET, rootLength:int) -> str:
        
        # loop = 0

        for child in root:
            
            '''check if tags "child" is valid '''
            self.validate.validateTag(child)            

            '''
            - check what kind of child -> has custom/special attribute or normal attribute
            - return custom function -> if has custom/special sttribute
            - otherwise return standard function
            '''
            
            result = self.validate.validateElementType(child)
            
            # loop=loop+1

            # child_len = len(child)   
            # attr_len = len(child.attrib)

            # none disini karena ada argument self pada customAttribute() atau standardAttribute()
            # coba buat sehingga tanpa perlu None

            # ....... do something here  ....
            # translate element into xml string
            # self.str_buffer = f"{self.str_buffer}......"

            # if result is a tuple, :
            # result[0] -> contain used special attribs being used in that element
            # result[1] -> contain translateHandling.customAttribute function

            if isinstance(result, tuple):
                
                func = result[1]
                usedSpecialAttribs = result[0]

                func(None, child, usedSpecialAttribs)
            
            # result -> contain translateHandling.standardAttribute
            else:
                func = result
                func(None, child)

            
            

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