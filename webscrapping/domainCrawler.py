import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ElementTree
import xmltodict
import pandas as pd
import xml

class Crawler:
    """
        Crawler class is used to crawl through the pages of a site.
    """

    def __init__(self, domain, blacklist=[], iterations=100, expensive=True):
        self.domain = urlparse(domain)
        self.blacklist = blacklist  # list of pages that we must not crawl
        self.iterations = iterations  # BFS iteration upper limit
        self.sites_reached = []  # sites reached/crawled
        self.sitemap_paths = []  # sitemap paths
        self.expensive = expensive  # if true, then some method may be time-consuming

    def get_reached_sites(self):
        """'Return reached sites, i.e. the result of crawling"""
        return self.sites_reached
    

    def crawl(self, force_BFS = False):
        """The primary method that will be used for site-crawling

        Parameters
        ----------
        force_BFS : bool, optional
            Force the algorithm to use BFS discovery (default False)
        """
        
        # Get sitemap data from robots.txt
        self.get_robots_results()
        
        # if no robots or sitemap page exists then BFS
        if self.robots_sitemaps and not force_BFS:
            # THERE IS A SITEMAP IN ROBOTS.TXT
            
            # list all the non-INDEX sitemaps
            self.fetch_all_sitemap_paths()
            
            # Extract URLs from sitemaps
            self.get_page_urls()
        else:
            # Start BFS discovery
            self.BFS_discover()


    def BFS_discover(self,fresh=True):
        """Uses Breadth-First Search algorithm to crawl the pages of a website.

        Parameters
        ----------
        fresh : bool, optional
            Indicates whether the discovery adds to sites_reached,
            or starts from scractch (default True)
        """

        def is_url_invisited(_url):
            """Nested method to see if a url is already visited"""
            return _url not in visited and _url + '/' not in visited

        # already visited pages
        visited = set()
        # If not fresh, then already visited pages data is re-used
        if not fresh:
            visited = set(self.sites_reached)

        # queue starts with the base url
        queue = [self.domain.geturl()]
        # iteration counter
        n = 0

        while queue and n < self.iterations:
            url = queue.pop(0)
            if url not in visited:
                visited.add(url)
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    for link in soup.find_all("a", href=True):
                        full_url = urljoin(url, link["href"])
                        if self.is_valid_url(full_url) and is_url_invisited(full_url):                    
                            queue.append(full_url)

                except requests.exceptions.RequestException as e:
                    print(f"Request failed crawling to {url}:\n {e}")
            n += 1

        self.sites_reached += list(visited)



    def is_valid_url(self, url):
        """Checks if a given URL is valid with respect to the base domain
        
        Parameters
        ----------
        url : str
            The url whose validity is to be checked
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.netloc == self.domain.netloc

    
    def get_robots_results(self):
        """
        Extract the sitemap from robots.txt.
        Sets robots_sitemaps attr with the extracted sitemaps
        None if no robots.txt or sitemap.xml exists.

        """
        url_robots = urljoin(self.domain.geturl(), 'robots.txt')
        rp = RobotFileParser()
        rp.set_url(url_robots)
        rp.read()
        sitemaps = rp.site_maps()
        self.robots_sitemaps = sitemaps
    
    def fetch_all_sitemap_paths(self):
        """Fills the sitemap_paths with only non-INDEX sitemaps."""
        
        robots_results = self.robots_sitemaps
        all_paths = []
        for path in robots_results:
            path_type = self.get_sitemap_type(path, crucial=True) 
            print(path, path_type)
            if path_type == 'INDEX':
                all_paths += self.expand_sitemap_index(path)
            elif  path_type == 'SITEMAP':
                all_paths += [path]
            else:
                continue

        self.sitemap_paths = all_paths

    def get_sitemap_type(self, path, crucial= False):
        """
        Identifies the type of the sitemap.
        The type can be either INDEX, SITEMAP or None.
        If crucial is selected, then time-expensive method is employed
        regardless of the value of 'expensive' attribute.
        """

        if self.expensive or crucial:
            # THE EXPENSIVE WAY
            xml = self.get_and_turn_xml_to_dict(path)
            if 'sitemapindex' in xml:
                return "INDEX"
            elif 'urlset' in xml:
                return "SITEMAP"
            return None
        else:
            # THE CHEAP WAY
            if 'index' in path:
                return "INDEX"
            else:
                return "SITEMAP"
    
    def get_page_urls(self):
        """
        From the list of non-INDEX sitemaps, extracts the page URLs.
        """

        for sitemap in self.sitemap_paths:
            sitemap_dict = self.get_and_turn_xml_to_dict(sitemap)
            pages = sitemap_dict['urlset']['url']
            if type(pages) == list:
                self.sites_reached += [page['loc'] for page in pages]
            else:
                self.sites_reached += [pages['loc']]


    def get_and_turn_xml_to_dict(self, path):
        """
        Gets the xml from a URL and parses it to dict.
        If the data in URL is not XML-parseable then it returns None
        
        Parameters
        ----------
        path : str
            The URL at which the XML is located
        
        Returns
        -------
        dict or None
        """
        sitemap_xml = requests.get(path).text
        try:
            sitemap_dict = xmltodict.parse(sitemap_xml)
            return sitemap_dict
        except xml.parsers.expat.ExpatError:
            print(f"ERROR OCCURED TRYING TO PARSE {path}")
            return None
        
    def expand_sitemap_index(self, index_path):
        """
        Given a path of a sitemap INDEX, extracts the actual SITEMAPS.
        if the INDEX contains other INDEX, then recursively extracts them too.

        Parameters
        ----------
        path : str
            The path of the INDEX
        
        Returns
        -------
        list
            List of non-INDEX sitemaps.
        """
        sitemap_content = self.get_and_turn_xml_to_dict(index_path)
        if sitemap_content is None:
            return [] 
        sm_dicts = sitemap_content['sitemapindex']['sitemap']
        sm_values = [sm['loc'] for sm in sm_dicts]
        expansion = []
        for sitemap in sm_values:
            if self.get_sitemap_type(sitemap) == 'INDEX':
                print(f'expanding {sitemap}')
                expansion += self.expand_sitemap_index(sitemap)
            else:
                print(f'added {sitemap}')
                expansion += [sitemap]
        return expansion
    
    def save(self, path=None):
        """Dev Tool : saves the crawled sites into a .txt file"""
        if path is None:
            path = rf"data/{self.domain.netloc}"
        
        with open(path + ".txt", 'w') as f:
            f.write("\n".join(self.sites_reached))

        print("SAVED SUCCESFULLY")
