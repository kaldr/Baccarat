from colorama import Fore, Back, Style, init
import bson
import json
from bson.json_util import loads, RELAXED_JSON_OPTIONS, default
import re
import moment
init(autoreset=True)
import collections
from bson.codec_options import CodecOptions
options = CodecOptions(document_class=collections.OrderedDict)


class console:
    printFunc = print
    line = 0

    @classmethod
    def lineColor(self):
        if self.line % 2 == 0:
            return Back.GREEN
        else:
            return Back.CYAN

    @classmethod
    def singleLog(self, text, end=False):
        if end:
            color = Back.MAGENTA
            tcolor = Fore.MAGENTA
        else:
            color = self.lineColor()
            tcolor = ""
        self.line += 1
        self.printFunc(color + Fore.WHITE + "  " +
                       moment.now().timezone("PRC").format("HH:mm:ss") + "  " + Style.RESET_ALL + "  " + tcolor + text + Style.RESET_ALL)

    @classmethod
    def printNormalText(self, t):
        try:
            s = t.replace("'", '"').replace("False", 'false').replace("True", 'true').replace("None", "''")
            s = re.sub(r'ObjectId\("([^\)]+)"\)', '\'ObjectId(\\1)\'', s)
            s = re.sub(r'<attribute\s"([^"]+)"\sof\s"([^"]+)"\sobjects>', '<attribute \\1 of \\2 objects>', s)
            s = re.sub(r'(<[^>]+>)', '\'\\1\'', s)
            s = re.sub(r'datetime\.datetime\(([^\)]+)\)', '\'Date(\\1)\'', s).replace("'", '"')
            a = json.loads(s)
            if isinstance(a, dict):
                # print("in dict")
                d = "\n" + json.dumps(a, ensure_ascii=False, sort_keys=False,  indent=4)
            elif isinstance(a, list):
                if [x for x in a if isinstance(x, dict) or isinstance(x, list)]:
                    d = "\n" + json.dumps(a, ensure_ascii=False, sort_keys=False, indent=4)
                else:
                    d = str(a)
            else:
                d = json.dumps(a, ensure_ascii=False, sort_keys=False, indent=4)
            return d
        except Exception as e:
            return t

    @classmethod
    def parseText(self, text):
        if isinstance(text, str):
            if not text:
                text = "无结果"
                return "  " + text
            else:
                texts = text.split('\n')
                if len(texts) > 1:
                    for t in texts:
                        if not t == texts[-1]:
                            r = self.printNormalText(t)
                            self.singleLog(r)
                        else:
                            self.singleLog("[ 运行完成 ]", True)
                    return None
                else:
                    # print("In this")
                    d = self.printNormalText(text.replace("\n", ""))
                    return "  " + d

        elif isinstance(text, list):
            return "[ " + ', '.join(str(i) for i in text) + " ]"
        elif isinstance(text, dict):
            return "\n" + Style.RESET_ALL + "\n" + bson.dumps(text, ensure_ascii=False, indent=4)

    @classmethod
    def success(self, text):
        parsedText = self.parseText(text)
        if parsedText:
            self.printFunc("")
            self.printFunc(Back.MAGENTA + Fore.WHITE + "  " + moment.now().timezone("PRC").format(
                "HH:mm:ss") + "  " + Style.RESET_ALL + Fore.MAGENTA + parsedText + "  ")

    @classmethod
    def error(self, text):
        parsedText = self.parseText(text)
        if parsedText:
            self.printFunc(Back.RED + Fore.WHITE + "  " + moment.now().timezone("PRC").format(
                "HH:mm:ss") + "  " + Style.RESET_ALL + Fore.RED + parsedText + "  ")

    @classmethod
    def warn(self, text):
        parsedText = self.parseText(text)
        if parsedText:
            self.printFunc(Back.YELLOW + Fore.WHITE + "  " + moment.now().timezone("PRC").format(
                "HH:mm:ss") + "  " + Style.RESET_ALL + Fore.YELLOW + parsedText + "  ")

    @classmethod
    def start(self, text):
        parsedText = self.parseText(text)
        if parsedText:
            self.printFunc("")
            self.printFunc(Back.GREEN + Fore.WHITE + "  " + moment.now().timezone("PRC").format(
                "HH:mm:ss") + "  " + Style.RESET_ALL + Fore.GREEN + parsedText + "  ")

    @classmethod
    def end(self, text):
        parsedText = self.parseText(text)
        if parsedText:
            self.printFunc(Back.BLUE + Fore.WHITE + "  " + moment.now().timezone("PRC").format(
                "HH:mm:ss") + "  " + Style.RESET_ALL + Fore.BLUE + parsedText + "  ")

    @classmethod
    def log(self, text):
        parsedText = self.parseText(text)
        self.line += 1
        if parsedText:
            self.printFunc(self.lineColor() + Fore.WHITE + "  " +
                           moment.now().timezone("PRC").format("HH:mm:ss") + "  " + Style.RESET_ALL + parsedText + Style.RESET_ALL)
