# default.ttcd contains a default Twelve Tone Composition Definition (ttcd).
# You can make copies of this, edit the parameters and pass the file name on the commandline to create your own MIDI composition.
from collections import OrderedDict
import configparser

def config(cfgfile='default.amgd'):

    timechanges = {}
    tempochanges = {}
    parts = OrderedDict()
    pc_sets = OrderedDict()

    cfg = {}

    config = configparser.ConfigParser()
    config.read(cfgfile)
    cfg['amg_version'] = config['SYS']['version']

    cfg['outfile'] = config['MAIN']['outfile']
    cfg['outpath'] = config['MAIN']['outpath']
    cfg['musicxmlPath'] = config['MAIN']['musicxmlPath']
    cfg['copyright'] = config['METADATA']['copyright']
    cfg['date'] = config['METADATA']['date']
    cfg['composer'] = config['METADATA']['composer']
    cfg['title'] = config['METADATA']['title']

    cfg['mode'] = config['COMP']['Mode']
    cfg['chordal'] = config['COMP']['Chordal']
    cfg['orow'] = config['COMP']['ORow']
    cfg['duration'] = config['COMP']['Duration']
    cfg['tempo'] = int(config['COMP']['Tempo'])
    cfg['timesig'] = config['COMP']['TimeSig']
    cfg['pcs'] = int(config['COMP']['PCS'])
    cfg['pct_cluster'] = int(config['COMP']['Cluster'])
    cfg['max_cluster'] = int(config['COMP']['ClusterMax'])
    cfg['pct_repeat'] = int(config['COMP']['Repeat'])
    cfg['max_repeat'] = int(config['COMP']['RepeatMax'])
    cfg['rois'] = config['COMP']['ROIS']
    cfg['same_series'] = config['COMP']['Same Series']

    for n in config['TEMPOCHANGES']:
        tempochanges[n] = config['TEMPOCHANGES'][n]+'\n'

    for n in config['TIMECHANGES']:
        timechanges[n] = config['TIMECHANGES'][n]+'\n'

    for n in config['PARTS']:
        parts[n] = config['PARTS'][n]

    for n in config['PCSETS']:
        pc_sets[n] = config['PCSETS'][n]

    cfg['tempochanges'] = tempochanges
    cfg['timechanges'] = timechanges
    cfg['parts'] = parts
    cfg['pc_sets'] = pc_sets


    print('\nUsing AMG definition file: ', cfgfile)
    print('AMG version: ' + cfg['amg_version'] )

    return cfg
