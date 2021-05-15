# Windows 10 Spotlight Images Downloader
Windows 10 Spotlight Images is a WordPress website in which all Windows Spotlight images are shared. The URL is https://windows10spotlight.com

You can learn more here : https://windows10spotlight.com/about



This script allows you to download all images from this website.

### Usage

   ```
   usage: Windows10SpotlighDownloader.py [OPTIONS [OPTIONS]]
   
   OPTIONS
      -f, --full-update       Do a full update of your library = Check all images,
                              download the new ones but do not download the existing ones.

      -n, --no-download       Do not download images, just list URL.
      
      -o, --output-directory  The folder to save images into.
      
      -p, --page-number       The website page to start to download.
      
      -u, --update            Do an update of your library = Check all images,
                              download the new ones and exit program at the first existing ones.

      -w, --website           By default, the website is https://windows10spotlight.com
                              but if my script works with other websites, you can specify the URL here.
   
   DEFAULT BEHAVIOR
      Without argument, the behavior is the same as
       
          Windows10SpotlighDownloader.py --output-directory . --page-number 1 --update --website https://windows10spotlight.com
      
      In other words, it will update from page 1 on the script directory.
   ```

