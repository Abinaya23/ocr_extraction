from PIL import Image 
import pytesseract 
from tesserocr import PyTessBaseAPI
import sys 
from pdf2image import convert_from_path 
import os 
import json
import datetime


# provide the file path where all your fiels located
filePath='C:/Users/abinaya.seenivasan@sap.com/OneDrive - SAP SE/SAP/work/IRPA/blog/ocr/python/'
# filename of the invoice
fileName='invoice.pdf'

# json file path
json_file_path=filePath+'data/'

# tessdata file path
tessdata_path=filePath+'tessdata/.'


# set image dpi
def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(file_path, dpi=(300, 300))
    return file_path


# extract the pages from the pdf
pages = convert_from_path(filePath+fileName,500)

#process each pages in the pdf
for index, page in enumerate(pages):
	imageFileName=fileName.split('.')[0]+str(index)+'.jpg'
	pages[index].save(filePath+imageFileName,'JPEG')
	imageFileName=set_image_dpi(filePath+imageFileName)

	#call tessdata for every image
	with PyTessBaseAPI(path=tessdata_path, lang='vie') as api:
	     api.SetImageFile(filePath+imageFileName)
	     outText=api.GetUTF8Text()
	     outTextList=outText.split('\n')

	     print(outTextList[5:9])
	
	# retrieve company name from 5th line
	companyName=outTextList[4].split(':')[1]

	# retrieve address from 7thth line
	address=outTextList[6].split(': ')[1]

	# retrieve telphone from 8th line
	telPhone=outTextList[7].split(': ')[1]

	# retrieve invoice number from 10th line
	invoiceNum=outTextList[9].split(': ')[1]

	# retrieve account number from 12th line
	accNum=outTextList[11].split(': ')[1]

	#form data as dictionary
	data={'companyName':companyName,'address':address,'telPhone':telPhone,'invoiceNum':invoiceNum,'accNum':accNum}

	if not os.path.exists(json_file_path):
		os.makedirs(json_file_path)
	#save data as json
	with open(json_file_path+fileName.split('.')[0]+str(index)+'.json','w') as json_file:
		json.dump(data,json_file)