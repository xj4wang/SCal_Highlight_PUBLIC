import string

def writeHTML():
    
    letters = list(string.ascii_lowercase)
    
    h = ["Anthropology", "Archaeology, History", "Linguistics and languages", "Philosophy", "Religion", "Culinary arts", "Literature", "Performing arts", "Visual arts", "Other (please specify)"]
    
    ss = ["Economics", "Geography", "Interdisciplinary studies", "Area studies", "Ethic and cultural studies", "Gender and sexuality studies", "Organizational studies", "Political science", "Psychology", " Sociology", "Other (please specify)"]
    
    ns = ["Biology", "Chemistry", "Earth sciences", "Physics", "Space sciences", "Other (please specify)"]
    
    fs = ["Computer sciences", "Logic", "Mathematics", "Pure mathematics", "Applied mathematics", " Statistics", "System science", "Other (please specify)"]
    
    n = "4"
    for i in range(len(fs)):
        print("<li>")
        print("<input type=\"checkbox\" id=\"education" + n + letters[i] + "\" name=\"education\" value=\"education" + n + letters[i] + "\">")
        print("<label for=\"education" + n + letters[i] + "\">" + fs[i] + "</label>")
        print("</li>")


writeHTML()