import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from config import BASE, AJAX_URL, OUTPUT_DIR

# fetch a page of PDF links
async def fetch_page(session, page_num, year_id):
    """
    Fetch a single page of PDF links from the CBSL website.
    
    Args:
        session (aiohttp.ClientSession): The HTTP session to use for requests
        page_num (int): The page number to fetch (0-indexed)
        year_id (str): The CBSL year ID filter (e.g., "88" for 2025)
    
    Returns:
        list: A list of tuples containing (date_object, pdf_url) for each PDF found.
              Returns empty list if request fails or no PDFs found.
    """

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
    
async def download_pdf(session, date_obj, url, output_dir):
    """
    Download a single PDF file and save it to the specified directory.
    
    Args:
        session (aiohttp.ClientSession): The HTTP session to use for downloading
        date_obj (datetime): The date object for naming the file (or None if unknown)
        url (str): The full URL of the PDF to download
        output_dir (str): The directory path where the PDF should be saved
    
    Returns:
        None
    """

    # ensure folder exists
    os.makedirs(output_dir, exist_ok=True)

    # build filename
    if date_obj:
        filename = f"{date_obj.strftime('%Y-%m-%d')}.pdf"
    else:
        filename = "unknown_date.pdf"

    output_path = os.path.join(output_dir, filename)

    # skip if already downloaded
    if os.path.exists(output_path):
        print(f"Skipping {output_path} (already exists)")
        return

    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed {url}: HTTP {response.status}")
                return

            pdf_content = await response.read()
            with open(output_path, "wb") as f:
                f.write(pdf_content)
                print(f"Saved {output_path}")

    except Exception as e:
        print(f"Error downloading {url}: {e}")
    
async def main():
    """
    Main function that orchestrates the entire PDF scraping process.
    
    This function:
    1. Iterates through each year in the year_map
    2. Creates a dedicated output directory for each year
    3. Fetches all PDF links from all pages for that year
    4. Removes duplicate URLs (CBSL sometimes returns duplicates)
    5. Downloads all PDFs concurrently (max 5 at a time)
    6. Saves files in year-specific subdirectories
    
    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:

        # map CBSL year IDs to actual years
        year_map = {
            "88": 2025
        }

        # process each year separately
        for year_id, year_num in year_map.items():
            print(f"\nFetching reports for {year_num} (year_id={year_id})...")

            # make a folder for this specific year
            year_output_dir = os.path.join(OUTPUT_DIR, str(year_num))
            os.makedirs(year_output_dir, exist_ok=True)

            all_links = []
            current_page = 0

            print(f"Fetching PDF links for {year_num}...")

            # fetch all pages for this year
            while True:
                reports = await fetch_page(session, current_page, year_id)

                if not reports:
                    print(f"No more reports found at page {current_page} for {year_num}.")
                    break

                print(f"Found {len(reports)} reports on page {current_page} ({year_num})")
                all_links.extend(reports)
                current_page += 1
                await asyncio.sleep(1)

            print(f"Total PDFs found for {year_num}: {len(all_links)}")

            # download files for this year
            print(f"Starting downloads for {year_num}...")

            download_limit = asyncio.Semaphore(5)

            async def download_with_limit(date_obj, url):
                async with download_limit:
                    await download_pdf(session, date_obj, url, year_output_dir)
            
            # Deduplicate by URL to avoid duplicates (icon + text)
            unique_links = {}
            for date_obj, url in all_links:
                if url not in unique_links:
                    unique_links[url] = date_obj
                # else: duplicate, skip

            # Replace all_links with the cleaned version (fix tuple order)
            all_links = [(date_obj, url) for url, date_obj in unique_links.items()]



            # run all downloads (in parallel, max 5 at once)
            download_tasks = [
                download_with_limit(date_obj, url)
                for date_obj, url in all_links
            ]

            await asyncio.gather(*download_tasks)
            print(f"Completed downloads for {year_num}. Saved in {year_output_dir}")

            
if __name__ == "__main__":
    asyncio.run(main())

