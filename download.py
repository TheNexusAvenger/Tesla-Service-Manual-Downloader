"""
TheNexusAvenger

Downloads local copies of the Tesla service manuals.
"""

import requests
import os
import re
from requests import Response


class ServiceManualDownloadContext:
    def __init__(self):
        """Creates the download context.
        """

        self.phase1CheckedHtmlFiles = []
        self.htmlFiles = []
        self.otherFiles = ["index.json"]
        self.cookie = ""
        self.baseUrl = ""
        self.parentDirectory = ""


    def fetch(self, url: str) -> Response:
        """Fetches a web resource.

        :param url: URL to download from.
        :return: The response for the URL.
        """

        return requests.get(url, headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie": self.cookie
            })


    def downloadFile(self, url: str, path: str) -> None:
        """Downloads a file with the session cookie.

        :param url: URL to download from.
        :param path: Path to write to.
        """

        # Create the directories.
        fullPath = os.path.realpath(os.path.join(self.parentDirectory, path))
        if not os.path.exists(os.path.dirname(fullPath)):
            os.makedirs(os.path.dirname(fullPath))

        # Download the file.
        if not os.path.exists(fullPath):
            with open(fullPath, "wb") as file:
                file.write(self.fetch(url).content)


    def checkCookie(self) -> None:
        """Checks if the session cookie is valid.
        """

        if "error?message=" in self.fetch(self.baseUrl).url:
            raise AssertionError("Main page returned an error. The session cookie may be incorrect.")


    def checkHtmlFile(self, path: str) -> None:
        """Checks the sources of an HTML file.

        :param path: Path of the HTML file to check.
        """

        # Return if the file was checked.
        if path in self.phase1CheckedHtmlFiles:
            return
        if not path in self.htmlFiles:
            self.htmlFiles.append(path)
        self.phase1CheckedHtmlFiles.append(path)

        # Download the file.
        print("[Phase 1 (HTML Files): " + str(len(self.phase1CheckedHtmlFiles)) + "/" + str(len(self.htmlFiles)) + "] Downloading " + path)
        self.downloadFile(self.baseUrl + path, path)

        # Check the new HTML files.
        newHtmlFiles = []
        for source in self.getPageSources(path):
            if "html" in source:
                if not source in self.htmlFiles:
                    self.htmlFiles.append(source)
                    newHtmlFiles.append(source)
            else:
                if not source in self.otherFiles:
                    self.otherFiles.append(source)
        for path in newHtmlFiles:
            self.checkHtmlFile(path)


    def getPageSources(self, path: str) -> list:
        """Gets the sources referenced in an HTML file.

        :param path: The path of the HTML file to read.
        :return: The sources of the page to download.
        """

        # Parse the sources in the HTML file.
        fullPath = os.path.realpath(os.path.join(self.parentDirectory, path))
        rawSources = []
        with open(fullPath, encoding="utf8") as file:
            data = file.read()
            for match in re.findall("href=\"([^\"]+)\"", data):
                if ":" in match or match == "/" or match.startswith("#"):
                    pass
                else:
                    rawSources.append(match)
            for match in re.findall("src=\"([^\"]+)\"", data):
                if ":" in match or match == "/" or match.startswith("#"):
                    pass
                else:
                    rawSources.append(match)

        # Process the sources.
        sources = []
        for source in rawSources:
            if "#" in source:
                source = source.split("#")[0]
            while source.startswith("./"):
                source = source[2:]
            if not source in sources and not source.startswith("."):
                sources.append(source)
        return sources


    def downloadOtherFiles(self) -> None:
        """Downloads the other (non-HTML) files for the page.
        """

        for i in range(0, len(self.otherFiles)):
            path = self.otherFiles[i]
            print("[Phase 2 (Other Files): " + str(i + 1) + "/" + str(len(self.otherFiles)) + "] Downloading " + path)
            self.downloadFile(self.baseUrl + path, path)


    def downloadManual(self) -> None:
        """Downloads the manual.
        """

        self.checkCookie()
        self.checkHtmlFile("index.html")
        self.downloadOtherFiles()


if __name__ == '__main__':
    # Prompt for the service manual URL.
    url = input("Enter a service manual URL to download (ex: https://service.tesla.com/docs/ModelY/ServiceManual/en-us/): ")

    # Prompt for the save location.
    path = input("Enter a directory name to save to (ex: ModelYServiceManual): ")

    # Prompt for the cookie.
    cookie = input("Enter your cookie the web browser normally sends to fetch the service manual (ex: lang=en-US; _ga=...): ")

    # Run the fetcher.
    context = ServiceManualDownloadContext()
    context.baseUrl = url
    context.parentDirectory = path
    context.cookie = cookie
    context.downloadManual()