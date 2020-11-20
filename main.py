from scholarly import scholarly
from OSMPythonTools.nominatim import Nominatim
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from fp.fp import FreeProxy
from scholarly import ProxyGenerator
from time import sleep

pg = ProxyGenerator()
proxy = FreeProxy(rand=True, timeout=1, country_id=['BR']).get()
pg.SingleProxy(http=proxy, https=proxy)
scholarly.use_proxy(pg)


def plot_citations(author_name):
    m = Basemap(projection='mill',lon_0=180)
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='coral',lake_color='aqua')

    search_query = scholarly.search_author(author_name)
    author = next(search_query).fill()
    print(author)
    for pub in [author.publications[0]]:
        print('Title: ', pub.bib['title'])
        pub = pub.fill()
        sleep(45)
        for citation in pub.citedby:
            print(citation)
            sleep(45)
            firstAuthorId = None
            while firstAuthorId is None or len(citation.bib['author_id']) == 0:
              firstAuthorId = citation.bib['author_id'].pop()
            if firstAuthorId is None:
              continue
            print(firstAuthorId)
            author = scholarly.search_author_id(firstAuthorId)
            sleep(45)
            lat, lon = get_location(author.affiliation)
            m.plot(float(lon), float(lat), marker='D')
    plt.show()



def get_location(affiliation):
    nominatim = Nominatim()
    res = nominatim.query(affiliation).toJSON()[0]
    return (res['lat'], res['lon'])


if __name__ == '__main__':
    plot_citations('Anubhav Ashok')
    #get_location('Stanford University')
