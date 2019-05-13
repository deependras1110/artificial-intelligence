#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        check_true_false
# Purpose:     Main entry into logic program. Reads input files, creates 
#              base, tests statement, and generates result file.
#
# Created:     09/25/2011
# Last Edited: 07/22/2013     
# Notes:       *Ported by Christopher Conly from C++ code supplied by Dr. 
#               Vassilis Athitsos.
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so I put it in a list, which
#               is passed by reference.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import deepcopy
from logical_expression import *

def checkTable(kb, statement, model):
    a = eval_expression(kb, model)
    # print model
    # print a
    # print "----------"
    if eval_expression(kb, model) == True:
        if eval_expression(statement, model) == True:
            return True
        else:
            return False
    else:
        return True

def checkAll(kb, statement, symbols, model):
    if len(symbols) > 0:
        first = symbols.pop()

        modelTrue = deepcopy(model)
        modelTrue[first] = True
        modelFalse = deepcopy(model)
        modelFalse[first] = False

        return (checkAll(kb, statement, deepcopy(symbols), modelTrue) and checkAll(kb, statement, deepcopy(symbols), modelFalse))
    else:
        return checkTable(kb, statement, deepcopy(model))

def checkEntailment(kb, statement, kb_subexpressions):
    symbols = find_symbols(kb, statement)
    model = {}
    for subexpression in kb_subexpressions:
        if subexpression.symbol[0]:
            model[subexpression.symbol[0]] = True
            try:
                symbols.pop(symbols.index(subexpression.symbol[0]))
            except: 
                pass

        elif subexpression.connective[0] == 'not':
            if subexpression.subexpressions[0].symbol[0]:
                model[subexpression.subexpressions[0].symbol[0]] = False
                try: 
                    symbols.pop(symbols.index(subexpression.subexpressions[0].symbol[0]))
                except: pass
    return checkAll(kb, statement, deepcopy(symbols), deepcopy(model))

def check_true_false(knowledge_base, statement, kb_subexpression):

    kb_statement1 = checkEntailment(knowledge_base, statement, deepcopy(kb_subexpression))

    notStatement = logical_expression()
    notStatement.connective = ['not']
    notStatement.subexpressions.append(deepcopy(statement))
    kb_statement2 = checkEntailment(knowledge_base, notStatement, deepcopy(kb_subexpression))

    if kb_statement1 == True and kb_statement2 == False:
        ans = "Definitely True"
    elif kb_statement1 == False and kb_statement2 == True:
        ans = "Definitely False"
    elif kb_statement1 == False and kb_statement2 == False:
        ans = "Possibly True, Possibly False"
    elif kb_statement1 == True and kb_statement2 == True:
        ans = "Both True and False"

    f = open("result.txt", "w")
    print ans
    f.write(ans)
    print "Answer printed in result.txt"
    exit(0)

def main(argv):
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'rb')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)

    # Create the knowledge base with wumpus rules
    print '\nLoading wumpus rules...'
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # A mutable counter so recursive calls don't just make a copy
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'rb')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print 'Loading additional knowledge...'
    kb_subexpression = []
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # a mutable counter
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        kb_subexpression.append(subexpression)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')
    print len(kb_subexpression)
    # I had left this line out of the original code. If things break, comment out.
    # print_expression(knowledge_base, '\n')

    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'rb')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print 'Loading statement...'
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    
    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print '\nChecking statement: ',
    print_expression(statement, '')
    print '\n'

    # Run the statement through the inference engine
    check_true_false(knowledge_base, statement, deepcopy(kb_subexpression))

    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)