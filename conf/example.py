# dsname: Datastream name to pull data from
# dsname2: Secondary datastream(s) to include and merge
# t_delta: Script will resample data to 1 min.  If gaps are longer set this appropriately
# workers: Set to 1 in the case of radar data so it doesn't crash the system
conf = {
    'site': 'anx', # Site code
    'facility': 'S2', # Facility code
    'start_date': '2019-12-01', # Campaign start date for plot to span
    'end_date': '2020-05-31', # Campaign end date
    'outname': '/home/theisen/www/afc_summary/anx_s2.png', # Where to save.  Options are png, pdf, etc
    'chart_style': 'linear', # Which chart linear or 2D
    'info_style': 'simple', # simple will only display instrument name and datastream;
    'dqr_table': False, # True or False to add a table of DQRs at the end
    'doi_table': False, # True will make a table of DOIs, False and info_style not simple will add to plots
    'instruments':{
        # arm_inst_class: {'dsname': datastream name without site,
        #                  'dsname2': second datastream to include on same plot
        #                  't_delta': if expected sampling interval is not 1 minute set to minutes
        #                  'data_path': where to get data if not /data/archive on adc systems
        #                  'workers': if it is a large dataset like radars, set to 1 otherwise will
        #                             default to dask processing}
        'ceil': {'dsname': 'ceil10mS2.b1'},
        'dl': {'dsname': 'dlfptS2.b1', 'dsname2': 'dlppiS2.b1'},
        'ecor': {'dsname': '30ecorS2.b1', 't_delta': 30},
        'ldis': {'dsname': 'ldS2.b1'},
        'met': {'dsname': 'metwxtS2.b1'},
        'mpl': {'dsname': 'mplpolfsS2.b1'},
        'mwr': {'dsname': 'mwrlosS2.b1'},
        'tsi': {'dsname': 'tsiskycoverS2.b1'}
    }
}
