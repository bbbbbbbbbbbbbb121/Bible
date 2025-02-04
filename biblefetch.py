# Creates files as:
# Bible/NT/(1) Matthew.md
# Bible/OT/(1) Genesis.md

DEFAULT_SPECIAL = {
    "Lord": "Lᴏʀᴅ"
}

import requests, json, os, re

js = json.loads(requests.get("https://raw.githubusercontent.com/bbbbbbbbbbbbbb121/Bible/refs/heads/main/temp.json").text)

for a in js:
    url = f"https://raw.githubusercontent.com/TehShrike/world-english-bible/refs/heads/master/json/{a}"
    path = f"Bible/Books/{a}"
    
    if not os.path.exists(path):
        print(f"Downloading book {a}..")
        open(path, "w").write(requests.get(url).text)

def bookToPath(Book: str):
    Book = Book.lower()
    Book = Book.replace(" ", "")
    
    return "Bible/Books/" + Book + ".json"

def pathToBook(Book: str):
    def Format(Match):
        BookName = Match.group(2).capitalize()
        if len(Match.group(1)) == 0:
            return BookName
        else:
            return f"{Match.group(1)} {BookName}"
    Path = re.sub(string=Book, pattern="(\d*)(\w+).json", repl=Format).split("/")
    
    return Path[len(Path) - 1]

def formatText(Data, exportType, exportSettings):
    type = Data["type"]
    if exportType == "md":
        text = ""
        numbers = {
            "0": "⁰",
            "1": "¹",
            "2": "²",
            "3": "³",
            "4": "⁴",
            "5": "⁵",
            "6": "⁶",
            "7": "⁷",
            "8": "⁸",
            "9": "⁹"
        }
        
        versesInlined = exportSettings["versesInlined"]
        verse = exportSettings["versesNumbered"] and str(Data.get("verseNumber", "")) or ""
        verseText = Data.get("value", "").strip()
        
        if versesInlined:
            if type == "paragraph start" or verse == "1":
                text += f"\n#### "
            elif type == "paragraph end":
                text += "\n\n"
                
            if type == "paragraph text" or verseText != "":
                for n in numbers:
                    verse = verse.replace(n, numbers[n])
            
                text += f"{verse} {verseText} "
        else:
            if type == "paragraph text":
                for n in numbers:
                    verse = verse.replace(n, numbers[n])
            
                text += f"## {verse} {verseText}\n"
        
        return text
    else:
        return "Unsupported export type."
    
def validate(a, b):
    c = {}
    
    for key in b:
        c[key] = a.get(key, b[key])
        
    return c

def parseBook(book, exportType="md", exportSettings={}, special=DEFAULT_SPECIAL):
    path = bookToPath(book)
    name = pathToBook(path)
    content = json.loads(open(path, "r").read())
    
    exportSettings = validate(exportSettings, {"versesInlined": True, "versesNumbered": True})
    
    text = ""
    lastChapter = 0
    
    for Data in content:
        currentChapter = Data.get("chapterNumber", lastChapter)
        newChapter = lastChapter != currentChapter
        
        if newChapter:
            text += f"# {name} {currentChapter}\n"
            lastChapter = currentChapter
            
        text += formatText(Data, exportType, exportSettings)
    
    text = text.replace("\n#### #", "#")
    for word in special:
        text = re.sub(pattern=word, repl=special[word], string=text, flags=re.IGNORECASE)
    
    return text

def getAvailableBooks():
    return {
        "OT": [
            "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
            "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings",
            "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah",
            "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Songofsolomon",
            "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea",
            "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
            "Zephaniah", "Haggai", "Zechariah", "Malachi"
        ],
        "NT": [
            "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
            "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
            "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus",
            "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John",
            "3 John", "Jude", "Revelation"
        ]
    }

        
for Testament in getAvailableBooks():
    TestamentPath = f"Bible/BooksMD/{Testament}"
    for Index, Book in enumerate(getAvailableBooks()[Testament]):
        if not os.path.isdir(TestamentPath):
            os.mkdir(TestamentPath)
            
        Path = f"{TestamentPath}/({Index + 1}) {Book}.md"
    
        open(Path, "w").write(parseBook(Book))
