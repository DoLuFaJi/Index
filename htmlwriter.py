import os
import re

class HtmlWriter:
    #To write an html file that can be opened with a navigator
    #To use:
    #   html = HtmlWriter()
    #   html.writeHTMLresponse("hellohello", response)
    #       where hellohello is a string of the request from a user an response a list of Document
    #the created file is in ./test and its name is the request
    def __init__(self, datafolder):
        self.datafolder = datafolder
        self.error = False

    def __write__(self, request, text):
        try:
            file = open ('./test/'+request , 'a')
            file.write(text)
        except:
            print("Error: can\'t find file or write data")
            self.error = True
        else:
            file.close()

    def remove(self, request):
        try:
            if os.path.isfile('./test/'+request):
                os.remove('./test/'+request)
        except:
            print("Error: can\'t find file")
            self.error = True

    def header(self, request, details = ""):
        text = """
        <!DOCTYPE html>
        <html>
        <body>
        <h1>Index Dolufaji</h1>
        <p>Response for request """+request+"""</p>"""
        self.__write__(request, text)

    def footer(self, request):
        text = """<p>END Response for request """+request+"""END</p></body></html><script>function showDiv(lala) {console.log(document.getElementById(lala).style.display);if(document.getElementById(lala).style.display === 'none'){document.getElementById(lala).style.display = "block";}else{document.getElementById(lala).style.display = "none";}}</script>"""
        self.__write__(request, text)

    def addDocument(self, documentId, request, score):
        try:
            dif = open ('./data/Docs_in_file' , 'r')
            docsinfile = dif.readlines()
            text = "<input type=\"button\" value="+documentId+" onclick=\"showDiv("+documentId+")\"/><div id="+documentId+"  style=\"display:none;\" ><p>DOC ID : "+documentId+" with score = "+score+"</p>"
            self.__write__(request, text)
            for line in docsinfile:
                if str(","+documentId+",") in line:
                    filename = line[:line.find("=")]
                    text = """<p>FILE NAME : """+filename+"""</p>"""
                    file = open (self.datafolder+filename, 'r')
                    doc_in_file = file.read().split("<DOC>")
                    del doc_in_file[0] #the first is empty
                    for doc in doc_in_file:
                        docid = re.findall("<DOCID> (.*?) </DOCID>", doc)
                        if len(docid)!=0:
                            docid = docid[0]
                            if docid == documentId:
                                self.__write__(request, doc)
            text = "</div>"
            self.__write__(request, text)

        except Exception as e:
            print("Error: can\'t find file - adddocument")
            self.error = True

    def writeHTMLresponse(self, request, response):
        self.remove(request)
        self.header(request)
        for r in response:
            self.addDocument(str(r.name), request, str(r.score))
        self.footer(request)
        if self.error == False:
            print("""Generated file in './test/'"""+request)
#
# from document import Document
#
# d1 = Document(273, 456)
# d2 = Document(31, 46)
# d3 = Document(24, 56)
# d4 = Document(712, 546)
# d5 = Document(704, 789)
# d6 = Document(341, 159)
# response=[d1,d2,d3,d4,d5,d6]
#
# html = HtmlWriter()
# html.writeHTMLresponse("hellohello", response)
