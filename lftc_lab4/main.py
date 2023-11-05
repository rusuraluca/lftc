from analyzer import LexicalAnalyzer

scan = LexicalAnalyzer('p1.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('p2.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('p3.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('perr.txt', 'token.in')
scan.scan_file()

scan = LexicalAnalyzer('p4.txt', 'token.in')
scan.scan_file()
