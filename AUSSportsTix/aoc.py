# Acknowledgement of Country

# References listed here for general and below each section for specifics.
# https://www.commonground.org.au/article/first-nations-place-names-of-major-cities


# Data for AoC
CAPITAL_CITIES = {
    'brisbane': {
        'city': 'Brisbane',
        'place_name': 'Meanjin',
        'custodians': 'Turrbal and Jagera (Yuggera) people',
        'names': ['Turrabal', 'Turrubul', 'Jagera', 'Yuggera', 'Yagara', 'Yugara'],
        'contested': 'Jangera and Turrbal being seperate people is debated, including spelling variations. Referencing both peoples is important',
        'source': 'Queensland Parliamentary Counsel acknowledgement',
    },
    # https://www.turrbal.com.au/our-story
    # https://www.oqpc.qld.gov.au/acknowledgement-country

    'sydney': {
        'city': 'Sydney',
        'place_name': None,
        'custodians': 'Garidgal people of the Eora Nation',
        'names': ['Cadigal', 'Gadigal'],
        'contested': 'Gadical Country is the city centre. Greater Sydney also covers the Darug, Dharawal, Guringai people.',
        'source': 'City of Sydney; Metropolitan Local Aboriginal Land Council',
    },
    # https://www.aboriginalheritage.org/history/clans-of-sydney/
    # https://metrolalc.org.au/about-us/our-land/

    'melbourne': {
        'city': 'Melbourne',
        'place_name': 'Naarm',
        'custodians': 'Wurundjeri Woi-wurrung and Bunurong peoples of eastern Kulin',
        'names': ['Wurundjeri', 'Bunurong','Boon Wurrung', 'Boonwurrung'],
        'contested': 'Boundaries between Wurundjeri and Bunurong Country were redrawn in 2021.',
        'source': 'City of Melbourne acknowledgement',
    },
    # https://www.firstpeoplesrelations.vic.gov.au/acknowledgement-traditional-owners
    # https://aboriginal-map.melbourne.vic.gov.au/extras/acknowledgments

    'adelaide': {
        'city': 'Adelaide',
        'place_name': 'Tarntanya',
        'custodians': 'Kaurna people',
        'names': ['Kaurna'],
        'contested': 'Kaurna native title record over the Adelaide area was recognised by the Federal court in 2018.',
        'source': 'City of Adelaide; Kaurna Yerta Aboriginal Corporation',
    },
    # https://kyac.org.au/about-kaurna/
    # https://www.cityofadelaide.com.au/about-adelaide/kaurna-heritage/

    'perth': {
        'city': 'Perth',
        'place_name': 'Boorloo',
        'custodians': 'Whadjuk Noongar people',
        'names': ['Whadjuk'],
        'contested': 'Noongar is the wider nation of the south-west, where as Whadjuk is the group whos home is Perth',
        'source': 'City of Perth; South West Aboriginal Land and Sea Council',
    },
    # https://www.indigenous.gov.au/community/perth
    # https://www.abc.net.au/education/the-traditional-owners-of-perth-whadjuk-country/13868228
    # https://perth.wa.gov.au/community/community-services-and-facilities/elders-advisory-group

    'hobart': {
        'city': 'Hobart',
        'place_name': 'nipaluna',
        'custodians': 'muwinina people and the palawa people',
        'names': ['muwinina', 'palawa', 'Tasmanian Aboriginal'],
        'contested': 'City of Hobart has acknowledged the palawa people and loss of the muwinina people. pala kani words are written in lower case by choice of its people',
        'source': 'City of Hobart Aboriginal progam; Tasmanian Aboriginal Centre',
    },
    # https://tacinc.com.au/about-us/
    # https://www.hobartcity.com.au/Council/Vision-and-strategies/Strategies-plans-and-reports/Country-Culture-People

    'darwin': {
        'city': 'Darwin',
        'place_name': 'Garramilla',
        'custodians': 'Larrakia people',
        'names': ['Larrakia'],
        'contested': 'Larrakia Country covers the darwin and coast region',
        'source': 'City of Darwin, Larrakia Nationa Aboriginal Corporation',
    },
    # https://aiatsis.gov.au/austlang/language/n21
    # https://ian.umces.edu/blog/engaging-with-the-belyuen-people-and-larrakia-people-traditional-owners-of-darwin-harbour-australia/
    # https://larrakia.com/about/the-larrakia-people/
    # https://www.darwin.nt.gov.au/community/about-darwin/history

    'canberra': {
        'city': 'Canberra',
        'place_name': None,
        'custodians': 'Ngunnawal people and other regions people',
        'names': ['Ngunnawal', 'Ngambri', 'Ngarigo'],
        'contested': 'ACT Government recognised the Ngunnawal people but a dispute from the Ngambri people was made. Recognition of the dispute is important, rather than taking a side.',
        'source': 'ACT Indigenous Protocol',
    },
    # https://www.act.gov.au/community/aboriginal-and-torres-strait-islander-peoples/indigenous-protocols-in-the-act?utm_medium=shorturl&utm_content=ngunnawal-country
    # https://www.ngunnawal.org/who-we-are

}

# First nation names people can use instead
ALIASES = {
    'meanjin': 'brisbane', 'naarm': 'melbourne', 'tarntanya': 'adelaide',
    'boorloo': 'perth', 'nipaluna': 'hobart', 'garramilla': 'darwin'
}

# finding the name
def find_country(city):
    """Return the entry for a capital city (English or First nations name), or none."""
    key = (city or '').strip().lower()
    key = ALIASES.get(key, key)
    return CAPITAL_CITIES.get(key)
