import argparse
import urllib.request
import sys
import os
from pathlib import Path

from fake_useragent import UserAgent    # "fake-useragent" by hellysmile
from bs4 import BeautifulSoup           # "beautifulsoup4" by Leonard Richardson

# _____ ARGUMENTS PARSER _______________________________________________________________________________________________


parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description='Download 1920x1080p images from Windows 10 Spotlight site.',
    add_help=True,
    epilog='GitHub Page: https://github.com/locobastos/windows-10-spotlight-downloader'
)
parser.add_argument('-f', '--full-update',
                    action='store_true',
                    dest='full_update',
                    help='Update the library. Browse all images but do not re-download.')
parser.add_argument('-n', '--no-download',
                    action='store_true',
                    dest='no_download',
                    help='True if you want to list photos URL only')
parser.add_argument('-o', '--output-directory',
                    type=str,
                    action='store',
                    dest='output_directory',
                    help='The folder to save images into')
parser.add_argument('-p', '--page-number',
                    type=int,
                    action='store',
                    dest='page_number',
                    default=0,
                    help='The page number to start to download')
parser.add_argument('-u', '--update',
                    action='store_true',
                    dest='update',
                    help='Update the library. Stop at the first image already downloaded.')
parser.add_argument('-w', '--website',
                    type=str,
                    action='store',
                    dest='website',
                    default='https://windows10spotlight.com',
                    help='If this script support other websites, enter its URL here')
args = parser.parse_args()


# _____FUNCTiONS________________________________________________________________________________________________________


def get_html_source_code_from(url):
    """
    Connect to the URL and return the HTML source code.
    :param url: the url we want the source code
    :return: the source code
    """
    response = ""
    try:
        request = urllib.request.Request(url, headers=user_agent_header)
        response = urllib.request.urlopen(request)
    except (urllib.request.HTTPError, urllib.request.URLError):
        print("[ERROR_01] This website is not compatible with my python script or the page number does not exist.")
        sys.exit(1)
    except ValueError as value_error:
        if value_error.args[0].startswith("unknown url type"):
            print("[ERROR_02] An URL starts with http:// or https://")
            sys.exit(1)
    return BeautifulSoup(response.read(), "html.parser") if response != "" else ""


def browse_windows10spotlight(url):
    """
    Connects to the given URL then parse the HTML source code to retrieve, in the HTML tags <a></a>,
    the HTTP link of the spotlight image to download.
    :param url: The URL of the current page (e.g. https://windows10spotlight.com/page/123)
    """
    if not args.no_download:
        print("Grabbing: " + url)
    soup = get_html_source_code_from(url)

    # We have 2 possibilities:
    #   1) We are on a "page" page (e.g. https://windows10spotlight.com/page/123)
    #      ==> We have "h2" HTML tags
    if len(soup.find_all('h2')) > 0:
        for h2_tag in soup.find_all('h2'):
            # h2_tag is a Tag type if it has <a href> tag (e.g. <h2><a href='...'></a></h2>)
            if not isinstance(h2_tag.contents[0], str):
                browse_windows10spotlight(h2_tag.contents[0]['href'])
            # h2_tag is a string if it has no <a href> tag (e.g. <h2>This is a text</h2>)
            else:
                args.page_number += 1
                browse_windows10spotlight(args.website + '/page/' + str(args.page_number))
    #   2) We are on a "images" page (e.g https://windows10spotlight.com/images/a7fb8314253bb986d7f4676a324d2c25)
    #      ==> We do not have "h2" HTML tag
    elif len(soup.find_all('h2')) == 0:
        download_spotlight_image(soup.find('figure').contents[0]['href'])


def download_spotlight_image(href_link):
    """
    Downloads the spotlight image into the spotlight_images_location directory.
    :param href_link: The download URL.
    """
    posted_year = href_link.split('/')[5]
    posted_month = href_link.split('/')[6]
    hash_name = href_link.split('/')[7]
    file_url = "https://windows10spotlight.com/wp-content/uploads/" + posted_year + "/" + posted_month + "/" + hash_name
    if args.no_download:
        print(file_url)
    else:
        request = urllib.request.Request(file_url, headers=user_agent_header)
        file_data = urllib.request.urlopen(request)
        jpg_file_name = posted_year + '-' + posted_month + '-' + hash_name
        full_file_path = spotlight_images_location + "/" + jpg_file_name

        # The file exists and is not empty and we just want an update = exit program
        if args.update and os.path.isfile(full_file_path) and os.stat(full_file_path).st_size != 0:
            sys.exit("Update finished")
        # The file exists and is not empty and we want a full update = continue but don't download file
        elif args.full_update and os.path.isfile(full_file_path) and os.stat(full_file_path).st_size != 0:
            pass
        # The file does not exist or is empty = download it
        else:
            with open(spotlight_images_location + "/" + jpg_file_name, 'wb') as image_jpg_file:
                # The file does not exist, we download it
                image_jpg_file.write(file_data.read())
                image_jpg_file.close()


# _____MAiN_____________________________________________________________________________________________________________

user_agent = UserAgent()
user_agent_header = {'User-Agent': user_agent.chrome}

if len(sys.argv) > 0:
    # By default, if -u or --update is specified, I do an update
    if args.update is False:
        args.update = True

    # And if -f or --full-update is specified, I disable --update
    if args.full_update is True:
        args.update = False

    # If -o or --output-directory is not specified, I use the script folder
    if args.output_directory is not None:
        if not os.path.isdir(args.output_directory):
            Path(args.output_directory).mkdir(mode=0o775, parents=True, exist_ok=True)
        spotlight_images_location = args.output_directory
    else:
        spotlight_images_location = os.path.dirname(sys.argv[0])

    if isinstance(args.page_number, str):
        args.page_number = int(args.page_number)

    browse_windows10spotlight(args.website + "/page/" + str(args.page_number))
else:
    parser.print_help()
