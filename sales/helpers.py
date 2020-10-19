from datetime import timedelta

from django.utils import timezone

from accountancy.helpers import sort_multiple
from cashbook.models import CashBookTransaction
from nominals.models import NominalTransaction
from vat.models import VatTransaction

from .models import Customer, SaleHeader, SaleLine

PERIOD = '202007'

# because Heroku doesn't have one unlike my local Linux OS
common_words_dictionary = [
    "Argo",
    "Argo's",
    "Argonaut",
    "Argonaut's",
    "Argonne",
    "Argonne's",
    "Argos",
    "Argos's",
    "Argus",
    "Argus's",
    "Ariadne",
    "Ariadne's",
    "Arianism",
    "Arianism's",
    "Ariel",
    "Ariel's",
    "Aries",
    "Aries's",
    "Arieses",
    "Ariosto",
    "Ariosto's",
    "Aristarchus",
    "Aristarchus's",
    "Aristides",
    "Aristides's",
    "Aristophanes",
    "Aristophanes's",
    "Aristotelian",
    "Aristotelian's",
    "Aristotle",
    "Aristotle's",
    "Arius",
    "Arius's",
    "Arizona",
    "Arizona's",
    "Arizonan",
    "Arizonan's",
    "Arizonans",
    "Arizonian",
    "Arizonian's",
    "Arizonians",
    "Arjuna",
    "Arjuna's",
    "Arkansan",
    "Arkansan's",
    "Arkansas",
    "Arkansas's",
    "Arkhangelsk",
    "Arkhangelsk's",
    "Arkwright",
    "Arkwright's",
    "Arlene",
    "Arlene's",
    "Arline",
    "Arline's",
    "Arlington",
    "Arlington's",
    "Armageddon",
    "Armageddon's",
    "Armageddons",
    "Armagnac",
    "Armagnac's",
    "Armand",
    "Armand's",
    "Armando",
    "Armando's",
    "Armani",
    "Armani's",
    "Armenia",
    "Armenia's",
    "Armenian",
    "Armenian's",
    "Armenians",
    "Arminius",
    "Arminius's",
    "Armonk",
    "Armonk's",
    "Armour",
    "Armour's",
    "Armstrong",
    "Armstrong's",
    "Arneb",
    "Arneb's",
    "Arnhem",
    "Arnhem's",
    "Arno",
    "Arno's",
    "Arnold",
    "Arnold's",
    "Arnulfo",
    "Arnulfo's",
    "Aron",
    "Aron's",
    "Arrhenius",
    "Arrhenius's",
    "Arron",
    "Arron's",
    "Art",
    "Art's",
    "Artaxerxes",
    "Artaxerxes's",
    "Artemis",
    "Artemis's",
    "Arthur",
    "Arthur's",
    "Arthurian",
    "Arthurian's",
    "Artie",
    "Artie's",
    "Arturo",
    "Arturo's",
    "Aruba",
    "Aruba's",
    "Aryan",
    "Aryan's",
    "Aryans",
    "As",
    "As's",
    "Asama",
    "Asama's",
    "Ascella",
    "Ascella's",
    "Asgard",
    "Asgard's",
    "Ashanti",
    "Ashanti's",
    "Ashcroft",
    "Ashcroft's",
    "Ashe",
    "Ashe's",
    "Ashikaga",
    "Ashikaga's",
    "Ashkenazim",
    "Ashkenazim's",
    "Ashkhabad",
    "Ashkhabad's",
    "Ashlee",
    "Ashlee's",
    "Ashley",
    "Ashley's",
    "Ashmolean",
    "Ashmolean's",
    "Ashurbanipal",
    "Ashurbanipal's",
    "Asia",
    "Asia's",
    "Asiago",
    "Asian",
    "Asian's",
    "Asians",
    "Asiatic",
    "Asiatic's",
    "Asiatics",
    "Asimov",
    "Asimov's",
    "Asmara",
    "Asmara's",
    "Asoka",
    "Asoka's",
    "Aspell",
    "Aspell's",
    "Aspen",
    "Aspen's",
    "Asperger",
    "Asperger's",
    "Aspidiske",
    "Aspidiske's",
    "Asquith",
    "Asquith's",
    "Assad",
    "Assad's",
    "Assam",
    "Assam's",
    "Assamese",
    "Assamese's",
    "Assisi",
    "Assisi's",
    "Assyria",
    "Assyria's",
    "Assyrian",
    "Assyrian's",
    "Assyrians",
    "Astaire",
    "Astaire's",
    "Astana",
    "Astana's",
    "Astarte",
    "Astarte's",
    "Aston",
    "Aston's",
    "Astor",
    "Astor's",
    "Astoria",
    "Astoria's",
    "Astrakhan",
    "Astrakhan's",
    "AstroTurf",
    "AstroTurf's",
    "Asturias",
    "Asturias's",
    "Asunción",
    "Asunción's",
    "Aswan",
    "Aswan's",
    "Atacama",
    "Atacama's",
    "Atahualpa",
    "Atahualpa's",
    "Atalanta",
    "Atalanta's",
    "Atari",
    "Atari's",
    "Atatürk",
    "Atatürk's",
    "Athabasca",
    "Athabasca's",
    "Athabascan",
    "Athabascan's",
    "Athena",
    "Athena's",
    "Athenian",
    "Athenian's",
    "Athenians",
    "Athens",
    "Athens's",
    "Atkins",
    "Atkins's",
    "Atkinson",
    "Atkinson's",
    "Atlanta",
    "Atlanta's",
    "Atlantes",
    "Atlantic",
    "Atlantic's",
    "Atlantis",
    "Atlantis's",
    "Atlas",
    "Atlas's",
    "Atlases",
    "Atman",
    "Atman's",
    "Atreus",
    "Atreus's",
    "Atria",
    "Atria's",
    "Atropos",
    "Atropos's",
    "Ats",
    "Attic",
    "Attic's",
    "Attica",
    "Attica's",
    "Attila",
    "Attila's",
    "Attlee",
    "Attlee's",
    "Attucks",
    "Attucks's",
    "Atwood",
    "Atwood's",
    "Au",
    "Au's",
    "Aubrey",
    "Aubrey's",
    "Auckland",
    "Auckland's",
    "Auden",
    "Auden's",
    "Audi",
    "Audi's",
    "Audion",
    "Audion's",
    "Audra",
    "Audra's",
    "Audrey",
    "Audrey's",
    "Audubon",
    "Audubon's",
    "Aug",
    "Aug's",
    "Augean",
    "Augean's",
    "Augsburg",
    "Augsburg's",
    "August",
    "August's",
    "Augusta",
    "Augusta's",
    "Augustan",
    "Augustan's",
    "Augustine",
    "Augustine's",
    "Augusts",
    "Augustus",
    "Augustus's",
    "Aurangzeb",
    "Aurangzeb's",
    "Aurelia",
    "Aurelia's",
    "Aurelio",
    "Aurelio's",
    "Aurelius",
    "Aurelius's",
    "Aureomycin",
    "Aureomycin's",
    "Auriga",
    "Auriga's",
    "Aurora",
    "Aurora's",
    "Auschwitz",
    "Auschwitz's",
    "Aussie",
    "Aussie's",
    "Aussies",
    "Austen",
    "Austen's",
    "Austerlitz",
    "Austerlitz's",
    "Austin",
    "Austin's",
    "Austins",
    "Australasia",
    "Australasia's",
    "Australia",
    "Australia's",
    "Australian",
    "Australian's",
    "Australians",
    "Australoid",
    "Australoid's",
    "Australopithecus",
    "Australopithecus's",
    "Austria",
    "Austria's",
    "Austrian",
    "Austrian's",
    "Austrians",
    "Austronesian",
    "Austronesian's",
    "Autumn",
    "Autumn's",
    "Ava",
    "Ava's",
    "Avalon",
    "Avalon's",
    "Aventine",
    "Aventine's",
    "Avernus",
    "Avernus's",
    "Averroes",
    "Averroes's",
    "Avery",
    "Avery's",
    "Avesta",
    "Avesta's",
    "Avicenna",
    "Avicenna's",
    "Avignon",
    "Avignon's",
    "Avila",
    "Avila's",
    "Avior",
    "Avior's",
    "Avis",
    "Avis's",
    "Avogadro",
    "Avogadro's",
    "Avon",
    "Avon's",
    "Axum",
    "Axum's",
    "Ayala",
    "Ayala's",
    "Ayers",
    "Ayers's",
    "Aymara",
    "Aymara's",
    "Ayrshire",
    "Ayrshire's",
    "Ayurveda",
    "Ayurveda's",
    "Ayyubid",
    "Ayyubid's",
    "Azana",
    "Azana's",
    "Azania",
    "Azania's",
    "Azazel",
    "Azazel's",
    "Azerbaijan",
    "Azerbaijan's",
    "Azerbaijani",
    "Azerbaijani's",
    "Azores",
    "Azores's",
    "Azov",
    "Azov's",
    "Aztec",
    "Aztec's",
    "Aztecan",
    "Aztecan's",
    "Aztecs",
    "Aztlan",
    "Aztlan's",
    "B",
    "B's",
    "BBB",
    "BBB's",
    "BMW",
    "BMW's",
    "BP",
    "BP's",
    "BSD",
    "BSD's",
    "Ba",
    "Ba's",
    "Baal",
    "Baal's",
    "Baath",
    "Baath's",
    "Baathist",
    "Baathist's",
    "Babar",
    "Babar's",
    "Babbage",
    "Babbage's",
    "Babbitt",
    "Babbitt's",
    "Babel",
    "Babel's",
    "Babels",
    "Babur",
    "Babur's",
    "Babylon",
    "Babylon's",
    "Babylonian",
    "Babylonian's",
    "Babylons",
    "Bacall",
    "Bacall's",
    "Bacardi",
    "Bacardi's",
    "Bacchanalia",
    "Bacchanalia's",
    "Bacchus",
    "Bacchus's",
    "Bach",
    "Bach's",
    "Backus",
    "Backus's",
    "Bacon",
    "Bacon's",
    "Bactria",
    "Bactria's",
    "Baden",
    "Baden's",
    "Badlands",
    "Badlands's",
    "Baedeker",
    "Baedeker's",
    "Baez",
    "Baez's",
    "Baffin",
    "Baffin's",
    "Baggies",
    "Baggies's",
    "Baghdad",
    "Baghdad's",
    "Baguio",
    "Baguio's",
    "Baha'i",
    "Baha'i's",
    "Baha'ullah",
    "Baha'ullah's",
    "Bahama",
    "Bahama's",
    "Bahamas",
    "Bahamas's",
    "Bahamian",
    "Bahamian's",
    "Bahamians",
    "Bahia",
    "Bahia's",
    "Bahrain",
    "Bahrain's",
    "Baikal",
    "Baikal's",
    "Bailey",
    "Bailey's",
    "Baird",
    "Baird's",
    "Bakelite",
    "Bakelite's",
    "Baker",
    "Baker's",
    "Bakersfield",
    "Bakersfield's",
    "Baku",
    "Baku's",
    "Bakunin",
    "Bakunin's",
    "Balanchine",
    "Balanchine's",
    "Balaton",
    "Balaton's",
    "Balboa",
    "Balboa's",
    "Balder",
    "Balder's",
    "Baldwin",
    "Baldwin's",
    "Balearic",
    "Balearic's",
    "Balfour",
    "Balfour's",
    "Bali",
    "Bali's",
    "Balinese",
    "Balinese's",
    "Balkan",
    "Balkan's",
    "Balkans",
    "Balkans's",
    "Balkhash",
    "Balkhash's",
    "Ball",
    "Ball's",
    "Ballard",
    "Ballard's",
    "Balthazar",
    "Balthazar's",
    "Baltic",
    "Baltic's",
    "Baltimore",
    "Baltimore's",
    "Baluchistan",
    "Baluchistan's",
    "Balzac",
    "Balzac's",
    "Bamako",
    "Bamako's",
    "Bambi",
    "Bambi's",
    "Banach",
    "Banach's",
    "Bancroft",
    "Bancroft's",
    "Bandung",
    "Bandung's",
    "Bangalore",
    "Bangalore's",
    "Bangkok",
    "Bangkok's",
    "Bangladesh",
    "Bangladesh's",
    "Bangladeshi",
    "Bangladeshi's",
    "Bangladeshis",
    "Bangor",
    "Bangor's",
    "Bangui",
    "Bangui's",
    "Banjarmasin",
    "Banjarmasin's",
    "Banjul",
    "Banjul's",
    "Banks",
    "Banks's",
    "Banneker",
    "Banneker's",
    "Bannister",
    "Bannister's",
    "Banting",
    "Banting's",
    "Bantu",
    "Bantu's",
    "Bantus",
    "Baotou",
    "Baotou's",
    "Baptist",
    "Baptist's",
    "Baptiste",
    "Baptiste's",
    "Baptists",
    "Barabbas",
    "Barabbas's",
    "Barack",
    "Barack's",
    "Barbadian",
    "Barbadian's",
    "Barbadians",
    "Barbados",
    "Barbados's",
    "Barbara",
    "Barbara's",
    "Barbarella",
    "Barbarella's",
    "Barbarossa",
    "Barbarossa's",
    "Barbary",
    "Barbary's",
    "Barber",
    "Barber's",
    "Barbie",
    "Barbie's",
    "Barbour",
    "Barbour's",
    "Barbra",
    "Barbra's",
    "Barbuda",
    "Barbuda's",
    "Barcelona",
    "Barcelona's",
    "Barclay",
    "Barclay's",
    "Bardeen",
    "Bardeen's",
    "Barents",
    "Barents's",
    "Barker",
    "Barker's",
    "Barkley",
    "Barkley's",
    "Barlow",
    "Barlow's",
    "Barnabas",
    "Barnabas's",
    "Barnaby",
    "Barnaby's",
    "Barnard",
    "Barnard's",
    "Barnaul",
    "Barnaul's",
    "Barnes",
    "Barnes's",
    "Barnett",
    "Barnett's",
    "Barney",
    "Barney's",
    "Barnum",
    "Barnum's",
    "Baroda",
    "Baroda's",
    "Barquisimeto",
    "Barquisimeto's",
    "Barr",
    "Barr's",
    "Barranquilla",
    "Barranquilla's",
    "Barrera",
    "Barrera's",
    "Barrett",
    "Barrett's",
    "Barrie",
    "Barrie's",
    "Barron",
    "Barron's",
    "Barry",
    "Barry's",
    "Barrymore",
    "Barrymore's",
    "Barth",
    "Barth's",
    "Bartholdi",
    "Bartholdi's",
    "Bartholomew",
    "Bartholomew's",
    "Bartlett",
    "Bartlett's",
    "Barton",
    "Barton's",
    "Bartók",
    "Bartók's",
    "Baruch",
    "Baruch's",
    "Baryshnikov",
    "Baryshnikov's",
    "Basel",
    "Basel's",
    "Basho",
    "Basho's",
    "Basie",
    "Basie's",
    "Basil",
    "Basil's",
    "Basque",
    "Basque's",
    "Basques",
    "Basra",
    "Basra's",
    "Bass",
    "Bass's",
    "Basseterre",
    "Basseterre's",
    "Bastille",
    "Bastille's",
    "Bataan",
    "Bataan's",
    "Bates",
    "Bates's",
    "Bathsheba",
    "Bathsheba's",
    "Batista",
    "Batista's",
    "Batman",
    "Batman's",
    "Battle",
    "Battle's",
    "Batu",
    "Batu's",
    "Baudelaire",
    "Baudelaire's",
    "Baudouin",
    "Baudouin's",
    "Bauer",
    "Bauer's",
    "Bauhaus",
    "Bauhaus's",
    "Baum",
    "Baum's",
    "Bavaria",
    "Bavaria's",
    "Bavarian",
    "Bavarian's",
    "Baxter",
    "Baxter's",
    "Bayer",
    "Bayer's",
    "Bayes",
    "Bayes's",
    "Bayesian",
    "Bayesian's",
    "Bayeux",
    "Bayeux's",
    "Baylor",
    "Baylor's",
    "Bayonne",
    "Bayonne's",
    "Bayreuth",
    "Bayreuth's",
    "Baywatch",
    "Baywatch's",
    "Beach",
    "Beach's",
    "Beadle",
    "Beadle's",
    "Bean",
    "Bean's",
    "Beard",
    "Beard's",
    "Beardmore",
    "Beardmore's",
    "Beardsley",
    "Beardsley's",
    "Bearnaise",
    "Bearnaise's",
    "Beasley",
    "Beasley's",
    "Beatlemania",
    "Beatlemania's",
    "Beatles",
    "Beatles's",
    "Beatrice",
    "Beatrice's",
    "Beatrix",
    "Beatrix's",
    "Beatriz",
    "Beatriz's",
    "Beau",
    "Beau's",
    "Beaufort",
    "Beaufort's",
    "Beaujolais",
    "Beaujolais's",
    "Beaumarchais",
    "Beaumarchais's",
    "Beaumont",
    "Beaumont's",
    "Beauregard",
    "Beauregard's",
    "Beauvoir",
    "Beauvoir's",
    "Bechtel",
    "Bechtel's",
    "Beck",
    "Beck's",
    "Becker",
    "Becker's",
    "Becket",
    "Becket's",
    "Beckett",
    "Beckett's",
    "Becky",
    "Becky's",
    "Becquerel",
    "Becquerel's",
    "Bede",
    "Bede's",
    "Bedouin",
    "Bedouin's",
    "Bedouins",
    "Beebe",
    "Beebe's",
    "Beecher",
    "Beecher's",
    "Beefaroni",
    "Beefaroni's",
    "Beelzebub",
    "Beelzebub's",
    "Beerbohm",
    "Beerbohm's",
    "Beethoven",
    "Beethoven's",
    "Beeton",
    "Beeton's",
    "Begin",
    "Begin's",
    "Behan",
    "Behan's",
    "Behring",
    "Behring's",
    "Beiderbecke",
    "Beiderbecke's",
    "Beijing",
    "Beijing's",
    "Beirut",
    "Beirut's",
    "Bekesy",
    "Bekesy's",
    "Bela",
    "Bela's",
    "Belarus",
    "Belarus's",
    "Belau",
    "Belau's",
    "Belem",
    "Belem's",
    "Belfast",
    "Belfast's",
    "Belgian",
    "Belgian's",
    "Belgians",
    "Belgium",
    "Belgium's",
    "Belgrade",
    "Belgrade's",
    "Belinda",
    "Belinda's",
    "Belize",
    "Belize's",
    "Bell",
    "Bell's",
    "Bella",
    "Bella's",
    "Bellamy",
    "Bellamy's",
    "Bellatrix",
    "Bellatrix's",
    "Belleek",
    "Belleek's",
    "Bellini",
    "Bellini's",
    "Bellow",
    "Bellow's",
    "Belmont",
    "Belmont's",
    "Belmopan",
    "Belmopan's",
    "Belshazzar",
    "Belshazzar's",
    "Beltane",
    "Beltane's",
    "Belushi",
    "Belushi's",
    "Ben",
    "Ben's",
    "Benacerraf",
    "Benacerraf's",
    "Benares",
    "Benares's",
    "Benchley",
    "Benchley's",
    "Bender",
    "Bender's",
    "Bendix",
    "Bendix's",
    "Benedict",
    "Benedict's",
    "Benedictine",
    "Benedictine's",
    "Benelux",
    "Benelux's",
    "Benet",
    "Benet's",
    "Benetton",
    "Benetton's",
    "Bengal",
    "Bengal's",
    "Bengali",
    "Bengali's",
    "Benghazi",
    "Benghazi's",
    "Benin",
    "Benin's",
    "Benita",
    "Benita's",
    "Benito",
    "Benito's",
    "Benjamin",
    "Benjamin's",
    "Bennett",
    "Bennett's",
    "Bennie",
    "Bennie's",
    "Benny",
    "Benny's",
    "Benson",
    "Benson's",
    "Bentham",
    "Bentham's",
    "Bentley",
    "Bentley's",
    "Benton",
    "Benton's",
    "Benz",
    "Benz's",
    "Benzedrine",
    "Benzedrine's",
    "Beowulf",
    "Beowulf's",
    "Berber",
    "Berber's",
    "Berbers",
    "Berenice",
    "Berenice's",
    "Beretta",
    "Beretta's",
    "Berg",
    "Berg's",
    "Bergen",
    "Bergen's",
    "Berger",
    "Berger's",
    "Bergerac",
    "Bergerac's",
    "Bergman",
    "Bergman's",
    "Bergson",
    "Bergson's",
    "Beria",
    "Beria's",
    "Bering",
    "Bering's",
    "Berkeley",
    "Berkeley's",
    "Berkshire",
    "Berkshire's",
    "Berkshires",
    "Berkshires's",
    "Berle",
    "Berle's",
    "Berlin",
    "Berlin's",
    "Berliner",
    "Berliner's",
    "Berlins",
    "Berlioz",
    "Berlioz's",
    "Berlitz",
    "Berlitz's",
    "Bermuda",
    "Bermuda's",
    "Bermudas",
    "Bern",
    "Bern's",
    "Bernadette",
    "Bernadette's",
    "Bernadine",
    "Bernadine's",
    "Bernanke",
    "Bernanke's",
    "Bernard",
    "Bernard's",
    "Bernardo",
    "Bernardo's",
    "Bernays",
    "Bernays's",
    "Bernbach",
    "Bernbach's",
    "Berne",
    "Berne's",
    "Bernhardt",
    "Bernhardt's",
    "Bernice",
    "Bernice's",
    "Bernie",
    "Bernie's",
    "Bernini",
    "Bernini's",
    "Bernoulli"
]


def create_customers(n):
    customers = []
    i = 0

    for word in common_words_dictionary:
        customers.append(
            Customer(name=word, code=str(i))
        )
        if i > n:
            break
        i = i + 1
    return Customer.objects.bulk_create(customers)


def create_default_data():
    create_customers(1000)


def create_lines(header, lines):
    tmp = []
    for i, line in enumerate(lines):
        line["line_no"] = i + 1
        line["header"] = header
        tmp.append(SaleLine(**line))
    return SaleLine.objects.bulk_create(tmp)


def create_invoices(customer, ref_prefix, n, value=100):
    date = timezone.now()
    due_date = date + timedelta(days=31)
    invoices = []
    for i in range(n):
        i = SaleHeader(
            customer=customer,
            ref=ref_prefix + str(i),
            goods=value,
            vat=0.2 * value,
            total=1.2 * value,
            paid=0,
            due=1.2 * value,
            date=date,
            due_date=due_date,
            type="si",
            period=PERIOD
        )
        invoices.append(i)
    return SaleHeader.objects.bulk_create(invoices)


def create_invoice_with_lines(header, lines):
    header = SaleHeader.objects.create(**header)
    lines = create_lines(header, lines)
    return header, lines


def create_credit_note_with_lines(header, lines):
    header["paid"] *= -1
    header["total"] *= -1
    header["due"] *= -1
    header = SaleHeader.objects.create(**header)
    # this assumes lines[n] is line[0] for all n
    lines[0]["goods"] *= -1
    lines[0]["vat"] *= -1
    lines = create_lines(header, lines)
    return header, lines


def create_receipts(customer, ref_prefix, n, value=100):
    date = timezone.now()
    due_date = date + timedelta(days=31)
    payments = []
    for i in range(n):
        p = SaleHeader(
            customer=customer,
            ref=ref_prefix + str(i),
            total=-1 * value,
            paid=0,
            due=-1 * value,
            date=date,
            type="sp",
            period=PERIOD
        )
        payments.append(p)
    return SaleHeader.objects.bulk_create(payments)


def create_invoice_with_nom_entries(header, lines, vat_nominal, control_nominal):
    header = SaleHeader.objects.create(**header)
    lines = create_lines(header, lines)
    nom_trans = []
    for line in lines:
        if line.goods:
            nom_trans.append(
                NominalTransaction(
                    module="SL",
                    header=header.pk,
                    line=line.pk,
                    nominal=line.nominal,
                    value=-1 * line.goods,
                    ref=header.ref,
                    period=header.period,
                    date=header.date,
                    field="g",
                    type=header.type
                )
            )
        if line.vat:
            nom_trans.append(
                NominalTransaction(
                    module="SL",
                    header=header.pk,
                    line=line.pk,
                    nominal=vat_nominal,
                    value=-1 * line.vat,
                    ref=header.ref,
                    period=header.period,
                    date=header.date,
                    field="v",
                    type=header.type
                )
            )
        if line.goods or line.vat:
            nom_trans.append(
                NominalTransaction(
                    module="SL",
                    header=header.pk,
                    line=line.pk,
                    nominal=control_nominal,
                    value=line.goods + line.vat,
                    ref=header.ref,
                    period=header.period,
                    date=header.date,
                    field="t",
                    type=header.type
                )
            )
    nom_trans = NominalTransaction.objects.bulk_create(nom_trans)
    nom_trans = sort_multiple(nom_trans, *[(lambda n: n.line, False)])
    goods_and_vat = nom_trans[:-1]
    for i, line in enumerate(lines):
        line.goods_nominal_transaction = nom_trans[3 * i]
        line.vat_nominal_transaction = nom_trans[(3 * i) + 1]
        line.total_nominal_transaction = nom_trans[(3 * i) + 2]
    SaleLine.objects.bulk_update(
        lines,
        ["goods_nominal_transaction", "vat_nominal_transaction",
            "total_nominal_transaction"]
    )
    return header


def create_receipt_with_nom_entries(header, control_nominal, bank_nominal):
    header["total"] *= -1
    header["due"] *= -1
    header["paid"] *= -1
    header["goods"] = 0
    header["vat"] = 0
    header = SaleHeader.objects.create(**header)
    if header.total != 0:
        nom_trans = []
        nom_trans.append(
            NominalTransaction(
                module="SL",
                header=header.pk,
                line=1,
                nominal=bank_nominal,
                value=-1 * header.total,
                ref=header.ref,
                period=header.period,
                date=header.date,
                field="t",
                type=header.type
            )
        )
        nom_trans.append(
            NominalTransaction(
                module="SL",
                header=header.pk,
                line=2,
                nominal=control_nominal,
                value=header.total,
                ref=header.ref,
                period=header.period,
                date=header.date,
                field="t",
                type=header.type
            )
        )
        nom_trans = NominalTransaction.objects.bulk_create(nom_trans)
        CashBookTransaction.objects.create(
            module="SL",
            header=header.pk,
            line=1,
            cash_book=header.cash_book,
            value=-1 * header.total,
            ref=header.ref,
            period=header.period,
            date=header.date,
            field="t",
            type=header.type
        )
        return header


def create_refund_with_nom_entries(header, control_nominal, bank_nominal):
    # positive inputted, turn negative, then turned positive again in create_payment_with_nom
    header["total"] *= -1
    header["due"] *= -1
    header["paid"] *= -1
    # done this way because i created other function first
    return create_receipt_with_nom_entries(header, control_nominal, bank_nominal)


def create_credit_note_with_nom_entries(header, lines, vat_nominal, control_nominal):
    header["total"] = -1 * header["total"]
    header["due"] = -1 * header["due"]
    header["paid"] = -1 * header["paid"]
    header["goods"] = -1 * header["goods"]
    header["vat"] = -1 * header["vat"]
    # lines is assumed to be of form [ {} ] * N
    # thus each object is in fact the same object in memory
    lines[0]["goods"] = -1 * lines[0]["goods"]
    lines[0]["vat"] = -1 * lines[0]["vat"]
    return create_invoice_with_nom_entries(header, lines, vat_nominal, control_nominal)


def create_vat_transactions(header, lines):
    vat_trans = []
    for line in lines:
        vat_trans.append(
            VatTransaction(
                header=header.pk,
                line=line.pk,
                module="SL",
                ref=header.ref,
                period=header.period,
                date=header.date,
                field="v",
                tran_type=header.type,
                vat_type="o",
                vat_code=line.vat_code,
                vat_rate=line.vat_code.rate,
                goods=line.goods,
                vat=line.vat
            )
        )
    vat_trans = VatTransaction.objects.bulk_create(vat_trans)
    vat_trans = sort_multiple(vat_trans, *[ (lambda v : v.line, False) ])
    lines = sort_multiple(lines, *[ (lambda l : l.pk, False) ])
    for i, line in enumerate(lines):
        line.vat_transaction = vat_trans[i]
    SaleLine.objects.bulk_update(lines, ["vat_transaction"])
