# Tesla Service Manual Downloader
The Tesla Service Manual Downloader is a command line utility
for downloading the Tesla service manuals for offline use.

## Setup
The downloader requires [Python 3](https://www.python.org/) to run.
The process for installing depends on your operating system. The
library `requests` is also required, which can be installed with the following:
```bash
python3 -m pip install requests
```
or
```bash
cd /path/to/project/
python3 -m pip install -r requirements.txt
```

*On Windows*, use `python` instead of `python3` if the default install is used.<br>
*On Linux*, you may need to install `pip` (**P**ackage **I**nstaller for **P**ython).
This varies based on your distro. Ubuntu is `sudo apt install python3-pip`.

## Usage
### Downloading
The program runs with the `download.py` file. There are 3 parameters required:
* The URL of the page to download. For example, the Model Y service manual is
  https://service.tesla.com/docs/ModelY/ServiceManual/en-us/
* The directory to save to. It can be anything your file system will accept, but
  it must be unique and ideally readable. For example, `ModelYServiceManual`.
* Your session cookie used to fetch the service manual. **This is the hardest part
  to fetch and your session cookie allows access to your account. Do not share it
  and avoid sharing it to a file for this. If you do not trust this application 
 with it, do not run it.**
  * In Chrome, this can be viewed by going to the Developer Console on the page
    of the service manual (like https://service.tesla.com/docs/ModelY/ServiceManual/en-us/),
    go to the `Network` tab, reload the page if there is no entries, and copy the entire
    `Cookie` header under the `Request Headers`. It is long.

With the previous requirements, run the `download.py` script either by double-clicking
it (assuming your Operating System allows it) or running `python download.py` on Windows
or `python3 download.py` on macOS/Linux in the command line. You will be prompted
for the parameters previously stated. If it shows an error or instantly closes,
make sure the `Setup` section was completed.

If it runs, the output will look like the following including your input:
```
Enter a service manual URL to download (ex: https://service.tesla.com/docs/ModelY/ServiceManual/en-us/): https://service.tesla.com/docs/BodyRepair/Body_Repair_Procedures/Model_Y/HTML/en-us/
Enter a directory name to save to (ex: ModelYServiceManual): ModelYBodyRepairProcedures
Enter your cookie the web browser normally sends to fetch the service manual (ex: lang=en-US; _ga=...): lang=en-US; _ga=[REDACTED] ...
(Download output)
```

After the parameters are entered, the application will download the files in 2 phases:
1. Phase 1: Only the HTML files are downloaded.
2. Phase 2: All other files are downloaded. The HTML files are used to get a full list
   of files to download for this phase.

The time it takes to download and the size of the files vary by the target download.
The Model Y Service Manual is 2.22GB while the Model Y Body Repair Procedures
is only 124MB at the time of writing. Download times may vary based on internet connection
but are limited by Tesla's response times.

### Viewing
The `index.html` file in the download directory is the root file for viewing the service
manual. It can be viewed directly as a file. However - search will not work since it needs
to fetch a local file, which your browser will most likely block. To get around this, you
can set up a simple HTTP server to host the files on your system. Running `python3 -m http.server`
in a command line of the directory for the download and going to `localhost:8000` in your
browser will work.

## Notes
* This tool is not supported or endorsed by Tesla. Downloading local copies of the service
  manual is currently not supported by Tesla and puts a sizable load on the servers to do.
  Account activity may be logged when doing this.
* Downloading any other localization other than `en-us` is not tested. If changes are
  required, please create a pull request with the changes to make other locales work.
* Download only the service manuals you need. Downloading a lot more than you need may be
  viewed as too excessive and your subscription may be ended.
* **Do not distribute the downloaded files.**

## License
This project is available under the terms of the MIT License. See
[LICENSE](LICENSE) for details.