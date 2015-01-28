def make_creautre_summery(name=None,init=None):
    if not name:
        name = ''
    if not init:
        init = ''
    out = '<html>'
    if name == '':
        out = '{}<h1>Unnamed</h1>'.format(out)
    else:
        out = '{}<h1>{}</h1>'.format(out,name)
    out = '{}<b>Name:</b> {}<br>'.format(out,name)
    out = '{}<b>Initiative:</b> {}<br>'.format(out,init)
    out = '{}</html>'.format(out)
    return out


def make_init_text(name=None,init=None):
    if not init:
        return ''
    if not name: 
        return ''
    if init < -1:
        return ''
    try:
        init = int(init)
    except ValueError:
        return ''

    return '{}. {}'.format(init,name)
    
