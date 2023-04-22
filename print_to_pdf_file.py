# from fpdf import FPDF

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font('helvetica', size=12)
# pdf.cell(txt="hello world wkwkwkw")
# pdf.output("hello_world.pdf")

import webbrowser,os
from fpdf import FPDF

# class PDF(FPDF):
#     def header(self):
#         # Logo
#         # self.image('logo_pb.png', 10, 8, 33)
#         # Arial bold 15
#         self.set_font('Arial', 'B', 15)
#         # Move to the right
#         self.cell(80)
#         # Title
#         self.cell(30, 10, 'Title', 1, 0, 'C')
#         # Line break
#         self.ln(20)

#     # Page footer
#     def footer(self):
#         # Position at 1.5 cm from bottom
#         self.set_y(-15)
#         # Arial italic 8
#         self.set_font('Arial', 'I', 8)
#         # Page number
#         self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# # Instantiation of inherited class
# pdf = PDF()
# pdf.alias_nb_pages()
# pdf.add_page()
# pdf.set_font('Times', '', 12)
# for i in range(1, 41):
#     pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
# pdf.output('tuto2.pdf', 'F')


# Margin
m= 10
# Page width: Width of A4 is 210mm x 297mm 
pw = 297 - 2*m
# Cell height
ch = 12
pdf = FPDF()
pdf.add_page(orientation='L')
pdf.set_font('Arial', '', 12)

# pdf.cell(w=(pw/5)*5, h=ch, txt="Rekap Parkir ...", border=1, ln=1, align='C')
# pdf.cell(w=(pw/5)*5, h=ch, txt="periode: ... ", border=1, ln=1)

# header
pdf.cell(w=(pw/5), h=ch*2, txt="Lama Parkir", border=1, align='C')
pdf.cell(w=(pw/5), h=ch, txt="Motor", border=1)
pdf.cell(w=(pw/5), h=ch, txt="Mobil", border=1)
pdf.cell(w=(pw/5), h=ch, txt="Lainnya", border=1)
pdf.cell(w=(pw/5), h=ch, txt="Grand Total", border=1)

pdf.ln()

pdf.cell((pw/5), ch,  border=0)
# pdf.cell(w=(pw/5), h=ch)

# motor
pdf.cell(w=(pw/5)/2, h=ch, txt="jml", border=1)
pdf.cell(w=(pw/5)/2, h=ch, txt="total", border=1)

# mobil
pdf.cell(w=(pw/5)/2, h=ch, txt="jml", border=1)
pdf.cell(w=(pw/5)/2, h=ch, txt="total", border=1)

# lainnya
pdf.cell(w=(pw/5)/2, h=ch, txt="jml", border=1)
pdf.cell(w=(pw/5)/2, h=ch, txt="total", border=1)

# grand total
pdf.cell(w=(pw/5)/2, h=ch, txt="jml", border=1)
pdf.cell(w=(pw/5)/2, h=ch, txt="total", border=1)

# pdf.ln()
# pdf.cell(w=(pw/5)*5, h=ch, txt=".. datas ...", border=1, ln=0)
# pdf.cell(w=(pw/3), h=ch, txt="Cell 3a", border=1, ln=0)
# pdf.cell(w=(pw/3), h=ch, txt="Cell 3b", border=1, ln=0)
# pdf.cell(w=(pw/3), h=ch, txt="Cell 3c", border=1, ln=1)

# pdf.cell(w=(pw/3), h=ch, txt="Cell 4a", border=1, ln=0)
# pdf.cell(w=(pw/3)*2, h=ch, txt="Cell 4b", border=1, ln=1)

# pdf.set_xy(x=10, y= 220) # or use pdf.ln(50)

# pdf.cell(w=0, h=ch, txt="Cell 5", border=1, ln=1)

pdf.output('./tuto2.pdf', 'F')

path = os.path.abspath("tuto2.pdf")

webbrowser.open_new("file://"+path)

# os.chmod('./tuto2.pdf', stat.S_IXOTH)
# os.system('./tuto2.pdf')


