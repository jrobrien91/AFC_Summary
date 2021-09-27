# dsname: Datastream name to pull data from
# dsname2: Secondary datastream(s) to include and merge
# t_delta: Script will resample data to 1 min.  If gaps are longer set this appropriately
# workers: Set to 1 in the case of radar data so it doesn't crash the system
conf = {
    'site': 'hou',
    'facility': 'M1',
    'start_date': '2021-08-01',
    'end_date': '2021-10-01',
    'outname': '/home/theisen/www/afc_summary/test.pdf', #options are png, pdf, etc
    'chart_style': 'linear',
    'info_style': 'simple',
    'dqr_table': True,
    'doi_table': True, #this will remove the DOI from besides the plots
    'instruments':{
        'rwp': {'dsname': '915rwpwindconX10.a1', 'data_path': '/data/datastream', 't_delta': 60},
    }
}
