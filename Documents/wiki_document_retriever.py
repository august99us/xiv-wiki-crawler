import urllib
import urllib.request

class WikiDocumentRetriever:
    wiki_base_url = "https://ffxiv.consolegameswiki.com"

    def __init__(self):
        pass

    def retrieve_document(self, path) -> str:
        # Retrieve the html on the page
        req = urllib.request.Request(self.wiki_base_url + path, headers={'User-Agent' : "UriangerBot"}) 
        con = urllib.request.urlopen(req)
        html_bytes = con.read()
        html = html_bytes.decode("utf-8")
        return html