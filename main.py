import asyncio
import os
import time
from lib.ebooks_scraper import EbookScraper

# لإضافة ألوان
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# تنظيف الشاشة
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Header
def print_header():
    print(Colors.HEADER + "╔══════════════════════════════════════╗" + Colors.RESET)
    print(Colors.HEADER + "║        📚 HU Book Extractor          ║" + Colors.RESET)
    print(Colors.HEADER + "╚══════════════════════════════════════╝\n" + Colors.RESET)

async def run():
    clear()
    print_header()

    base_url = input(Colors.CYAN + "🔗 Enter Book URL:\n> " + Colors.RESET).strip()

    try:
        scraper = EbookScraper(base_url)

        print(Colors.YELLOW + "\n⏳ Validating URL..." + Colors.RESET)
        time.sleep(0.8)
        scraper.validate_url()
        print(Colors.GREEN + "✅ URL validated" + Colors.RESET)

        print(Colors.YELLOW + "📦 Fetching metadata..." + Colors.RESET)
        time.sleep(0.5)
        title = scraper.PDFnameExtractor()
        print(Colors.GREEN + f"📄 Book Title: {title}" + Colors.RESET)

        pages = scraper.PagesExtractor()
        print(Colors.GREEN + f"\n📚 Found {len(pages)} pages" + Colors.RESET)

        confirm = input(Colors.CYAN + "\n🚀 Start conversion? (y/n): " + Colors.RESET).lower()
        if confirm != "y":
            print(Colors.RED + "❌ Cancelled" + Colors.RESET)
            return

        print(Colors.YELLOW + "\n🚀 Starting conversion...\n" + Colors.RESET)

        # تحويل حقيقي
        await scraper.convert_all()

        print(Colors.GREEN + f"\n🎉 Done successfully! Saved as: {title}.pdf" + Colors.RESET)

    except Exception as e:
        print(Colors.RED + f"\n❌ Error: {e}" + Colors.RESET)

if __name__ == "__main__":
    asyncio.run(run())