# dsname: Datastream name to pull data from
# dsname2: Secondary datastream(s) to include and merge
# t_delta: Script will resample data to 1 min.  If gaps are longer set this appropriately
# workers: Set to 1 in the case of radar data so it doesn't crash the system
conf = {
    'site': 'hou',
    'facility': 'M1',
    'start_date': '2021-09-01',
    'end_date': '2021-10-01',
    'outname': '/home/theisen/www/afc_summary/hou_aos_tables_linear.pdf', #options are png, pdf, etc
    'chart_style': 'linear',
    'info_style': 'simple',
    'dqr_table': True,
    'doi_table': True, #this will remove the DOI from besides the plots
    'instruments':{
        'acsm': {'dsname': 'aosacsmM1.a0', 't_delta': 30},
        'aeth': {'dsname': 'aosaeth2spotM1.a1', 'data_path': '/data/datastream'},
        'ccn': {'dsname': 'aosccn200M1.a1', 'data_path': '/data/datastream'},
        'co-analyzer': {'dsname': 'aoscoM1.a1', 'data_path': '/data/datastream'},
        'cpc': {'dsname': 'aoscpcf1mM1.b1', 'data_path': '/data/datastream'},
        'cpc': {'dsname': 'aoscpcu1mM1.b1', 'data_path': '/data/datastream'},
        'htdma': {'dsname': 'aoshtdmaM1.a1', 't_delta': 60, 'data_path': '/data/datastream'},
        'aosmet': {'dsname': 'aosmetM1.a1', 'data_path': '/data/datastream'},
        'nephelometer': {'dsname': 'aosnephdry1mM1.b1', 'data_path': '/data/datastream'},
        'nephelometer': {'dsname': 'aosnephwet1mM1.b1', 'data_path': '/data/datastream'},
        'ozone': {'dsname': 'aoso3M1.b1', 'data_path': '/data/datastream'},
        'psap': {'dsname': 'aospsap3w1mM1.b1', 'data_path': '/data/datastream'},
        'smps': {'dsname': 'aossmpsM1.a1', 't_delta': 30, 'data_path': '/data/datastream'},
        'so2': {'dsname': 'aosso2M1.a1', 'data_path': '/data/datastream'},
        'uhsas': {'dsname': 'aosuhsasM1.b1', 'data_path': '/data/datastream'}
    }
}
