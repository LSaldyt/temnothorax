'''
Find0,n, Findm,n	0.01±0.002/min	484
Find0,0	0.18±0.01/min	484
Findn,n	0.09±0.002/min	2028
SearchExplore	0. 51±0.02/min	473
SearchAssess	0.23±0.01/min	1464
SearchCanvas	0.14±0.02/min	158
SearchCommitted	0.06±0.01/min	642
PropLost	0.91±0.04	55
DurationForward	7.2±1.6 min	4
DurationReverse	4.6±0.5 min	9
RejectThick, Thin	1.0±0.0	16
RejectThin, Thick	0.03±0.03	37

PickedUpExplore	0.010±0.001/min	110
PickedUpAssess	0.005±0.001/min	75
PickedUpCanvas	0.005±0.002/min	4
PickedUpCommitted	0.005±0.001/min	45
AcceptThick	0.053±0.004/min	257
AcceptThin	0.034±0.006/min	278
AcceptDark	0.032±0.005/min	84
AcceptLight	0.013±0.006/min	70
MinAccept	5 min	535
RecTimeTandem
 Mean	b: 17±1 min, a: 11±1 min, k: 2.0±0.9	152
 SD	b: 11±2 min, a: 10±2 min, k: 1.5±1.1	152
RecTimeTransport
 Mean	b: 11±1 min, a: 7±1 min, k: 1.5±0.5	1932
 SD	b: 9±1 min, a: 7±1 min, k: 0.6±0.3	1932
PropRecTransport	0.45±0.01	365
PropRecTandem	0.65±0.03	16
QuorumMet	T: 0.017±0.001, k: 2.0±0.2	443
RecruitThick, RecruitDark	0.23±0.01/min	405
RecruitThin, RecruitLight	0.15±0.02/min	395
TransInNestTime	1.0±0.02 min	1926
PauseTrans	0.25±0.19	535
Reverse	0.06±0.01	2117
LostTrans	0.56±0.12	16
'''

#Structure: paramname, three-tuple {p : (mean, sd, n)}

process_nest_index = lambda i : 0 if i == 0 else 'other'

def index_parameter(parameters, p, ant):
    state = ant.state
    if p in parameters:
        return parameters[p]
    elif state in parameters and p in parameters[state]:
        return parameters[state][p]
    elif 'find' in p:
        return parameters['__find_parameters__'][process_nest_index(ant.source)][p]
    elif p in {'accept', 'recruit'}:
        return parameters[p][nest_parameters['nests'][ant.current]]
    else:
        raise KeyError('Parameter not found: {} in state {}'.format(p, state))

nest_parameters = {
        'nests' : {
            1 : {'depth' : 'thick'},
            2 : {'depth' : 'thin'}
            }
        }

parameters = {
        'get-lost' : (0.91, 0.04, 55),
        'exploration' : {
            'search' : (0.51, 0.02, 473),
            'picked-up' : (0.01, 0.001, 110)
            },
        'assessment' : {
            'search'  : (0.23, 0.01, 1464),
            'picked-up'  : (0.005, 0.001, 75)
            },
        'canvassing' : {
            'search' : (0.12, 0.02, 158),
            'picked-up' : (0.005, 0.002, 4)
            },
        'committed'  : {
            'search' : (0.06, 0.01, 642),
            'picked-up' : (0.005, 0.001, 45)
            },
        '__find_parameters__' : {
            0 :  {'find-0' : (0.18, 0.1, 484),
                  'find-other' : (0.01, 0.002, 484)},
            'other' : {'find-0' : (0.09, 0.002, 2028),
                       'find-other' : (0.09, 0.002, 2028)}},
        '__nest_count__' : len(nest_parameters['nests']),
        'accept' : {
            'thick' : (0.053, 0.004, 257),
            'thin'  : (0.034, 0.006, 278),
            'dark'  : (0.032, 0.005, 84),
            'light' : (0.013, 0.006, 70)
            },
        'recruit' : {
            'thick' : (0.23, 0.01, 405),
            'dark'  : (0.23, 0.01, 405),
            'thin'  : (0.15, 0.02, 395),
            'light' : (0.15, 0.02, 395),
            },
    'reject-thick-thin' : (1.0, 0.0, 16),
    'reject-thin-thick' : (0.03, 0.03, 37),
    'min-accept'   : (5, 0, 535),
    'prop-rec-transport' : (0.45, 0.01, 365),
    'prop-rec-tandem'    : (0.65, 0.03, 16),
    'trans-in-nest-time' : (1.0, 0.02, 1926),
    'pause-trans'   : (0.25, 0.19, 535),
    'reverse'       : (0.06, 0.1, 2117),
    'lost-trans'    : (0.56, 0.12, 16),
#'recruit-thick' : (0.23, 0.01, 405),
#'recruit-dark'  : (0.23, 0.01, 405),
#'recruit-thin'  : (0.15, 0.02, 395),
#'recruit-light'  : (0.15, 0.02, 395),
#'accept-thick' : (0.053, 0.004, 257),
#'accept-thin'  : (0.034, 0.006, 278),
#'accept-dark'  : (0.032, 0.005, 84),
#'accept-light' : (0.013, 0.006, 70),
#'duration-forward' : (7.2, 1.6, 4),
#'duration-reverse' : (4.6, 0.5, 9),
}


'''
What are these parameters? See what paper says.
QuorumMet	T: 0.017±0.001, k: 2.0±0.2	443
RecTimeTandem
 Mean	b: 17±1 min, a: 11±1 min, k: 2.0±0.9	152
 SD	b: 11±2 min, a: 10±2 min, k: 1.5±1.1	152
RecTimeTransport
 Mean	b: 11±1 min, a: 7±1 min, k: 1.5±0.5	1932
 SD	b: 9±1 min, a: 7±1 min, k: 0.6±0.3	1932
'''

