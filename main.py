from scholarly import scholarly
from OSMPythonTools.nominatim import Nominatim
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt



def plot_citations(author_name):
    m = Basemap(projection='mill',lon_0=180)
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='coral',lake_color='aqua')

    search_query = scholarly.search_author(author_name)
    author = next(search_query).fill()
    for pub in author.publications:
        print('Title: ', pub.bib['title'])
        pub = pub.fill()
        for citation in pub.citedby:
            firstAuthorId = None
            while firstAuthorID is None or len(citation.author_ids) == 0:
                firstAuthorId = citation.author_ids.pop()
            if firstAuthorId is None:
                continue
            author = scholarly.search_author_id(firstAuthorId)
            lat, lon = get_location(author.affiliation)

            plt.plot(lat, lon)
    plt.show()



def get_location(affiliation):
    nominatim = Nominatim()
    res = nominatim.query(affiliation)[0]
    return (res['lat'], res['lon'])


if __name__ == '__main__':
    plot_citations('Anubhav Ashok')
    #get_location('Stanford University')
