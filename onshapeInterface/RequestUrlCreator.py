# This creates the URL request to send to the API, excluding the payload
# Use setRequest() and setCategory() based on the Glassworkd API (google)

class OnshapeUrl:
    def __init__(self, url):
        self.elementID = None
        self.workspaceID = None
        self.documentID = None
        self.wvm = None
        self.parseStudioURL(url)

    def parseStudioURL(self, url):
        index = url.find("document")
        index += 1
        closingIndex = url.find("/", index)
        index = closingIndex + 1
        closingIndex = url.find("/", index)
        self.documentID = url[index: closingIndex]

        index = url.find("w/")
        self.wvm = "w"
        if index == -1:
            index = url.find("v/")
            self.wvm = "v"
        if index == -1:
            index = url.find("m/")
            self.wvm = "m"
        index += 1
        closingIndex = url.find("/", index)
        index = closingIndex + 1
        closingIndex = url.find("/", index)
        self.workspaceID = url[index:closingIndex]

        index = url.find("e/")
        if index != -1:
            index += 1
            closingIndex = url.find("/", index)
            index = closingIndex + 1
            self.elementID = url[index:]


def getURL(category : str, request, document: str, workspace: str, wvm: str, element: str = None):
    s = "https://cad.onshape.com/api/"
    s += category
    s += "/d/" + document
    s += "/" + wvm + "/"
    # if use_version:
    #     s += "/v/"
    # else:
    #     s += "/w/"
    s += workspace
    if element is not None:
        s += "/e/" + element
    if request is not None:
        s += "/" + request
    return s

