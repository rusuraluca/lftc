from analyzer import LexicalAnalyzer

scan = LexicalAnalyzer('p1.rg.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('p2.rg.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('p3.rg.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('perr.rg.txt', 'token.in')
scan.scan_file()