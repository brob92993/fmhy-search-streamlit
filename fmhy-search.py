## Streamlit code
import streamlit as st

st.set_page_config(
    page_title="FMHY Search",
    page_icon="https://i.imgur.com/s9abZgP.png",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/Rust1667/fmhy-search-streamlit',
        'Report a bug': "https://github.com/Rust1667/fmhy-search-streamlit/issues",
        'About': "https://github.com/Rust1667/fmhy-search-streamlit"
    }
)


st.title("Search FMHY")

with st.sidebar:
    st.image("https://i.imgur.com/s9abZgP.png", width=100)
    st.text("Search Engine for r/FREEMEDIAHECKYEAH")
    st.markdown("Links:")
    st.markdown("* Wiki: [Reddit](https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/index/), [pages.dev](https://fmhy.pages.dev/), [Raw](https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page)")
    st.markdown("* [Github Repo (web-app)](https://github.com/Rust1667/fmhy-search-streamlit)")
    st.markdown("* [Github Repo (script)](https://github.com/Rust1667/a-FMHY-search-engine)")
    st.markdown("* [Other Search Tools for FMHY](https://www.reddit.com/r/FREEMEDIAHECKYEAH/comments/105xraz/howto_search_fmhy/)")

queryInputFromBox = st.text_input(label=" ", value="", help="Search for links in the Wiki.")


##Config
coloring = False
#coloring = st.checkbox('Coloring', help="Many links won't work when this is active.")

printRawMarkdown = False
#printRawMarkdown = st.checkbox('Raw')

failedSearchInfoMsg = "For specific media or software, try a [CSE](https://fmhy.pages.dev/toolsguide/#search-tools) / Live Sports [here](https://fmhy.pages.dev/videopiracyguide/#live-tv--sports) / Ask in [Discord](https://discord.gg/5W9QJKuPkD) or [Divolt](https://fmhy.divolt.xyz/)"

import requests

#----------------Alt Indexing------------
doAltIndexing = True #st.checkbox('Alt indexing', help="Includes the parent wiki page at the beginning of each result.")

def addPretext(lines, icon, baseURL, subURL):
    modified_lines = []
    currMdSubheading = ""
    currSubCat = ""
    currSubSubCat = ""

    for line in lines:
        if line.startswith("#"): #Title Lines
            if not subURL=="storage":
                if line.startswith("# ►"):
                    currMdSubheading = "#" + line.replace("# ►", "").strip().replace(" / ", "--").replace(" ", "-").lower()
                    currSubCat = "/ " + line.replace("# ►", "").strip() + " "
                    currSubSubCat = ""
                elif line.startswith("## ▷"):
                    if not subURL=="non-english": #Because non-eng section has multiple subsubcats with same names
                        currMdSubheading = "#" + line.replace("## ▷", "").strip().replace(" / ", "--").replace(" ", "-").lower()
                    currSubSubCat = "/ " + line.replace("## ▷", "").strip() + " "
            elif subURL=="storage":
                if line.startswith("## "):
                    currMdSubheading = "#" + line.replace("## ", "").strip().replace(" / ", "--").replace(" ", "-").lower()
                    currSubCat = "/ " + line.replace("## ", "").strip() + " "
                    currSubSubCat = ""
                elif line.startswith("### "):
                    currMdSubheading = "#" + line.replace("### ", "").strip().replace(" / ", "--").replace(" ", "-").lower()
                    currSubSubCat = "/ " + line.replace("### ", "").strip() + " "

            # Remove links from subcategory titles (because the screw the format)
            if 'http' in currSubCat: currSubCat = ''
            if 'http' in currSubSubCat: currSubSubCat = ''

        elif any(char.isalpha() for char in line): #If line has content
            preText = f"[{icon}{currSubCat}{currSubSubCat}]({baseURL}{subURL}{currMdSubheading}) ► "
            if line.startswith("* "): line = line[2:]
            modified_lines.append(preText + line)

    return modified_lines

def dlWikiChunk(fileName, icon, redditSubURL):
    pagesDevSiteSubURL = fileName.replace(".md", "").lower()
    subURL = pagesDevSiteSubURL

    #download the chunk
    print("Downloading " + fileName + "...")
    lines = requests.get("https://raw.githubusercontent.com/nbats/FMHYedit/main/" + fileName).text.split('\n')
    print("Downloaded")

    #add a pretext
    redditBaseURL = "https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/"
    pagesDevSiteBaseURL = "https://fmhy.pages.dev/"
    baseURL = pagesDevSiteBaseURL
    lines = addPretext(lines, icon, baseURL, subURL)

    return lines

def cleanLineForSearchMatchChecks(line):
    return line.replace('https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/', '/').replace('https://fmhy.pages.dev/', '/')

@st.cache_resource(ttl=43200)
def alternativeWikiIndexing():
    wikiChunks = [
        dlWikiChunk("VideoPiracyGuide.md", "📺", "video"),
        dlWikiChunk("AI.md", "🤖", "ai"),
        dlWikiChunk("Android-iOSGuide.md", "📱", "android"),
        dlWikiChunk("AudioPiracyGuide.md", "🎵", "audio"),
        dlWikiChunk("DownloadPiracyGuide.md", "💾", "download"),
        dlWikiChunk("EDUPiracyGuide.md", "🧠", "edu"),
        dlWikiChunk("GamingPiracyGuide.md", "🎮", "games"),
        dlWikiChunk("AdblockVPNGuide.md", "📛", "adblock-vpn-privacy"),
        dlWikiChunk("TOOLSGuide.md", "🔧", "tools-misc"),
        dlWikiChunk("MISCGuide.md", "📂", "misc"),
        dlWikiChunk("ReadingPiracyGuide.md", "📗", "reading"),
        dlWikiChunk("TorrentPiracyGuide.md", "🌀", "torrent"),
        dlWikiChunk("img-tools.md", "📷", "img-tools"),
        dlWikiChunk("LinuxGuide.md", "🐧🍏", "linux"),
        dlWikiChunk("DEVTools.md", "🖥️", "dev-tools"),
        dlWikiChunk("Non-English.md", "🌏", "non-eng"),
        dlWikiChunk("STORAGE.md", "🗄️", "storage"),
        dlWikiChunk("NSFWPiracy.md", "🌶", "https://saidit.net/s/freemediafuckyeah/wiki/index")
    ]
    return [item for sublist in wikiChunks for item in sublist]
#--------------------------------

@st.cache_resource(ttl=43200)
def standardWikiIndexing():
    try:
        #First, try to get it from Github
        response1 = requests.get("https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page")
        data = response1.text
    except:
        #If that fails, get it from the local backup
        with open('single-page', 'r') as f:
            data = f.read()
    lines = data.split('\n')
    return lines


def getAllLines():
    if doAltIndexing:
        try:
            lines = alternativeWikiIndexing()
        except:
            lines = standardWikiIndexing()
    else:
        lines = standardWikiIndexing()
    return lines

def removeEmptyStringsFromList(stringList):
    return [string for string in stringList if string != '']

def checkMultiWordQueryContainedExactlyInLine(line, searchQuery):
    if len(searchQuery.split(' ')) <= 1:
        return False
    return (searchQuery.lower() in line.lower())

def moveExactMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for i in range(len(myList)):
        if checkMultiWordQueryContainedExactlyInLine(myList[i], searchQuery):
            bumped.append(myList[i])
        else:
            notBumped.append(myList[i])
    return (bumped + notBumped)

def checkList1isInList2(list1, list2):
    for element in list1:
        if element not in list2:
            return False
    return True

def checkWordForWordMatch(line, searchQuery):
    lineWords = removeEmptyStringsFromList( line.lower().replace('[', ' ').replace(']', ' ').split(' ') )
    lineWords = [element.strip() for element in lineWords] #doesnt work on streamlit without this line even though it works locally
    searchQueryWords = removeEmptyStringsFromList( searchQuery.lower().split(' ') )
    return checkList1isInList2(searchQueryWords, lineWords)

def moveBetterMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for element in myList:
        if checkWordForWordMatch(element, searchQuery):
            bumped.append(element)
        else:
            notBumped.append(element)
    return (bumped + notBumped)

def getOnlyFullWordMatches(myList, searchQuery):
    bumped = []
    for element in myList:
        if checkWordForWordMatch(element, searchQuery):
            bumped.append(element)
    return bumped

def getLinesThatContainAllWords(lineList, searchQuery):
    words = removeEmptyStringsFromList( searchQuery.lower().split(' ') )
    bumped = []
    for line in lineList:
        if doAltIndexing:
            lineModdedForChecking = cleanLineForSearchMatchChecks(line).lower()
        else:
            lineModdedForChecking = line.lower()
        for word in words:
            if word not in lineModdedForChecking:
                break
        else:
            bumped.append(line)
    return bumped

def filterLines(lineList, searchQuery):
    if len(searchQuery)<=2 or (searchQuery==searchQuery.upper() and len(searchQuery)<=5):
        return getOnlyFullWordMatches(lineList, searchQuery)
    else:
        return getLinesThatContainAllWords(lineList, searchQuery)

def filterOutTitleLines(lineList):
    filteredList = []
    sectionTitleList = []
    for line in lineList:
        if line[0] != "#":
            filteredList.append(line)
        else:
            sectionTitleList.append(line)
    return [filteredList, sectionTitleList]



def doASearch(searchInput):
    searchInput = searchInput.strip()

    #make sure the input is right before continuing
    if searchInput=="":
        st.warning("The search query is empty.", icon="⚠️")
        return
    #if len(searchInput)<2 and not searchInput=="⭐":
    #    st.warning("The search query is too short.", icon="⚠️")
    #    return

    #main results
    myLineList = lineList
    linesFoundPrev = filterLines(myLineList, searchInput)

    #show only full word matches if there are too many results
    if len(linesFoundPrev) > 300:
        toomanywarningmsg = "Too many results (" + str(len(linesFoundPrev)) + "). " + "Showing only full-word matches."
        st.text(toomanywarningmsg)
        linesFoundPrev = getOnlyFullWordMatches(linesFoundPrev, searchInput)

    #rank results
    #linesFoundPrev = moveExactMatchesToFront(linesFoundPrev, searchInput)
    linesFoundPrev = moveBetterMatchesToFront(linesFoundPrev, searchInput)

    #extract titles lines
    linesFoundAll = filterOutTitleLines(linesFoundPrev)
    linesFound = linesFoundAll[0]
    sectionTitleList = linesFoundAll[1]

    #make sure results are not too many before continuing
    if len(linesFound) > 700 and not searchInput=="⭐":
        toomanywarningmsg = "Too many results (" + str(len(linesFound)) + ")."
        st.warning(toomanywarningmsg, icon="⚠️")

        #Print the section titles
        if len(sectionTitleList)>0:
            st.markdown(" ")
            st.markdown("There are these section titles in the Wiki: ")
            sectionTitleListToPrint = "\n\n".join(sectionTitleList)
            st.code(sectionTitleListToPrint, language="markdown")
            #st.markdown(" ")
            st.markdown("Find them by doing <Ctrl+F> in the [Raw markdown](https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page).")

        return

    myFilterWords = searchInput.lower().split(' ')

    #create string of text to print
    textToPrint = "\n\n".join(linesFound)

    #print search results count
    if len(linesFound)>0:
        st.text(str(len(linesFound)) + " search results for " + searchInput + ":\n")
    else:
        st.markdown("No results found for " + searchInput + "!")
        st.info(failedSearchInfoMsg, icon="ℹ️")

    # print search results
    if not printRawMarkdown:
        st.markdown(textToPrint)
    else:
        st.code(textToPrint, language="markdown")

    #title section results
    if len(sectionTitleList)>0:
        st.markdown(" ")
        st.markdown("Also there are these section titles in the Wiki: ")
        sectionTitleListToPrint = "\n\n".join(sectionTitleList)
        st.code(sectionTitleListToPrint, language="markdown")
        #st.markdown(" ")
        st.markdown("Find them by doing <Ctrl+F> in the [Raw markdown](https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page).")

    #Some results but maybe not enough
    if len(linesFound)>0 and len(linesFound)<=10:
        with st.expander("Not what you were looking for?"):
            st.info(failedSearchInfoMsg, icon="ℹ️")


## Execute at start of script
lineList = getAllLines()


## Streamlit code
def put_query_in_URL(queryInput):
    queryStringInURL = queryInput.strip()
    if not queryStringInURL=="":
        st.experimental_set_query_params(
            q=queryStringInURL
        )
    else:
        st.experimental_set_query_params()

def search_from_URL_query():
    queryParameters = st.experimental_get_query_params()
    if "q" in queryParameters:
        queryWords = queryParameters['q']
        queryInput = " ".join(queryWords)
        doASearch(queryInput)

if st.button("Search"):
    queryInput = queryInputFromBox
    doASearch(queryInput)
    put_query_in_URL(queryInput)
else:
    search_from_URL_query()
