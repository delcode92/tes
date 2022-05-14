from pyclbr import Function
import sys,ast
from xml.etree import ElementTree
from xmlrpc.client import Boolean, boolean
from modules.utils.translateHandling import translateHandling
from modules.utils.constantValue import constantvalue

class elementValidation:
    def __init__(self) -> None:
        self.allowedTags = constantvalue().allowedTags

    def validateTag(self, content:...=None, tags:list=None) -> boolean:
        
        
        if isinstance(content, str):
            for t in tags:
                element_tag = f"<{t}"
        
                if not element_tag in content:
                    sys.exit(f"\nsorry, your file don't have {element_tag} /> element \nplease put {element_tag} /> in your file\n")
        
        elif isinstance(content, ElementTree.Element):
            
            '''
            content same as ElementTree child
            get child tag
            '''

            if content.tag not in self.allowedTags:
                sys.exit(f"not known for <{content.tag}/> tag name, please check your tag name ")
  
    def validateElementType(self, element:ElementTree) -> Function:
        
        # return custom() or normal()

        # custom / special attrib
        customAttrs = constantvalue().specialAttrib
        
        usedSpecialAttrs = []
        
        stat = False
        # attr_name = ""

        for a in customAttrs:
            x = element.attrib.get(a, 0)

            if x != 0 :
                
                stat = True

                # save used special attribs
                usedSpecialAttrs.append(a)

                # validate attribute
                a = a.capitalize() 
                getattr( attributeValidation, f"validate{a}")( element )
                 

        # harus return tuple function & list special attrirb disini
        # cek dulu panjang attribute & elementnya , baru return function yg sesuai dengan kondisinya
        if stat == False:
            func = translateHandling.standardAttribute
            return func
        
        elif stat == True:
            func = translateHandling.customAttribute
            return usedSpecialAttrs,func


class attributeValidation:
    def __init__(self) -> None:
        pass

    def checkDefaultAttribute(self, element:ElementTree, attrs_string):
        ...

        '''
        # define element tag and it's default attribute
        defAttrsDict = { 
            "input": {"type":"text"},
            "button": {"type":"button"},
            "createform": {"method":"post"} 
        }
        
        xAttr = ""
        for attr,val in defAttrsDict[element].items():

            # if default attribute not in attrs string, add default attribute
            if attr not in attrs_string:
                xAttr = f'{xAttr}{attr}="{val}" '

        return f'{attrs_string} {xAttr}'
        '''

    def validateProps(element:ElementTree)-> Boolean:
        
        
        # if an element has already props attribute, can't combine with other attribute
        if len(element.keys()) > 1:
            sys.exit("in one element, props attribute cannot be combined with other attribute")


        # cek props length
        props_value = element.attrib["props"]

        if len(props_value) == 0:
            sys.exit("your props attribute is empty")
        
        try:
            # convert props_value string to dictionary
            props_dict = ast.literal_eval(props_value)
        except:
            # exit system if props_val not suitable for literal_eval(), eg: "", " " ... etc
            sys.exit(f'<{element.tag} props="{props_value}"/> --> props must in JSON format')

        # check if props_dict string has successful convert to dictionary
        aDict = isinstance(props_dict, dict)

        if not aDict:
            # exit system if literal_eval() not error but the result is not a dictionary
            sys.exit(f'<{element.tag} props="{props_value}"/> --> props must in JSON format')
        
        # check if has name key
        name_val = props_dict.get("name", False)

        if not name_val:
            sys.exit(f'<{element.tag} props="{props_value}"/> --> props must have "name" key , see more detail here https://delcode92.github.io#props_key')