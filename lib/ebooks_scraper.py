from urllib.parse import urlparse, urlunparse
import requests as req
from playwright.async_api import async_playwright
from PyPDF2 import PdfMerger
import xml.etree.ElementTree as ET
import os

class EbookScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.Pages_dir = "epub/EPUB/"
        self.Package_Name = "package.xml"
        self.Page_content = None
    
    def normalize_url(self):
        parsed = urlparse(self.base_url)
        clean_path = parsed.path

        if clean_path.endswith("index.html"):
            clean_path = clean_path.replace("index.html", "")

        if not clean_path.endswith("/"):
            clean_path += "/"

        clean_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            clean_path,
            '', '', ''  # params, query, fragment
        ))
        return clean_url
    
    def validate_url(self):
        clean_url = self.normalize_url()
        try:
            response = req.get(clean_url).status_code
        
            if response != 200:
                print("Error: Unable to access the URL. Please check the URL and try again.")
                exit()

            if not clean_url.startswith("http://") and not clean_url.startswith("https://"):
                print("Error: Invalid URL. Please enter a valid URL starting with http:// or https://")
                exit()

            responseOfPagesList = req.get(clean_url + self.Pages_dir + self.Package_Name)

            if responseOfPagesList.status_code != 200:
                print("Error: Unable to access the package.xml file. Please check the URL and try again.")
                exit()

            self.Page_content = responseOfPagesList.content
            return clean_url
    
        except Exception as e:
            print(f"Error: {e}")
            exit()

    def PDFnameExtractor(self):
        Pages = self.Page_content
        ns = {
            'opf': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        root = ET.fromstring(Pages)
        element = root.find("opf:metadata/dc:title", ns)
        return element.text.strip() if element is not None and element.text else "Unknown Title"
    
    def PagesExtractor(self):
        Pages_list = []
        Pages = self.Page_content
        ns = {'opf': 'http://www.idpf.org/2007/opf'}
        ET.register_namespace('', "http://www.idpf.org/2007/opf")
        root = ET.fromstring(Pages)
        elements = root.find("opf:manifest", ns)
        for element in elements:
            if element.attrib["media-type"] == "application/xhtml+xml":
                Pages_list.append(element.attrib["href"])
        print(f"✅ Found {len(Pages_list)} pages to convert.")
        return Pages_list
    
    async def html_to_pdf(self,playwright, url, pdf_path):
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.pdf(path=pdf_path, format="A4")
        await browser.close()
    
    async def convert_all(self):
        temp_pdfs = []
        Extract_Pages = self.PagesExtractor()
        async with async_playwright() as p:
            for idx, file in enumerate(Extract_Pages, 1):
                url_full = self.base_url + self.Pages_dir + file
                temp_pdf = f"temp_{idx}.pdf"
                temp_pdfs.append(temp_pdf)
                print(f"📥 Converting page {idx}/{len(Extract_Pages)}: {file}")
                await self.html_to_pdf(p, url_full, temp_pdf)

        # دمج كل PDF في واحد
        merger = PdfMerger()
        for pdf in temp_pdfs:
            merger.append(pdf)

        output_pdf = self.PDFnameExtractor() + ".pdf"
        merger.write(output_pdf)
        merger.close()
        print(f"🎉 All pages merged into {output_pdf}")

        # حذف الملفات المؤقتة
        for pdf in temp_pdfs:
            os.remove(pdf)