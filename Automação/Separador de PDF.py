from PyPDF2 import PdfFileReader, PdfFileWriter

'''
Projeto por Lucas Severi.

Necessidade: Empresa quer separar um grande documento em pdf por páginas.
> Páginas nomeadas de 1 a n
> Todos pdf's armazenados na mesma pasta

Recursos:
> Documento PDF a ser dividido nomeado "pdf.pdf"

'''

# path do documento
pdf_file = open("/Users/lucaa/Desktop/Python Script/pdf.pdf", "rb")

pdf_reader = PdfFileReader(pdf_file)

num_pages = pdf_reader.getNumPages()

for i in range(num_pages):
	pdf_writer = PdfFileWriter()
	pdf_writer.addPage(pdf_reader.getPage(i))
	# path a ser salvo
	split_file = open('/Users/lucaa/Desktop/Python Script/Separados/pagina_%i.pdf' %(i+1), 'wb')
	pdf_writer.write(split_file)
	split_file.close()
	

pdf_file.close()