#!/usr/bin/env python3
"""
Code data structure for DocServe
"""
import datetime
import pickle
import os

class DocContext:
  """
  Information for documents to render to html
  """
  def __init__(self, image_url_func, user_id, doc_id):
    self.image_url_func = image_url_func
    self.user_id = user_id
    self.doc_id = doc_id

  def getImageURL(self, element_index, ref_val):
    return self.image_url_func(self.user_id, self.doc_id,
                               element_index, ref_val)


class ElementType:
  """
  Types of elements in a document
  """
  TITLE = 'title'
  ABSTRACT = 'abstract'
  OUTLINE = 'outline'
  HEADING = 'heading'
  SUBHEADING = 'subheading'
  TEXT = 'text'
  IMAGE = 'image'


class Element:
  """
  Represents a Heading, Subheading, Text, or Image
  """
  def __init__(self, elementType, index=0):
    self.elementType = elementType
    self.elementIndex = index
    self.content = ""

  def setContent(self, content):
    self.content = content

  def getContent(self):
    return self.content

  def emitHTML(self, context):
    if self.elementType == ElementType.TITLE:
      return '<h1>' + self.content + '</h1>'
    elif self.elementType == ElementType.ABSTRACT:
      return '<i>' + self.content + '</i>'
    elif self.elementType == ElementType.OUTLINE:
      return self.content
    elif self.elementType == ElementType.HEADING:
      return '<h2>' + self.content + '</h2>'
    elif self.elementType == ElementType.SUBHEADING:
      return '<h3>' + self.content + '</h3>'
    elif self.elementType == ElementType.TEXT:
      return '<p>' + self.content + '</p>'      
    elif self.elementType == ElementType.IMAGE:
      return ('<img src="' + context.getImageURL(self.elementIndex,
                                                 self.content)
              + '" style="max-width:600px;">')
    return ""
  
    
class Document:
  """
  Stores all information about a document
  """
  
  def __init__(self, doc_id):
    self.filename = None
    self.doc_id = doc_id
    self.titleElement = Element(ElementType.TITLE)
    self.abstractElement = Element(ElementType.ABSTRACT)
    self.outlineElement = Element(ElementType.OUTLINE)
    self.elements = []
    self.createdDate = datetime.datetime.now(datetime.timezone.utc)
    self.modifiedDate = datetime.datetime.now(datetime.timezone.utc)    
    self.next_index = { ElementType.HEADING : 1,
                        ElementType.SUBHEADING : 1,
                        ElementType.TEXT : 1,
                        ElementType.IMAGE : 1 }


  def newDocument(doc_id=None):
    if doc_id is None or len(doc_id) == 0:
      doc_id = os.urandom(3).hex()
    doc = Document(doc_id)
    return doc

  def loadDocument(path, filename):
    file_path = os.path.join(path, filename)
    if not os.path.exists(file_path):
      return None
    
    f = open(file_path, 'rb')
    document = pickle.load(f) 
    f.close()

    # Fix any possibly missing fields
    if not hasattr(document, "createdDate"):
      document.createdDate = datetime.datetime.now(datetime.timezone.utc)
      document.modifiedDate = document.createdDate
    
    return document

  def saveDocument(self, path, filename=None):
    if filename is not None:
      self.filename = filename 
    file_path = os.path.join(path, self.filename)
    self.modifiedDate = datetime.datetime.now(datetime.timezone.utc)    
    f = open(file_path + '.tmp', 'wb')
    pickle.dump(self, f)
    f.close()
    os.replace(file_path + '.tmp', file_path)

  def docId(self):
    return self.doc_id

  TIME_FORMAT="%Y-%m-%d %H:%M %Z"
  
  def getCreateDate(self):
    return self.createdDate.strftime(Document.TIME_FORMAT)

  def getModifyDate(self):
    return self.createdDate.strftime(Document.TIME_FORMAT)

  def setElementContent(self, elementType, index, content):
    new_index = index
    
    if elementType == ElementType.TITLE:
      self.titleElement.setContent(content)
    elif elementType == ElementType.ABSTRACT:      
      self.abstractElement.setContent(content)
    elif elementType == ElementType.OUTLINE:
      self.outlineElement.setContent(content)
    else:
      element = self.findOrCreateElement(elementType, index)
      element.setContent(content)
      new_index = element.elementIndex
    return new_index

  def getElementContent(self, elementType, index):
    if elementType == ElementType.TITLE:
      return self.titleElement.getContent()
    elif elementType == ElementType.ABSTRACT:      
      return self.abstractElement.getContent()
    elif elementType == ElementType.OUTLINE:
      return self.outlineElement.getContent()
    else:
      element = self.findElement(elementType, index)
      if element is not None:
        return element.getContent()
    return None

  def findElement(self, elementType, index):
    for element in self.elements:
      if element.elementType == elementType and element.elementIndex == index:
        return element
    return None

  def getNextIndex(self, elementType):
    index = self.next_index[elementType]
    self.next_index[elementType] = index + 1
    return index

  def findOrCreateElement(self, elementType, index):
    element = self.findElement(elementType, index)
    if element is None:
      index = self.getNextIndex(elementType)
      element = Element(elementType, index)
      self.elements.append(element)
    return element
  
                          
def test():
  print("new document")
  doc = Document.newDocument()
  
  print("set title")  
  doc.setElementContent(ElementType.TITLE, 0, "Document Title")
  
  print("set abstract")  
  doc.setElementContent(ElementType.ABSTRACT, 0, "This is a detailed abstract")
  
  print("set heading")  
  hindex = doc.setElementContent(ElementType.HEADING, 0, "Heading 1")
  
  print("set subheading")  
  index = doc.setElementContent(ElementType.SUBHEADING, 0, "SubHeading 1")
  
  print("set text")  
  tindex = doc.setElementContent(ElementType.TEXT, 0, "This is a long paragraph")
  
  print("set image")
  index = doc.setElementContent(ElementType.IMAGE, 0, "image stuff")

  print("get title")
  title = doc.getElementContent(ElementType.TITLE, 0)  
  print("title: %s" % title)

  print("get text")  
  text = doc.getElementContent(ElementType.TEXT, tindex)  
  print("text: %s" % text)

  filename = "tmp-file"
  doc.saveDocument('/tmp', filename)
  doc = Document.loadDocument('/tmp', filename)
  
  print("get heading")  
  text = doc.getElementContent(ElementType.HEADING, hindex)  
  print("heading: %s" % text)

if __name__ == "__main__":
  test()
    
        
    
        
        

    
    
