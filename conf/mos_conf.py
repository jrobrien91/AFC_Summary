# dsname: Datastream name to pull data from
# dsname2: Secondary datastream(s) to include and merge
# t_delta: Script will resample data to 1 min.  If gaps are longer set this appropriately
# workers: Set to 1 in the case of radar data so it doesn't crash the system
conf = {
    'site': 'mos',
    'facility': 'M1',
    'start_date': '2019-10-01',
    'end_date': '2020-10-31',
    'outname': '/home/theisen/www/afc_summary/mos_tables.pdf', #options are png, pdf, etc
    'dqr_table': True,
    'doi_table': True, #this will remove the DOI from besides the plots
    'instruments':{
        'aeri': {'dsname': 'aerisummaryM1.b1'},
        'ceil': {'dsname': 'ceilM1.b1'},
        'dl': {'dsname': 'dlfptM1.a1', 'dsname2': 'dlusrM1.a1'},
        'hsrl': {'dsname': 'hsrlM1.a1', 'data_path': '/data/datastream'},
        'ldis': {'dsname': 'ldM1.b1'},
        'mpl': {'dsname': 'mplpolfsM1.b1'},
        'mwr': {'dsname': 'mwrlosM1.b1'},
        'mwr3c': {'dsname': 'mwr3cM1.b1'},
        'rwp': {'dsname': '1290rwpprecipconM1.a1', 'dsname2': '1290rwpwindconM1.a1', 't_delta': 10},
        'sonde': {'dsname': 'sondewnpnM1.b1', 't_delta': 1440/4},
        'tsi': {'dsname': 'tsiskycoverM1.b1', 'data_path': '/data/datastream'}
    }
}
