import header
#handling everything related to turning genes into decisions


#will contain a generic FFNN that can be populated with weights and size
#specified.  Maybe an RNN too (depends on final Implementation)
#also will have generic self attention


def feedForward(x, w1, w2, w3, b1, b2, b3):
    #each w dimensionality is (inputs, neurons)
    #hardcoding at 2 hidden layers - shouldnt (hopefully) need more

    #x needs to be vertical matrix of same width as w1
    if np.shape(x)[1] != np.shape(w1)[0]:
        raise Exception("Invalid dimensions: (x, w1)")

    #b needs to be vertical, same as amount of neurons
    if np.shape(b1)[1] != np.shape(w1)[1]:
        raise Exception("Invalid dimensions: (x, w1)")

    #first layer pre activation
    a1 = np.dot(w1, x) + b1

    #first layer activation
    h1 = sig(a1)

    #pattern repeats for subsequent layers
    if np.shape(h1)[1] != np.shape(w2)[0]:
        raise Exception("Invalid dimensions: (x, w1)")

    #b2 needs to be vertical, same as amount of neurons as w2
    if np.shape(b2)[1] != np.shape(w2)[1]:
        raise Exception("Invalid dimensions: (x, w1)")

    a2 = np.dot(w2, h1) + b2

    h2 = sig(a2)

    #h2 needs to be vertical, same height as w2 is wide
    if np.shape(h2)[1] != np.shape(w3)[0]:
        raise Exception("Invalid dimensions: (x, w1)")


    if np.shape(b3)[1] != np.shape(w3)[1]:
        raise Exception("Invalid dimensions: (x, w1)")

    a3 = np.dot(w3, h2) + b3

    out = sig(a3)

    return out

def selfAttention(x, wQ, wK, wV):
    #will allow for inputs to be mixed to varying degrees
    #simulating decison making influenced by other factors
    #analgous example: in the sentence 'The moose is in it's den'
    #to know what it refers to you have to take the other words into account
    #much more than the word 'it'

    #x is vertical vector, height needs to match width of each w(same width)
    if np.shape(x)[1] != np.shape(wQ)[0]:
        raise Exception("Invalid dimensions: (x, wQ)")

    if np.shape(x)[1] != np.shape(wK)[0]:
        raise Exception("Invalid dimensions: (x, wK)")

    if np.shape(x)[1] != np.shape(wV)[0]:
        raise Exception("Invalid dimensions: (x, wV)")


    queries = np.dot(x, wQ)
    keys = np.dot(x, wK)
    values = np.dot(x, wV)

    scores = np.multipy(queries, keys)

    #dividing score by sqrt of key vector size
    #default for stabilizing gradients
    stabilize = scores/math.sqrt(np.shape(keys)[1])





#using sigmoid instead of softmax because softmax fits things better
#when there is only one right answer, this will be more fuzzy
def sig(x):
    #sigmoid activation function
    return 1/(1 + np.exp(-x))
