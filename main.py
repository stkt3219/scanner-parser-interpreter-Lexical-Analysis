import interpreterLexicalAnalysis
import parserLexicalAnalysis
import scannerLexicalAnalysis

while True:
    userinput = input('compute > ')
    result, error = interpreterLexicalAnalysis.run(userinput)  # pass in filename with file input
    if error:
        print(error.string())
    else:
        print(result)
