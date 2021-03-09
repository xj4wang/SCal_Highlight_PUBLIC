import string

def writeQuestions():
    file = open('questions.txt', 'r')
    mc = ['a', 'b', 'c', 'd', 'e']
        
    for i in range(1, 20+1): # for each of the 20 topics
        topic = file.readline().rstrip()
        file.readline()        
        
        for j in range(1, 3+1): # for each of the 3 mc questions per topic
            question = file.readline().rstrip()
            print("var q" + str(j) + " = Object.create(question);")
            print("q" + str(j) + ".q = '" + question + "';")
            
            for letter in mc: # for each of the 5 mc answers per each question
                answer = file.readline()  .rstrip()              
                print("q" + str(j) + "." + letter + " = '" + answer + "';")
            
            print("")
            file.readline()
            
        print("var qs = Object.create(question_set);")
        print("qs.t = '" + topic + "';")
        print("qs.q1 = q1;")
        print("qs.q2 = q2;")
        print("qs.q3 = q3;")
        print("list_of_questions.push(qs);")
        print("")
        print("")
        
        file.readline()
        file.readline()

    file.close()
    
writeQuestions()