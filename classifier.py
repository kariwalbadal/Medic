def classifier(diseases, symptoms):

    if len(symptoms) == 0:
        print("Empty symptoms list. Try again.")
        return []

    if(len(diseases) == 0):
        print("No matching disease found")
        return []

    max_match_count = 0
    min_match_count = 500
    for disease in diseases:
        symp = disease.get_symp()
        match_count = 0
        unmatch_count = 0
        for item in symp:
            for symptom in symptoms:
                if symptom==item :
                    match_count = match_count+1
                else:
                    unmatch_count = unmatch_count+1
        if match_count > max_match_count:
            max_match_count = match_count
        if match_count < min_match_count:
            min_match_count = match_count
    disease_match_bucket = [[]]
    #print("max match"+str(max_match_count))
    #print("Min match"+str(min_match_count))
    for x in range(max_match_count-min_match_count+1):
        disease_match_bucket.append([])
    #print((disease_match_bucket))
    disease_match_bucket.remove([])
    for disease in diseases:
        symp = disease.get_symp()
        match_count = 0
        unmatch_count = 0
        for item in symp:
            for symptom in symptoms:
                if symptom==item:
                    match_count = match_count+1
                else:
                    unmatch_count = unmatch_count+1

        disease_match_bucket[max_match_count-match_count].append(disease)
        #print(len(disease_match_bucket))



    most_pot_diseases  = disease_match_bucket[0]
    maybe_pot_diseases = []
    if(len(disease_match_bucket) > 1):
        maybe_pot_diseases = disease_match_bucket[1]
    #print(disease_match_bucket)
    #print(len(disease_match_bucket))
    score = []
    i = 0
    #print(most_pot_diseases)
    #print(maybe_pot_diseases)
    for most_pot_disease in most_pot_diseases:
        pd = most_pot_disease.get_pd()
        loc = most_pot_disease.get_loc()
        cli = most_pot_disease.get_cli()
        score.append(max_match_count*1200 + pd * 0.3 + loc * 0.35 + cli * 0.35)
        print("score " + str(max_match_count*1200 + pd * 0.3 + loc * 0.35 + cli * 0.35) + " for " + most_pot_disease.get_name())
        i = i+1

    for maybe_pot_disease in maybe_pot_diseases:
        pd = maybe_pot_disease.get_pd()
        loc = maybe_pot_disease.get_loc()
        cli = maybe_pot_disease.get_cli()
        score.append((max_match_count - 1) * 1000 + pd * 0.3 + loc * 0.35 + cli * 0.35)
        print("score " + str(
            (max_match_count - 1) * 1000 + pd * 0.3 + loc * 0.35 + cli * 0.35) + " for " + maybe_pot_disease.get_name())
        i = i + 1

    max_score = 0
    max_score_i = 0
    #print(i)
    #print(len(score))
    i=0
    for x in score:
        if(x > max_score):
            max_score = score[i]
            max_score_i = i
#        print(pot_diseases[i].get_name()+" score "+str(x))
        i = i+1
    if(max_score_i < len(most_pot_diseases)):
        #print("The most likely disease is " + most_pot_diseases[max_score_i].get_name())
        return most_pot_diseases[max_score_i].get_name()
    else:
        #print("The most likely disease is " + maybe_pot_diseases[max_score_i-len(most_pot_diseases)].get_name())
        return maybe_pot_diseases[max_score_i-len(most_pot_diseases)].get_name()