from header import *
#handling everything related to turning genes into decisions


#will contain a generic FFNN that can be populated with weights and size
#specified.  Maybe an RNN too (depends on final Implementation)
#also will have generic self attention


def feedForward(x, w1, w2, w3, b1, b2, b3):
    #each w dimensionality is (neurons, inputs)
    #neurons for last w is inputs for next
    #hardcoding at 2 hidden layers - shouldnt (hopefully) need more

    #x needs to be vertical matrix of same height as w1 is wide
    if np.shape(x)[0] != np.shape(w1)[1]:
        raise Exception("Invalid dimensions: (x, w1)", np.shape(x), np.shape(w1))

    #b needs to be vertical, same as amount of neurons
    if np.shape(b1)[0] != np.shape(w1)[0]:
        raise Exception("Invalid dimensions: (b1, w1)")

    #first layer pre activation
    a1 = np.dot(w1, x) + b1

    #first layer activation
    h1 = sig(a1)

    #pattern repeats for subsequent layers
    if np.shape(h1)[0] != np.shape(w2)[1]:
        raise Exception("Invalid dimensions: (h1, w2)")

    #b2 needs to be vertical, same as amount of neurons as w2
    if np.shape(b2)[0] != np.shape(w2)[0]:
        raise Exception("Invalid dimensions: (b2, w2)")

    a2 = np.dot(w2, h1) + b2

    h2 = sig(a2)

    #h2 needs to be vertical, same height as w2 is wide
    if np.shape(h2)[0] != np.shape(w3)[1]:
        raise Exception("Invalid dimensions: (h2, w3)")


    if np.shape(b3)[0] != np.shape(w3)[0]:
        raise Exception("Invalid dimensions: (b3, w3)")

    a3 = np.dot(w3, h2) + b3

    out = sig(a3)

    return out

def selfAttention(x, wQ, wK, wV):
    #will allow for inputs to be mixed to varying degrees
    #simulating decison making influenced by other factors
    #analgous example: in the sentence 'The moose is in it's den'
    #to know what it refers to you have to take the other words into account
    #much more than the word 'it'

    #w dimensions - ([arbitrary], inputs)

    #x is vertical vectors, height needs to match width of each w(same width)
    if np.shape(x)[1] != np.shape(wQ)[0]:
        raise Exception("Invalid dimensions: (x, wQ)")

    if np.shape(x)[1] != np.shape(wK)[0]:
        raise Exception("Invalid dimensions: (x, wK)")

    if np.shape(x)[1] != np.shape(wV)[0]:
        raise Exception("Invalid dimensions: (x, wV)")


    queries = np.dot(wQ, x)
    keys = np.dot(wK, x)
    values = np.dot(wV, x)

    scores = np.dot(np.rot90(queries), keys)
    #note - scores are of format [[qnk1, qnk2, ...,qnkn]
    #                             [      ...           ]
    #                            [q1k1, q1k2, ..., qnkn]
    #rows correspond to different inputs
    #for item (x, y) is the score input x has given input y
    #(how much y matters to x)

    #dividing score by sqrt of key vector size
    #default for stabilizing gradients
    stabilize = scores/math.sqrt(np.shape(keys)[1])

    weights = softmax(stabilize, axis=1)

    #applying weights to values then summing
    #each output is a weighted sum of the inputs roughly corresponding
    #to original inputs

    #outputs same dimensionality as input
    output = None

    for row in range(np.shape(x)[0]):
        weightedVals = weights[row, :] * values

        wSum = np.vstack(np.sum(weightedVals, axis=1))

        if output is None:
            output = wSum
        else:
            np.concatenate(output, wSum, axis=1)

    return output

#using sigmoid instead of softmax because softmax fits things better
#when there is only one right answer, this will be more fuzzy
def sig(x):
    #sigmoid activation function
    return 1/(1 + np.exp(-x))

def softmax(x, axis=1):
    #note to future me - make sure the axis is right
    #sum outputs horizontal arrays - this may cause a bug
    return np.exp(x) / np.sum(np.exp(x), axis=axis)

"""
Finished selfAttention function, all decision logic now complete
"""
