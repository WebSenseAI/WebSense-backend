import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from webscrapping.sitemapExtractor import get_robots_results, fetch_all_sitemap_paths, mine_pages_form_sitemap


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
        robots_results = get_robots_results(self.domain.geturl())
        
        # if no robots or sitemap page exists then BFS
        if robots_results and not force_BFS:
            # THERE IS A SITEMAP IN ROBOTS.TXT
            
            # list all the non-INDEX sitemaps
            sitemap_paths = fetch_all_sitemap_paths(robots_results)
            
            # Extract URLs from sitemaps
            self.sites_reached = mine_pages_form_sitemap(sitemap_paths)
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

    def save(self, path=None):
        """Dev Tool : saves the crawled sites into a .txt file"""
        if path is None:
            path = rf"data/{self.domain.netloc}"
        
        with open(path + ".txt", 'w') as f:
            f.write("\n".join(self.sites_reached))

        print("SAVED SUCCESFULLY")
