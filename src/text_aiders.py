def make_creautre_summery(name=None,init=None,hp=None):
    if not name:
        name = ''
    if not init:
        init = ''
    if not hp:
        hp = ''
    out = '<html>'
    if name == '':
        out = '{}<h1>Unnamed</h1>'.format(out)
    else:
        out = '{}<h1>{}</h1>'.format(out,name)
    out = '{}<b>Name:</b> {}<br>'.format(out,name)
    out = '{}<b>Initiative:</b> {}<br>'.format(out,init)
    out = '{}<b>HP:</b> {}<br>'.format(out,hp)
    out = '{}</html>'.format(out)
    return out


def make_init_text(name=None,init=None,hp=None):
    if hp == 0: hp = '0' #For the "not hp" test below
    if not init: #There has to be an initiative value
        return ''
    if not hp: #There has to be an hp value
        return ''
    if not name: #There has to be a name
        return ''
    if init < -1: #An empty initiaive
        return ''
    try:
        init = int(init)
        hp = int(hp)
    except ValueError: #invalid values;
        return ''

    return '{}. {} ({})'.format(init,name,hp)
    
def list_init_round(init_labels=[]):
    #This will produce a string of ordered list of creatures
    out = '<html><h1>Choose target</h1>'
    i = 1
    for label in init_labels:
        name = label.name
        hp = label.hp
        init = label.init_round
        if init < 0:
            continue
        line = '<br>{}) {} - {} hit points'.format(i,name,hp)
        out = '{}{}'.format(out,line)
        i += 1
    out = '{}</html>'.format(out)
    return out
