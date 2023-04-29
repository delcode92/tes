# self.limit = 18
# self.offset = 0


# def updateLabel(self):
#         # start = 0 + 1
#         # start = 18 + 1
#         # start = 36 + 1
#         start = self.offset + 1
        
#         # min( 0 + 18, 51 )
#         # min( 18 + 18, 51 )
#         # min( 36 + 18, 51 )
#         end = min(self.offset + self.limit, len(self.data))
        
#         # total = 51
#         total = len(self.data)
#         self.label.setText("{}-{} from {} results".format(start, end, total))
        
# def nextPage(self):
#     # 1) 0 + 18 < 51
#     # 2) 18 + 18 < 51
#     # 2) 36 + 18 < 51
#     if self.offset + self.limit < len(self.data):
        
#         # self.offset = 0 + 18
#         # self.offset = 18 + 18
#         # self.offset = 36 + 18
#         self.offset += self.limit
#         self.updateTable()
#         self.updateLabel()
    
# def prevPage(self):
#     if self.offset > 0:
#         self.offset -= self.limit
#         self.updateTable()
#         self.updateLabel()


l1 = [
    {"k1":"v1"},
    {"k2":"v2"},
    {"k3":"v3"}
]

new_list = [{"k0":"v0"}] + l1 + [{"k4":"v4"}]

# print( new_list )

components_setter = [{
                        "name":"main_kendaraan",
                        "category":"widget",
                        "layout": "VBoxLayout",
                        "max_width":700,
                        "style":"style here",
                        "children":[]
                    }]

components_setter[0]["children"] = new_list

# print( components_setter[0]["children"] )

l = []
l = l+ [{"k1":"v1"}]
l = l+ [{"k2":"v2"}]

print( l )

