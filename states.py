from transition import transition, move, move_random
'''
i denotes nest that the ant is currently assessing or recruiting to
f denotes the nest from which the ant recruits

ant:
    state: {exporation, assessment, canvassing, committed} (exploration initially)
    sub-state : {follow, search, carried.. }
    current : index representing current assessment or recruitment nest (0 initially)
    source  : index representing source nest (None initially)

arrive-at-nest(ant, x):
    1-reject(ant.current, x) : at-nest(x, ant.current)
    reject(ant.current, x)   : search(ant.state)

accept-loc(ant, x):
    pass
'''

#def arrive(states, parameters, ant):
#pass

def accept(ant):


arrive = transition(substate='at-nest')

states = {
        'exploration': {
            'follow': {
                #'follow-leader' : transition(state=''), (Dependent on leaders and their locations)
                'get-lost' : transition(substate='search')},
            'search': {
                'picked-up'  : transition(substate='carried'),
                'find-0'     : move(0),
                'find-other' : move_random
                },
            'carried': {
                #'arrive' : arrive (Dependent on number of ants in carrying state)
            },
            'at-nest':{
                'search' : transition(substate='search')
                #'follow-leader' : transition()
                }
            },
        'assessment':{
            'follow': {
                'get-lost' : transition(substate='search'),
                #'arrive' : '' (Dependent on leaders)
                },
            'search': {
                'find-0' : move(0),
                'find-other' : move_random,
                'picked-up' : transition(substate='carried')
                },
            'carried': {
                #'arrive' : '' (Dependent on carrying ant)
                },
            'at-nest': {
                #'accept' : '', (Dependent on nest)
                #'accept' : transition(),
                'search' : transition(substate='search')
                #'follow-leader' : '' (Dependent on leaders)
                }},
        'canvassing' : {
            'search': {
                'find-0' : move(0),
                'find-other' : move_random,
                'picked-up' : transition(substate='carried')
                },
            'carried': {
                #'', 'arrive', (Carrying ant)
                },
            'at-nest' : {
                'search': transition(substate='search'),
                #'recruit' : 'accept-loc' (?)
                },
            'lead-forward' : {
                #'at-nest' : '' (?)
                }
        },
        'committed' :
        {
            'follow'         : {
                'search' : '',
                'getlost-trans' : 'arrive',
                'invgetlost + getlost*losttrans' : 'transport',
                },
            'search'         : {
                'find-0' : move(0),
                'find-other' : move_random,
                'picked-up' : ''
                },
            'carried'        : {
                'arrive' : '',
                'at-nest' : ''
                },
            'at-nest'        : {
                'follow-leader' : 'follow',
                'search' : 'search',
                'recruit' : 'pre-reverse'
                },
            'transport'      : {
                'stop-trans' : 'search',
                'invstoptrans' : 'pre-reverse'
                },
            'reverse-tandem' : {
                'transport' : ''
                },
            'pre-reverse'    : {
                '1-reverse' : 'transport',
                'reverse'  : 'reverse-tandem'
                }
        }
}



'''

states:
    exploration:
        follow(0, -):
            follow-leader : arrive-at-nest(x)
            get-lost: e-search(0, -)
        search(0, -):
            e-picked-up : e-carried(0, -)
            find(0, 0)  : e-at-nest(0, -)
            find(0, j)  : arrive-at-nest(j)
            find(0, i)  : arrive-at-nest(i)
        carried(0, -):
            arrive-at-nest(j)
            arrive-at-nest(i)
        at-nest(0, -)
            e-search : e-search(0, -)
            follow-leader : follow(0, -)
    assessment:
        follow(i, f):
            get-lost: a-search(i, f)
            arrive-at-nest(x)
        search(i, f)
            find(j, i) : arrive-at-nest(j)
            a-picked-up : a-carried(i, f)
            find(i, x) : a-at-nest(x, f)
        carried(i, f):
            arrive-at-nest(x)
        at-nest(i, f):
            accept(i) : accept-loc
            a-search : search(i, f)
            follow-leader : follow(0, -)
        at-nest(j, f):
           ?
    canvassing:
        search(i, f):
            find(j, i) : arrive-at-nest(j)
            find(i, f) : at-nest(i, f)
            c-picked-up: carried(i, f)
        carried(i, f):
            arrive-at-nest(x)
        at-nest(i, f):
            c-search: search(i, f)
            recruit: accept-loc(i)
        lead-forward(i, f):
            at-nest(i, f)
    committed:
        follow(i, f):
            search(i, f)
            getlost * (1-losttrans): arrive-at-nest(j)
            1-getlost +  getlost * losttrans: transport(i, f)
        search(i, f):
            find(j, i) : arrive-at-nest(j)
            c-picked-up: carried(i, f)
            find(i, i) : at-nest(i, f)
        carried(i, f):
            arrive-at-nest(x)
            at-nest(i, f)
        at-nest(i, f):
            follow-leader : follow(i, f)
            c-search: search(i, f)
            recruit(i) : pre-reverse
        transport(i, f):
            stop-trans : search(i, f)
            1-stop-trans: pre-reverse
        reverse-tandem(i, f):
            transport(i, f)
        pre-reverse:
            1-reverse: transport(i, f)
            reverse: reverse-tandem(i, f)
'''
