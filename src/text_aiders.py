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
    
