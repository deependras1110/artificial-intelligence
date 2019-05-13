Task 1

To execute the program, run the following command:
    $ python compute_a_posteriori.py [sequence]

Example:
    $ python compute_a_posteriori.py CCCCC

Note:
- The output is stored in result.txt
- All the decimal values are corrected to 5 points

----------------------------------------------------------------

Task 2

To execute the program, run the following command:
    $ python bnet.py [required-parameters] [given [on-given-parameters]]

Example:
    $ python bnet.py Jf Mt given Et

Note:
- 'given' should be in lower case
- Every term should start with Upper Case 'X' and end with lower case
- The Upper case of term represents events, where 
    'A' - Alarm
    'B' - Burglary
    'E' - Earthquake
    'M' - Mary Calls
    'J' - John Calls
- While the Lower case of term represents happening in boolean. Like:
    't' - True
    'f' - False
- Say, the term is 'Af' it means Event 'Alarm Rings did not happen'
- required-parameters and on-given-parameters are collection of terms seperated by space