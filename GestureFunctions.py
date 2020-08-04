#FUNCTIONS FOR GESTURE CONTROL GLOVE

# These next two functions check for the correlation between two different lists of lists
def offset_and_normalize(inp):
    mean_input = sum(inp) / len(inp)
    remove_offset = [x-mean_input for x in inp]
    norm_factor = (sum([x*x for x in remove_offset]))**0.5
    return [x/norm_factor for x in remove_offset]

def correlation(x,y):
    norm_x = offset_and_normalize(x)
    norm_y = offset_and_normalize(y)
    sum_of_products = sum([x*y for (x,y) in zip(norm_x,norm_y)])
    return sum_of_products

# since the parameters of the above two functions are just for lists of numbers,
# the function below modifies it so that it can take lists of lists of numbers
def corrForListsOfLists(firstInp, secondInp):
    maxIndex = len(firstInp)-1
    index = 0
    addedCorr = 0
    while index <= maxIndex:
        singleCorr = correlation(firstInp[index], secondInp[index])
        addedCorr += singleCorr
        index += 1
    avgCorrOfMasterList = addedCorr / len(firstInp)
    return avgCorrOfMasterList