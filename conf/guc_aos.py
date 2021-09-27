# dsname: Datastream name to pull data from
# dsname2: Secondary datastream(s) to include and merge
# t_delta: Script will resample data to 1 min.  If gaps are longer set this appropriately
# workers: Set to 1 in the case of radar data so it doesn't crash the system
conf = {
    'site': 'guc',
    'facility': 'M1',
    'start_date': '2021-09-01',
    'end_date': '2021-10-01',
    'outname': '/home/theisen/www/afc_summary/guc_aos_tables_linear.pdf', #options are png, pdf, etc
    'chart_style': 'linear',
    'info_style': 'simple',
    'dqr_table': True,
    'doi_table': True, #this will remove the DOI from besides the plots
    'instruments':{
        'acsm': {'dsname': 'aosacsmtofM1.a0', 't_delta': 30},
        'ccn': {'dsname': 'aosccn200M1.a1', 'data_path': '/data/datastream'},
        'co-analyzer': {'dsname': 'aoscoM1.a1', 'data_path': '/data/datastream'},
        'cpc': {'dsname': 'aoscpcf1mM1.b1', 'data_path': '/data/datastream'},
        'cpc': {'dsname': 'aoscpcu1mM1.b1', 'data_path': '/data/datastream'},
        'htdma': {'dsname': 'aoshtdmaM1.a1', 't_delta': 60, 'data_path': '/data/datastream'},
        'aosmet': {'dsname': 'aosmetM1.a1', 'data_path': '/data/datastream'},
        'nephelometer': {'dsname': 'aosnephdry1mM1.b1', 'data_path': '/data/datastream'},
        'ozone': {'dsname': 'aoso3M1.b1', 'data_path': '/data/datastream'},
        'psap': {'dsname': 'aospsap3w1mM1.b1', 'data_path': '/data/datastream'},
        'smps': {'dsname': 'aossmpsM1.a1', 't_delta': 30, 'data_path': '/data/datastream'},
        'sp2': {'dsname': 'aossp2auxM1.a0', 'data_path': '/data/datastream'},
        'uhsas': {'dsname': 'aosuhsasM1.b1', 'data_path': '/data/datastream'}
    }
}
