import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from config import BASE, AJAX_URL, OUTPUT_DIR

# fetch a page of PDF links
async def fetch_page(session, page_num, year_id='88'):

    # prepare the form data to send to CBSL website
    payload = {
        "view_name": "price_report",
        "view_display_id": "block_1",
        "view_path": "node/144",
        "view_base_path": "publications/price",
        "pager_element": 0,
        "page": page_num,
        "field_year_tid": year_id,
        "field_month_tid": "All",
    }

    # send request to CBSL API
    async with session.post(AJAX_URL, data=payload) as response:

        # check if request was successful
        if response.status != 200:
            print(f"Failed to fetch page {page_num}: HTTP {response.status}")
            return []
        
        # get JSON response
        json_data = await response.json()

        # find HTML content in the JSON response
        html_content = None

        for item in json_data:
            if item.get("command") == "insert":
                html_content = item.get("data")
                break
        
        # If no HTML found, return empty list
        if not html_content:
            print(f"No HTML content found on page {page_num}")
            return []
        
        # parse HTML to extract PDF links
        soup = BeautifulSoup(html_content, "html.parser")
        pdf_links = []

        for link in soup.select("a[href$='.pdf']"):
            # get full URL
            pdf_url = urljoin(BASE, link['href'])

            # get the link text
            link_text = link.get_text(strip=True)

            # try to extract the date from text
            date_object = None
            try:
                # format "Daily Price Report - 01 January 2025"
                
                # date_part = link_text.split("-")[-1].strip()
                # date_object = datetime.strptime(date_part, '%d %B %Y')
                date_object = datetime.strptime(link_text.split("-")[-1].strip(), "%d %B %Y")

            except Exception:
                # if date parsing fails just use None
                pass

            pdf_links.append((date_object, pdf_url))
        
    return pdf_links
    
async def download_pdf(session, date_obj, url):

    # create file name from the date use unknown if date is null
    if date_obj:
        filename = f"{date_obj.strftime('%Y-%m-%d')}.pdf"
    else:
        filename = "unknown_date.pdf"

    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # full path where the file be saved
    output_path = os.path.join(OUTPUT_DIR, filename)


    # skip if the file already exists
    if os.path.exists(output_path):
        print(f"File already exists, skipping: {output_path}")
        return
    
    try:
        # download the pdf
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to download {url}: HTTP {response.status}")
                return
            
            # read the content
            pdf_content = await response.read()

            # save to file
            with open(output_path, "wb") as file:
                file.write(pdf_content)
                print(f"Saved {output_path}")

    except Exception as e:
        print(f"Error downloading {url}: {e}")

    
async def main():
    async with aiohttp.ClientSession() as session:

        # collect all pdf links from multiple pages
        all_links = []
        current_page = 0

        print("Fetching PDF links from all pages...")

        # keep fetching links until no more links are found
        while True:
            reports = await fetch_page(session, current_page)

            # if no reports were found
            if not reports:
                print(f"No more reports found at page {current_page}. Stopping.")
                break
            
            print(f"Found {len(reports)} reports on page {current_page}")
            all_links.extend(reports)
            current_page += 1

            # Wait 1 second between requests to be polite to the server
            await asyncio.sleep(1)

        print(f"Total pdfs found: {len(all_links)}")


        # download the files
        print("Starting PDF downloads...")

        # limit to 5 simultanous downloads to avoid overwhelming the server
        download_limit = asyncio.Semaphore(5)

        async def download_with_limit(date_obj, url):
            async with download_limit:
                await download_pdf(session, date_obj, url)

        # create download for all pdfs
        download_tasks = [
            download_with_limit(date_obj, url)     
            for date_obj, url in all_links       
        ]

        # run all download tasks
        await asyncio.gather(*download_tasks)

        print(f"All downloads completed. Saved in {OUTPUT_DIR}")
            
if __name__ == "__main__":
    asyncio.run(main())

