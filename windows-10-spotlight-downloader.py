import argparse
import urllib.error
import urllib.request
import sys
import os
import pathlib

from fake_useragent import UserAgent  # "fake-useragent-ex" by hellysmile
from bs4 import BeautifulSoup         # "beautifulsoup4" by Leonard Richardson


class Windows10SpotlightDownloader:

    def __init__(self, p_args_parsed: argparse.Namespace, p_script_dir: str):
        self.user_agent_header = {'User-Agent': UserAgent().chrome}

        # I do an update, by default, if "-u" or "--update" is not specified
        if p_args_parsed.update is False:
            self.update = True
        else:
            self.update = p_args_parsed.update

        if p_args_parsed.output_directory is None:
            self.output_directory = os.path.dirname(p_script_dir)
        else:
            self.output_directory = p_args_parsed.output_directory

        self.full_update = p_args_parsed.full_update
        self.no_download = p_args_parsed.no_download
        self.page_number = p_args_parsed.page_number
        self.website = p_args_parsed.website
        self.current_url = self.website + "/page/" + str(self.page_number)

        # I disable "--update" if "-f" or "--full-update" is specified
        if p_args_parsed.full_update is True:
            self.update = False

        if not os.path.isdir(self.output_directory):
            pathlib.Path(self.output_directory).mkdir(mode=0o775, parents=True, exist_ok=True)

        if isinstance(p_args_parsed.page_number, str):
            self.page_number = int(p_args_parsed.page_number)

    def __download_spotlight_image(self, href_link: str) -> None:
        """
        Downloads the spotlight image into the spotlight_images_location directory.
        :param: The download URL.
        :type: str
        :return: None
        """
        posted_year = href_link.split('/')[5]
        posted_month = href_link.split('/')[6]
        hash_name = href_link.split('/')[7]
        file_url = "https://windows10spotlight.com/wp-content/uploads/" + posted_year + "/" + posted_month + "/" + hash_name
        if self.no_download:
            print(file_url)
        else:
            request = urllib.request.Request(file_url, headers=self.user_agent_header)
            file_data = urllib.request.urlopen(request)
            jpg_file_name = posted_year + '-' + posted_month + '-' + hash_name
            full_file_path = os.path.join(self.output_directory, jpg_file_name)

            # The file exists and is not empty, and we just want an update = exit program
            if self.update and os.path.isfile(full_file_path) and os.stat(full_file_path).st_size != 0:
                sys.exit("Update finished")
            # The file exists and is not empty, and we want a full update = continue but don't download file
            elif self.full_update and os.path.isfile(full_file_path) and os.stat(full_file_path).st_size != 0:
                pass
            # The file does not exist or is empty = download it
            else:
                with open(full_file_path, 'wb') as image_jpg_file:
                    # The file does not exist, we download it
                    image_jpg_file.write(file_data.read())
                    image_jpg_file.close()

    def __get_html_source_code_from(self, url: str) -> BeautifulSoup:
        """
        Connect to the URL and return the HTML source code.
        :param: the url we want the source code
        :type: str
        :return: the source code
        """
        response = ""
        try:
            request = urllib.request.Request(url, headers=self.user_agent_header)
            response = urllib.request.urlopen(request)
        except (urllib.error.HTTPError, urllib.error.URLError):
            print("[ERROR_01] This website is not compatible with my python script or the page number does not exist.")
            sys.exit(1)
        except ValueError as value_error:
            if value_error.args[0].startswith("unknown url type"):
                print("[ERROR_02] An URL starts with http:// or https://")
                sys.exit(1)
        return BeautifulSoup(response.read(), "html.parser") if response != "" else ""

    def browse_windows10spotlight(self) -> None:
        """
        Connects to the given URL then parse the HTML source code to retrieve, in the HTML tags <a></a>,
        the HTTP link of the spotlight image to download.
        :param: The URL of the current page (e.g. https://windows10spotlight.com/page/123)
        :type: str
        :return: None
        """
        if not self.no_download:
            print("Grabbing: " + self.current_url)
            if "uncategorized" not in self.current_url:
                soup = self.__get_html_source_code_from(self.current_url)

                # We have 3 possibilities:
                #   1) We are on a "page" page (e.g. https://windows10spotlight.com/page/123)
                #      ==> We have "h2" HTML tags
                if len(soup.find_all('h2')) > 2:
                    for h2_tag in soup.find_all('h2'):
                        if len(h2_tag.string) > 1:
                            # h2_tag is a Tag type if it has <a href> tag (e.g. <h2><a href='...'></a></h2>)
                            if not isinstance(h2_tag.contents[0], str):
                                self.current_url = h2_tag.contents[0]['href']
                                self.browse_windows10spotlight()
                            # h2_tag is a string if it has no <a href> tag (e.g. <h2>This is a text</h2>)
                            else:
                                self.page_number += 1
                                self.current_url = self.website + '/page/' + str(self.page_number)
                                self.browse_windows10spotlight()
                #   2) We are on a "images" page (e.g https://windows10spotlight.com/images/a7fb8314253bb986d7f4676a324d2c25)
                #      ==> We do not have "h2" HTML tag
                elif len(soup.find_all('h2')) == 1:
                    self.__download_spotlight_image(soup.find('figure').contents[0]['href'])


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
                    type=pathlib.Path,
                    action='store',
                    dest='output_directory',
                    help='The folder to save images into')
parser.add_argument('-p', '--page-number',
                    type=int,
                    action='store',
                    dest='page_number',
                    default=1,
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
args_parsed = parser.parse_args()

if len(sys.argv) > 1:
    W10SL = Windows10SpotlightDownloader(args_parsed, sys.argv[0])
    W10SL.browse_windows10spotlight()
else:
    parser.print_help()
