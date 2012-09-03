from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

from pdfminer.layout import LTTextBox, LTTextLine


class Box(object):
    ''' represents one rubai '''

    def __init__(self, x0, x1, y0, y1, text):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.text = text

    def __str__(self):
        return "<Box (%d, %d) (%d, %d)>" % (self.x0, self.y0, self.x1, self.y1)


def get_text(layout_objs):
    text_content = []

    boxes = []

    for l in layout_objs:
        if isinstance(l, LTTextBox) or isinstance(l, LTTextLine):
            #print type(l), l.bbox
            boxes.append(Box(l.x0, l.x1, l.y0, l.y1, l.get_text()))

            #if l.index == 2:
                #text_content.append(l.get_text())
            #elif l.index == 3:
                #text_content.append(l.get_text())
    #print ''.join(text_content).encode('utf-8')
    boxes.sort(key=lambda x: x.x0, reverse=True)
    print ("".join([b.text for b in boxes])).encode('utf-8')

    return text_content


def main():

    # Open a PDF file.
    fp = open('Divani_Kebir-1.pdf', 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    doc = PDFDocument()
    # Connect the parser and document objects.
    parser.set_document(doc)
    doc.set_parser(parser)
    # Supply the password for initialization.
    # (If no password is set, give an empty string.)
    doc.initialize()
    # Check if the document allows text extraction. If not, abort.
    if not doc.is_extractable:
        print 'not extraction'
        return

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in doc.get_pages():
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        if layout.pageid >= 2:
            break
        get_text(layout)

if __name__ == '__main__':
    main()
