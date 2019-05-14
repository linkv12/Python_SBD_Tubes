def cleanString(string) :
    while (string[-1] == ' ' or string[-1] == '#' or string[-1] == ')' or string[-1] == ";") :
        if string[-1] == ' ' :
            string = removeLastSpace(string)
        elif string[-1] == '#' :
            string = removeLastHashTag(string)
        elif string[-1] == ')' or string[-1] == ';' :
            string = string[:-1]

    while (string[0] == ' ' or string[0] == '(') :
        if (string[0] == ' ') :
            string = removeFirstSpace(string)
        elif (string[0] == '(') :
            string = string[1:]


    return string

def removeLastHashTag (string) :
    if string[-1] == '#' :
        return string[:-1]
    else :
        return string

def removeLastSpace (string) :
    if string[-1] == ' ' :
        return string[:-1]
    else :
        return string

def removeFirstSpace (string) :
    if string[0] == ' ' :
        return string[1:]
    else :
        return string
