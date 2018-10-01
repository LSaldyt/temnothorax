'''
i denotes nest that the ant is currently assessing or recruiting to
f denotes the nest from which the ant recruits

ant:
    state: {exporation, assessment, canvassing, committed} (exploration initially)
    current : index representing current assessment or recruitment nest (0 initially)
    source  : index representing source nest (None initially)

arrive-at-nest(ant, x):
    1-reject(ant.current, x) : at-nest(x, ant.current)
    reject(ant.current, x)   : search(ant.state)

accept-loc(ant, x):
    pass

states:
    exploration:
        follow(0, -):
            arrive-at-nest(x)
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
