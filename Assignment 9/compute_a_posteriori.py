import sys
import re

def __main__(argv):
    if argv[1]:
        pattern = re.compile('^[LC]+$')
        sequence = argv[1].upper()
        if pattern.match(sequence):

            # Finding possibilities of lime and cherries
            p_l = 0
            p_c = 0
            for i in range(0,5):
                p_l = p_l + (p_l_h[i]*p_h[i])
                p_c = p_c + (p_c_h[i]*p_h[i])

                
            f = open("result.txt", "w")
            f.write("Observation sequence Q: " + str(sequence))
            f.write("\nLength of Q: " + str(len(sequence)))
            for j in range(0, len(sequence)):
                
                c = sequence[j]
                f.write("\n\nAfter observation "+str(j+1)+" = "+str(c)+"\n")

                # Finding possibility of 'H' given sequence
                if c == 'L':
                    s = p_l_h
                    d = p_l
                else:
                    s = p_c_h
                    d = p_c
                for i in range(0,5):
                    p_h[i] = (p_h[i]/d)*s[i]
                    f.write('\nP(h' + str(i) + ' | Q) = ' + str(round(p_h[i],5)))

                # Finding possibility of lime and cherry
                p_l = 0
                p_c = 0
                for i in range(0,5):
                    p_l = p_l + (p_l_h[i]*p_h[i])
                    p_c = p_c + (p_c_h[i]*p_h[i])

                f.write('\n\nProbability that the next candy we pick will be C, given Q: ' + str(round(p_c, 5)))
                f.write('\nProbability that the next candy we pick will be L, given Q: ' + str(round(p_l, 5)))

        else:
            exit('Sequence should have series of L or M')
    else:
        exit("Follow the syntax: \npython compute_a_posteriori.py [sequence]")

p_h = [0.10, 0.20, 0.40, 0.20, 0.10]
p_c_h = [1.00, 0.75, 0.50, 0.25, 0.00]
p_l_h = [0.00, 0.25, 0.50, 0.75, 1.00]
__main__(sys.argv)