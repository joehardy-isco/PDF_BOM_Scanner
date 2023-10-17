#!/usr/bin/env python
# coding: utf-8

# In[49]:


import os
fol_path = r'F:\PycharmProjects\pdf_drawing_bom_scanner'
pdf_path = r'2-0-528-40139-PE01 - Isometric.pdf'
image_path = r'BOM.png'
full_pdf_path = os.path.join(fol_path,pdf_path)
full_image_path = os.path.join(fol_path,image_path)


# In[50]:


import pytesseract


# In[51]:


# !pip install pdfminer.six
# from pdfminer.high_level import extract_text

# def extract_text_from_pdf(pdf_path):
#     return extract_text(pdf_path)


# # Example usage
# text = extract_text_from_pdf(full_pdf_path)
# print(text)


# In[57]:


#!pip install PyMuPDF
import fitz

def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text using PyMuPDF
pymupdf_text = extract_text_pymupdf(full_pdf_path).split("\n")
bill_of_materials = []
start_collecting = False
for line in pymupdf_text:
    if line=='N':
        break
    if line=='BILL OF MATERIALS':
        start_collecting = True
    if start_collecting:   
        bill_of_materials.append(line)


# In[58]:


import numpy as np


# In[73]:


new_table = []
second_table = []
unallowed = ['BILL OF MATERIALS','PIPE','FITTINGS','FLANGES','VALVES','PIPE SUPPORTS']
columns = ['ID','QTY','ND','DESCRIPTION','SUPPORT DETAIL']
columns_seen = [0,0,0,0,0]
table_to_input = new_table
second_table_used = False
for t_element in bill_of_materials:
    if not t_element.upper().strip() in unallowed:
        try:
            col_i = columns.index(t_element.upper().strip())
        except:
            col_i = -1
        if col_i!=-1:
            if columns_seen[col_i]==0:
                if t_element=='SUPPORT DETAIL':
                    new_table = table_to_input
                    table_to_input = second_table
                    table_to_input.extend(columns[:-1])
                    second_table_used = True
                columns_seen[col_i]=1
            elif columns_seen[col_i]==1:
                continue
        table_to_input.append(t_element)
if second_table_used:
    second_table = table_to_input
else:
    new_table = table_to_input
new_table = np.array(new_table).reshape(-1,4)
if len(second_table)>0:
    second_table = np.array(second_table).reshape(-1,5)
print(new_table)
print(second_table)


# In[ ]:





# In[80]:


import pandas as pd
ndf = pd.DataFrame(new_table)
ndf.columns = ndf.iloc[0]
ndf = ndf.drop(0)
if isinstance(second_table,np.ndarray):
    sdf = pd.DataFrame(second_table)
    sdf.columns = sdf.iloc[0]
    sdf = sdf.drop(0)
    combined = pd.concat([ndf, sdf])#.fillna(None)
    final = combined
else:
    final = ndf
final


# In[ ]:




